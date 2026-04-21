# SQL Reference — IE 6700 Final Exam

---

## Schemas

### classicmodels
```
Customers(customerNumber, customername, contactLastName, contactFirstName, phone,
          addressline1, addressline2, city, state, postalcode, country, salesRepEmployeeNumber)
Employees(employeeNumber, lastName, firstName, extension, email, officeCode, reprotsTo, jobtitle)
Offices(officecode, city, phone, addressLine1, addressLine2, state, country, postalcode, territory)
Orderdetails(orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
Orders(orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
Payments(customerNumber, checkNumber, paymentDate, amount)
Productlines(productLine, textDescription, htmlDescription, image)
Products(productCode, productName, productLine, prodocScale, productVendor,
         productDescription, quantityInStock, buyPrice, MSRP)
```

### world
```
City(ID, Name, CountryCode, District, Population)
Country(Code, Name, Continent, Region, SurfaceArea, IndepYear, Population,
        LifeExpectancy, GNP, GNPOld, LocalName, GovernmentForm, HeadofState, Capital, Code2)
CountryLanguage(CountryCode, Language, IsOfficial, Percentage)
```

### wine purchase order
```
Product(prodnr, prodname, prodtype, available_quantity)
Supplier(supnr, supname, supcity, ...)
Supplies(prodnr, supnr, purchase_price, ...)
Purchase_Order(ponr, podate, supnr, ...)
PO_Line(ponr, prodnr, quantity, ...)
```

---

## SQL Statement Types

### SELECT
```sql
SELECT column1, column2, ...
FROM table_name
[WHERE condition]
[GROUP BY column]
[HAVING condition]
[ORDER BY column [ASC|DESC]];
```

### INSERT
```sql
-- Insert a single row
INSERT INTO customers (customerNumber, customername, city, country)
VALUES (999, 'New Customer', 'Boston', 'USA');

-- Insert multiple rows
INSERT INTO customers (customerNumber, customername, city, country)
VALUES (1001, 'Alpha Corp', 'NYC', 'USA'),
       (1002, 'Beta Inc',  'LA',  'USA');

-- Insert from a SELECT
INSERT INTO archive_orders (orderNumber, customerNumber, orderDate)
SELECT orderNumber, customerNumber, orderDate
FROM orders
WHERE status = 'Cancelled';
```

### UPDATE
```sql
-- Update a single column
UPDATE products
SET buyPrice = buyPrice * 1.10
WHERE productLine = 'planes';

-- Update multiple columns
UPDATE customers
SET city = 'New York', state = 'NY'
WHERE customerNumber = 103;

-- Update using a subquery
UPDATE orderdetails
SET priceEach = (SELECT MSRP FROM products WHERE products.productCode = orderdetails.productCode)
WHERE priceEach IS NULL;
```

### DELETE
```sql
-- Delete specific rows
DELETE FROM orders
WHERE status = 'Cancelled';

-- Delete using a subquery
DELETE FROM orderdetails
WHERE orderNumber IN (
    SELECT orderNumber FROM orders WHERE status = 'Cancelled'
);

-- Delete all rows (keep table structure)
DELETE FROM payments;
```

---

## SELECT Component Syntax

```sql
SELECT   <columns, expressions, aggregates>      -- what to return
FROM     <table(s), joins, subqueries>           -- data source
WHERE    <row-level filter, before grouping>     -- filter rows
GROUP BY <grouping columns>                      -- collapse into groups
HAVING   <group-level filter, after grouping>    -- filter groups
ORDER BY <sort columns / positions> [ASC|DESC];  -- sort output
```

**Execution order:** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

---

## 1. Simple Queries

```sql
-- Retrieve everything in Country
SELECT * FROM country;

-- Retrieve specific columns
SELECT code, name FROM country;

-- Retrieve with alias and arithmetic
SELECT name, countrycode, population / 1000 AS population_thousands FROM city;

-- Distinct values
SELECT DISTINCT countrycode FROM city;

-- Filter with WHERE
SELECT id, name, population FROM city WHERE countrycode = 'USA';

-- Multiple conditions
SELECT id, name, population FROM city
WHERE countrycode = 'IND' AND population > 1000000;

-- BETWEEN
SELECT id, name, population FROM city
WHERE population BETWEEN 1000000 AND 10000000;

-- IN
SELECT code, name FROM country WHERE continent IN ('Asia', 'Africa');

-- LIKE (pattern matching)
SELECT code, name FROM country WHERE governmentform LIKE '%republic%';

-- IS NULL
SELECT code, name FROM country WHERE indepyear IS NULL;

-- Count customers from NYC (classicmodels)
SELECT COUNT(*) FROM customers WHERE city = 'NYC';

-- Orders sorted ascending by date, descending by customer number
SELECT ordernumber FROM orders ORDER BY orderdate ASC, customernumber DESC;

-- Order by column position
SELECT productcode, ordernumber, priceeach FROM orderdetails
WHERE productcode = 'S24_2840'
ORDER BY 3 DESC;

-- Order by column name
SELECT code, name, surfacearea, indepyear FROM country
ORDER BY surfacearea DESC, indepyear ASC;
```

---

## 2. Aggregation

Aggregate functions operate on a set of values and return a single value.  
`COUNT(*)` counts all rows; `COUNT(col)` skips NULLs; `COUNT(DISTINCT col)` counts unique non-NULL values.

```sql
-- COUNT(*) vs COUNT(col) vs COUNT(DISTINCT col)
SELECT COUNT(*)                              FROM customers WHERE city = 'NYC';
SELECT COUNT(priceeach)                     FROM orderdetails WHERE productcode = 'S24_3969';
SELECT COUNT(DISTINCT priceeach)            FROM orderdetails WHERE productcode = 'S24_3969';

-- SUM
SELECT SUM(quantityordered) FROM orderdetails;
SELECT productcode, SUM(quantityordered) AS total_quantity
FROM orderdetails WHERE productcode = 'S24_2840';

-- Weighted average (all rows)
SELECT AVG(priceeach) AS weighted_avg_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- Unweighted average (distinct values only)
SELECT AVG(DISTINCT priceeach) AS unweighted_avg_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- VARIANCE
SELECT VARIANCE(priceeach) AS variance_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- MIN / MAX
SELECT MIN(priceeach) AS min_price, MAX(priceeach) AS max_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- World schema examples
SELECT COUNT(*)           FROM country WHERE governmentform = 'Republic';
SELECT COUNT(region)      FROM country WHERE governmentform = 'Republic';
SELECT COUNT(DISTINCT region) FROM country WHERE governmentform = 'Republic';
SELECT SUM(GNP)           FROM country WHERE governmentform = 'Republic';
SELECT AVG(GNP)           AS weighted_average_GNP  FROM country WHERE governmentform = 'Republic';
SELECT AVG(DISTINCT GNP)  AS unweighted_average_GNP FROM country WHERE governmentform = 'Republic';
SELECT VARIANCE(GNP)      AS variance_GNP FROM country WHERE governmentform = 'Republic';
SELECT MIN(GNP) AS min_GNP, MAX(GNP) AS max_GNP FROM country WHERE governmentform = 'Republic';
```

---

## 3. GROUP BY / HAVING

**Rule:** When using GROUP BY, every column in SELECT must either be in the GROUP BY clause or be inside an aggregate function. HAVING filters *after* grouping (like WHERE, but for groups).

```sql
-- Products with at least 25 orders
SELECT productcode FROM orderdetails
GROUP BY productcode
HAVING COUNT(*) >= 25;

-- Products where total quantity ordered > 1000
SELECT productcode, SUM(quantityordered) AS total_qty FROM orderdetails
GROUP BY productcode
HAVING SUM(quantityordered) > 1000;

-- Countries with at least 3 cities in the City table
SELECT countrycode FROM city
GROUP BY countrycode
HAVING COUNT(*) > 2;

-- Countries whose total city population exceeds 100,000,000
SELECT countrycode FROM city
GROUP BY countrycode
HAVING SUM(population) > 100000000;

-- Productcode, productname, total quantity ordered (must join first, then group)
SELECT od.productcode, p.productname, SUM(quantityordered) AS totalquantity
FROM orderdetails od, products p
WHERE od.productcode = p.productcode
GROUP BY od.productcode;

-- Wine: highest available_quantity per product type, descending
SELECT prodtype, MAX(available_quantity) AS highest_quantity
FROM product
GROUP BY prodtype
ORDER BY highest_quantity DESC;

-- Wine: highest purchase price per product type
SELECT p.prodtype, MAX(s.purchase_price)
FROM product p, supplies s
WHERE p.prodnr = s.prodnr
GROUP BY p.prodtype;

-- Wine: total quantity ordered per product type
SELECT p.prodtype, SUM(pol.quantity) AS total_quantity
FROM product p, purchase_order po, po_line pol
WHERE p.prodnr = pol.prodnr AND pol.ponr = po.ponr
GROUP BY p.prodtype;
```

---

## 4. Inner Join

An **INNER JOIN** returns only rows where there is a match in **both** tables. Rows with no match are excluded.

**Implicit syntax (comma + WHERE):**
```sql
SELECT c.customernumber, c.customername, o.ordernumber, o.orderdate,
       p.productcode, p.productname, od.quantityordered
FROM customers c, orders o, orderdetails od, products p
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode;
```

**Explicit JOIN syntax:**
```sql
SELECT c.customernumber, c.customername, o.ordernumber
FROM customers c
INNER JOIN orders o ON c.customernumber = o.customernumber;
```

**Self join — pairs of customers in the same city:**
```sql
SELECT c1.customername, c2.customername, c1.city
FROM customers c1, customers c2
WHERE c1.city = c2.city AND c1.customernumber < c2.customernumber;
```

**Multi-table join — customers who ordered 'planes':**
```sql
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od, products p
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode
  AND p.productline    = 'planes';
```

**Join with aggregation — product total quantity:**
```sql
SELECT od.productcode, p.productname, SUM(od.quantityordered) AS totalquantity
FROM orderdetails od, products p
WHERE od.productcode = p.productcode
GROUP BY od.productcode;
```

---

## 5. Outer Joins (LEFT, RIGHT, FULL)

An **OUTER JOIN** returns matched rows **plus** unmatched rows from one or both sides, filling missing columns with NULL.

| Join Type | Keeps unmatched rows from |
|-----------|--------------------------|
| LEFT OUTER JOIN | Left (first) table |
| RIGHT OUTER JOIN | Right (second) table |
| FULL OUTER JOIN | Both tables (not supported in MySQL — simulate with UNION) |

```sql
-- LEFT OUTER JOIN: all customers, even those with no orders
SELECT c.customernumber, c.customername, o.ordernumber
FROM customers AS c
LEFT OUTER JOIN orders AS o ON c.customernumber = o.customernumber;

-- RIGHT OUTER JOIN: all products, even those with no orders
SELECT p.productcode, p.productname, SUM(od.quantityordered) AS total_qty
FROM orderdetails AS od
RIGHT OUTER JOIN products AS p ON od.productcode = p.productcode
GROUP BY p.productcode;

-- Wine: total orders per supplier city, including cities with zero orders
WITH suporder AS (
    SELECT supnr, COUNT(*) AS totorder
    FROM purchase_order
    GROUP BY supnr
)
SELECT r.supcity, SUM(so.totorder) AS tot_order_by_city
FROM supplier r
LEFT OUTER JOIN suporder so ON r.supnr = so.supnr
GROUP BY r.supcity
ORDER BY 2 DESC;

-- FULL OUTER JOIN simulation in MySQL (UNION of LEFT and RIGHT)
SELECT c.customernumber, c.customername, o.ordernumber
FROM customers c
LEFT OUTER JOIN orders o ON c.customernumber = o.customernumber
UNION
SELECT c.customernumber, c.customername, o.ordernumber
FROM customers c
RIGHT OUTER JOIN orders o ON c.customernumber = o.customernumber;
```

---

## 6. Nested (Non-Correlated) Queries

A **nested query** (subquery) is a query inside another query. It is evaluated **once** independently and its result is passed to the outer query. The subquery does **not** reference columns from the outer query.

```sql
-- Single-value subquery (=)
-- Name of the customer who placed order 10202
SELECT customername FROM customers
WHERE customernumber = (SELECT customernumber FROM orders WHERE ordernumber = '10202');

-- Multi-value subquery (IN) — customers who ordered product 'S24_2840'
-- #1: chained subqueries
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT customernumber FROM orders
    WHERE ordernumber IN (
        SELECT ordernumber FROM orderdetails WHERE productcode = 'S24_2840'
    )
);

-- #2: join inside subquery
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S24_2840'
);

-- Customers who ordered BOTH 'S24_2840' AND 'S50_1341'
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S24_2840'
)
AND customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S50_1341'
);

-- Subquery in FROM clause (derived table / inline view)
-- Wine: products with highest available_quantity per type
SELECT p.prodname, p.prodtype, p.available_quantity
FROM product p,
    (SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
     FROM product
     GROUP BY prodtype) AS pm
WHERE p.prodtype = pm.prodtype
  AND p.available_quantity = pm.max_ava_quantity;
```

---

## 7. Correlated Queries

A **correlated query** references a column from the **outer query**. It is re-evaluated for **every row** of the outer query (like a loop). This makes it slower but more expressive.

**Key difference from nested:** the subquery contains a reference to the outer table alias (e.g., `p.productcode`, `c.customernumber`).

```sql
-- Products with at least 5 orders (correlated)
SELECT p.productname FROM products p
WHERE (SELECT COUNT(*) FROM orderdetails od WHERE od.productcode = p.productcode) >= 5;

-- Customers who ordered a product below its average price
SELECT c.customernumber, c.customername, p.productcode, p.productname,
       od.priceeach, od.quantityordered
FROM customers c, products p, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode
  AND od.priceeach < (SELECT AVG(priceeach) FROM orderdetails WHERE productcode = p.productcode);

-- Top 2 customers by order count (correlated, approach #1)
SELECT customernumber, customername FROM customers
WHERE customernumber IN (
    SELECT m1.customernumber
    FROM (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m1
    WHERE 2 > (
        SELECT COUNT(*) FROM (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m2
        WHERE m1.num < m2.num
    )
);

-- Top 2 customers by order count (approach #2 — using CTE)
WITH corders AS (
    SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber
),
top2 AS (
    SELECT co1.customernumber FROM corders co1
    WHERE 2 > (SELECT COUNT(*) FROM corders co2 WHERE co1.num < co2.num)
)
SELECT c.customernumber, c.customername
FROM customers c, top2 t2
WHERE c.customernumber = t2.customernumber;
```

> **Note:** `ORDER BY ... LIMIT 2` is NOT a correlated query — it simply sorts and truncates results.

---

## 8. ALL / ANY

Use `>=ALL` / `<=ALL` / `>ANY` / `<ANY` to compare a value against a **set** returned by a subquery.

| Operator | Meaning |
|----------|---------|
| `>= ALL(set)` | Greater than or equal to **every** value in the set → the maximum |
| `<= ALL(set)` | Less than or equal to **every** value in the set → the minimum |
| `> ANY(set)`  | Greater than **at least one** value in the set → not the minimum |
| `< ANY(set)`  | Less than **at least one** value in the set → not the maximum |

```sql
-- Customer who paid the HIGHEST price for 'S18_3136' (>= ALL = max)
-- #1
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    >= ALL (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136');

-- #2 (equivalent using MAX)
SELECT c.customernumber, c.customername FROM customers c
WHERE c.customernumber = (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND productcode   = 'S18_3136'
      AND od.priceeach  = (SELECT MAX(priceeach) FROM orderdetails WHERE productcode = 'S18_3136')
);

-- Customers who did NOT pay the LOWEST price for 'S18_3136' (> ANY = not the min)
-- #1
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    > ANY (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136');

-- #2 (equivalent using <> MIN)
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    <> (SELECT MIN(priceeach) FROM orderdetails WHERE productcode = 'S18_3136');
```

**When to use:**
- `>= ALL` → find the row(s) with the maximum value
- `<= ALL` → find the row(s) with the minimum value
- `> ANY`  → exclude the minimum (anything not the smallest)
- `< ANY`  → exclude the maximum (anything not the largest)

---

## 9. EXISTS / NOT EXISTS

`EXISTS` returns TRUE if the subquery returns **at least one row**. It is always correlated — the subquery references the outer query.

| Combination | Meaning |
|-------------|---------|
| `WHERE EXISTS (...)` | Row qualifies if the subquery finds a match |
| `WHERE NOT EXISTS (...)` | Row qualifies if the subquery finds NO match |

```sql
-- EXISTS: customers who ordered 'S18_3136'
SELECT c.customernumber, c.customername FROM customers c
WHERE EXISTS (
    SELECT * FROM orders o, orderdetails od
    WHERE o.ordernumber    = od.ordernumber
      AND o.customernumber = c.customernumber
      AND od.productcode   = 'S18_3136'
);

-- NOT EXISTS: customers who have NOT placed any order
SELECT customernumber, customername FROM customers c
WHERE NOT EXISTS (
    SELECT * FROM orders o WHERE o.customernumber = c.customernumber
);

-- EXISTS + NOT EXISTS: customers who ordered A but NOT B
SELECT c.customernumber, c.customername FROM customers c
WHERE EXISTS (
    SELECT * FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND o.customernumber = c.customernumber AND od.productcode = 'S24_2840'
)
AND NOT EXISTS (
    SELECT * FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND o.customernumber = c.customernumber AND od.productcode = 'S50_1341'
);
```

---

## 10. Subqueries in SELECT and FROM

### Subquery in SELECT (scalar subquery)
Returns a single value per row of the outer query. Evaluated once per outer row (correlated).

```sql
-- Show each product with its order count
SELECT p.productname,
       (SELECT COUNT(*) FROM orderdetails od WHERE od.productcode = p.productcode) AS order_count
FROM products p;

-- Show each customer with total amount paid
SELECT c.customername,
       (SELECT SUM(amount) FROM payments pa WHERE pa.customernumber = c.customernumber) AS total_paid
FROM customers c;
```

### Subquery in FROM (derived table / inline view)
Treated as a temporary table; must be aliased. Evaluated once (non-correlated).

```sql
-- Wine: products with highest available_quantity in their type
SELECT p.prodname, p.prodtype, p.available_quantity
FROM product p,
    (SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
     FROM product GROUP BY prodtype) AS pm
WHERE p.prodtype = pm.prodtype
  AND p.available_quantity = pm.max_ava_quantity;

-- Top 2 customers (using derived tables)
SELECT customernumber, customername FROM customers
WHERE customernumber IN (
    SELECT m1.customernumber
    FROM (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m1
    WHERE 2 > (
        SELECT COUNT(*) FROM
            (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m2
        WHERE m1.num < m2.num
    )
);
```

---

## 11. Set Operations

MySQL supports `UNION` and `UNION ALL`. `INTERSECT` and `EXCEPT` are **not supported** in MySQL — use alternatives.

| Operation | Description | MySQL support |
|-----------|-------------|---------------|
| `UNION` | All rows from both, **removes duplicates** | Yes |
| `UNION ALL` | All rows from both, **keeps duplicates** | Yes |
| `INTERSECT` | Rows in **both** results | No — use JOIN or IN |
| `EXCEPT` | Rows in first but **not** second | No — use NOT IN or NOT EXISTS |

### UNION
```sql
-- Customers in 'Boston' OR who ordered 'S18_3136'
SELECT customernumber, customername FROM customers WHERE city = 'boston'
UNION
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136';
```

### INTERSECT alternative (AND / IN / JOIN)
```sql
-- Customers in 'Boston' AND who ordered 'S18_3136'
-- #1: direct join
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND c.city = 'boston'
  AND od.productcode   = 'S18_3136';

-- #2: nested IN
SELECT customernumber, customername FROM customers
WHERE city = 'boston'
  AND customernumber IN (
      SELECT c.customernumber FROM customers c, orders o, orderdetails od
      WHERE c.customernumber = o.customernumber
        AND o.ordernumber    = od.ordernumber
        AND od.productcode   = 'S18_3136'
  );
```

### EXCEPT alternative (NOT IN / NOT EXISTS)
```sql
-- Customers who have NOT ordered any product
SELECT customernumber, customername FROM customers
WHERE customernumber NOT IN (SELECT customernumber FROM orders);

-- Equivalent with NOT EXISTS
SELECT customernumber, customername FROM customers c
WHERE NOT EXISTS (SELECT * FROM orders o WHERE o.customernumber = c.customernumber);
```

---

## 12. Common Table Expressions (CTEs) and Temporary Tables

### CTEs — `WITH` clause
A CTE defines a named result set scoped to a single query. Preferred over deeply nested subqueries for readability.

```sql
-- Wine: most expensive wine per product type
WITH tp AS (
    SELECT p.prodtype, MAX(s.purchase_price) AS max_price
    FROM product p JOIN supplies s ON p.prodnr = s.prodnr
    GROUP BY p.prodtype
)
SELECT p.prodtype, p.prodnr, p.prodname
FROM product p, tp t, supplies s
WHERE p.prodtype  = t.prodtype
  AND p.prodnr    = s.prodnr
  AND s.purchase_price = t.max_price;

-- Wine: most popular product type per month
WITH mquan AS (
    SELECT MONTH(po.podate) AS month, p.prodtype AS product_type, COUNT(pol.quantity) AS total_quantity
    FROM purchase_order po, product p, po_line pol
    WHERE pol.prodnr = p.prodnr AND po.ponr = pol.ponr
    GROUP BY MONTH(po.podate), p.prodtype
),
maxquan AS (
    SELECT month, MAX(total_quantity) AS max_quantity FROM mquan GROUP BY month
)
SELECT m.month, m.product_type, m.total_quantity
FROM maxquan ma JOIN mquan m ON ma.month = m.month
WHERE m.total_quantity = ma.max_quantity;

-- Wine: products with highest available_quantity per type (CTE version)
WITH ptm AS (
    SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
    FROM product GROUP BY prodtype
)
SELECT p.prodnr, p.prodname, p.prodtype, p.available_quantity
FROM product p JOIN ptm ON p.prodtype = ptm.prodtype
WHERE p.available_quantity = ptm.max_ava_quantity;

-- Top 2 customers (CTE version)
WITH corders AS (
    SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber
),
top2 AS (
    SELECT co1.customernumber FROM corders co1
    WHERE 2 > (SELECT COUNT(*) FROM corders co2 WHERE co1.num < co2.num)
)
SELECT c.customernumber, c.customername
FROM customers c, top2 t2
WHERE c.customernumber = t2.customernumber;

-- Total orders by supplier city (CTE + LEFT JOIN)
WITH suporder AS (
    SELECT supnr, COUNT(*) AS totorder FROM purchase_order GROUP BY supnr
)
SELECT r.supcity, SUM(so.totorder) AS tot_order_by_city
FROM supplier r LEFT OUTER JOIN suporder so ON r.supnr = so.supnr
GROUP BY r.supcity
ORDER BY 2 DESC;
```

### Temporary Tables
Created for the session; dropped automatically when the session ends. Useful for multi-step computations.

```sql
-- Create and populate a temporary table
CREATE TEMPORARY TABLE temp_product_max AS
SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
FROM product GROUP BY prodtype;

-- Use the temporary table
SELECT p.prodname, p.prodtype, p.available_quantity
FROM product p JOIN temp_product_max t ON p.prodtype = t.prodtype
WHERE p.available_quantity = t.max_ava_quantity;

-- Drop manually if needed
DROP TEMPORARY TABLE IF EXISTS temp_product_max;
```

**When to use CTE vs Temp Table:**
- **CTE** — scoped to one query; cleaner syntax; evaluated each time it is referenced (in MySQL).
- **Temp Table** — persists across multiple queries in a session; can be indexed; better for large intermediate results reused multiple times.

---

## 13. RANK()

`RANK()` is a window function that assigns a rank to each row within a partition. Tied rows get the same rank; the next rank is skipped (gaps).

`DENSE_RANK()` — no gaps after ties.  
`ROW_NUMBER()` — unique sequential number regardless of ties.

```sql
-- Rank customers by number of orders
SELECT customernumber,
       COUNT(*) AS num_orders,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
FROM orders
GROUP BY customernumber;

-- Rank products by total quantity ordered, per product line
SELECT p.productline, p.productname,
       SUM(od.quantityordered) AS total_qty,
       RANK() OVER (PARTITION BY p.productline ORDER BY SUM(od.quantityordered) DESC) AS rnk
FROM products p JOIN orderdetails od ON p.productcode = od.productcode
GROUP BY p.productline, p.productname;

-- Top-ranked customer per product line (using CTE + RANK)
WITH ranked AS (
    SELECT p.productline, c.customername,
           SUM(od.quantityordered) AS total_qty,
           RANK() OVER (PARTITION BY p.productline ORDER BY SUM(od.quantityordered) DESC) AS rnk
    FROM customers c
    JOIN orders o ON c.customernumber = o.customernumber
    JOIN orderdetails od ON o.ordernumber = od.ordernumber
    JOIN products p ON od.productcode = p.productcode
    GROUP BY p.productline, c.customername
)
SELECT productline, customername, total_qty
FROM ranked WHERE rnk = 1;
```

---

## 14. Triggers and Stored Procedures

### Stored Procedure
A named, reusable block of SQL stored on the server.

```sql
DELIMITER $$

CREATE PROCEDURE GetCustomerOrders(IN cust_num INT)
BEGIN
    SELECT o.ordernumber, o.orderdate, o.status
    FROM orders o
    WHERE o.customernumber = cust_num;
END$$

DELIMITER ;

-- Call it
CALL GetCustomerOrders(103);
```

### Trigger
Automatically executes when a specified DML event occurs on a table.

```sql
DELIMITER $$

-- BEFORE INSERT trigger: set default status if missing
CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.status IS NULL THEN
        SET NEW.status = 'In Process';
    END IF;
END$$

-- AFTER UPDATE trigger: log price changes
CREATE TRIGGER after_price_update
AFTER UPDATE ON orderdetails
FOR EACH ROW
BEGIN
    IF NEW.priceeach <> OLD.priceeach THEN
        INSERT INTO price_audit (productcode, old_price, new_price, changed_at)
        VALUES (NEW.productcode, OLD.priceeach, NEW.priceeach, NOW());
    END IF;
END$$

DELIMITER ;
```

**Trigger timing options:**
- `BEFORE INSERT`, `AFTER INSERT`
- `BEFORE UPDATE`, `AFTER UPDATE`
- `BEFORE DELETE`, `AFTER DELETE`

---

## 15. Recursive Queries

MySQL supports recursive CTEs (MySQL 8.0+) using `WITH RECURSIVE`.

```sql
-- Recursive CTE: employee hierarchy (who reports to whom)
WITH RECURSIVE emp_hierarchy AS (
    -- Base case: top-level employees (no manager)
    SELECT employeeNumber, firstName, lastName, reportsTo, 1 AS level
    FROM employees
    WHERE reportsTo IS NULL

    UNION ALL

    -- Recursive case: employees reporting to someone already in the CTE
    SELECT e.employeeNumber, e.firstName, e.lastName, e.reportsTo, h.level + 1
    FROM employees e
    JOIN emp_hierarchy h ON e.reportsTo = h.employeeNumber
)
SELECT * FROM emp_hierarchy ORDER BY level, employeeNumber;

-- Recursive CTE: number series 1 to 10
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums;
```

---

## 16. Conceptual Questions

### When must aggregation be used together with GROUP BY / HAVING?

Use `GROUP BY` whenever you want aggregate values **per group** rather than across the entire table.

- If `SELECT` contains both an aggregate function and a non-aggregate column, those non-aggregate columns **must** appear in `GROUP BY`.
- `HAVING` is required when you want to filter based on an aggregate result (e.g., `HAVING COUNT(*) > 5`). You cannot use aggregate functions in `WHERE`.

```
WHERE  → filters individual rows   (before grouping)
HAVING → filters groups            (after grouping, on aggregate results)
```

### What is the difference between INNER JOIN and OUTER JOIN?

| | INNER JOIN | OUTER JOIN |
|-|-----------|-----------|
| Matched rows | Included | Included |
| Unmatched rows | **Excluded** | **Included** (NULLs fill missing side) |
| Use case | Only related data needed | Must keep all rows from one/both tables |

### What is the difference between a nested and a correlated query?

| | Nested (Non-correlated) | Correlated |
|-|------------------------|------------|
| References outer query? | No | Yes |
| Evaluated | Once, then result used | Once per row of outer query |
| Performance | Generally faster | Slower (re-runs per outer row) |
| Example | `WHERE id IN (SELECT id FROM ...)` | `WHERE EXISTS (SELECT * FROM ... WHERE outer.col = inner.col)` |

### When to use >=ALL, <=ALL, >ANY, <ANY?

| Operator | Equivalent to | Use when you want |
|----------|--------------|------------------|
| `>= ALL(set)` | `>= MAX(set)` | The maximum value |
| `<= ALL(set)` | `<= MIN(set)` | The minimum value |
| `> ANY(set)`  | `> MIN(set)` | Anything greater than the smallest (not the minimum) |
| `< ANY(set)`  | `< MAX(set)` | Anything less than the largest (not the maximum) |

### Differences between EXISTS / NOT EXISTS combinations?

| Pattern | Returns rows where... |
|---------|----------------------|
| `WHERE EXISTS (subq)` | Subquery finds at least one match → include the outer row |
| `WHERE NOT EXISTS (subq)` | Subquery finds no match → include the outer row |
| `EXISTS(A) AND NOT EXISTS(B)` | Matches A but does not match B |
| `NOT EXISTS(A) AND NOT EXISTS(B)` | Matches neither A nor B |
| `NOT EXISTS(A) OR NOT EXISTS(B)` | Does not match A, or does not match B (or both) |

### How do subqueries in SELECT and FROM work?

- **Subquery in SELECT:** Returns exactly one value (scalar) per outer row. It runs once per outer row (correlated). Must return a single column and a single row per evaluation.
- **Subquery in FROM:** Returns a full result set used as a temporary/derived table. Must be aliased. Evaluated once. Cannot reference outer query columns.

### When and how to use set operators?

Use set operators when combining results from two queries with the **same number and compatible column types**.

| Operator | Use when | MySQL |
|----------|----------|-------|
| `UNION` | Combining results with duplicate removal | Yes |
| `UNION ALL` | Combining results keeping duplicates | Yes |
| `INTERSECT` | Rows common to both queries | No → use `IN` / `JOIN` |
| `EXCEPT` | Rows in first not in second | No → use `NOT IN` / `NOT EXISTS` |

**Equivalents:**
- `A UNION B` → rows in A, or B, or both (no duplicates)
- `A INTERSECT B` → `WHERE id IN (SELECT id FROM B)`
- `A EXCEPT B` → `WHERE id NOT IN (SELECT id FROM B)`

### How to debug a SQL query?

1. **Read the error message** — MySQL error messages name the exact clause and line.
2. **Simplify** — comment out JOINs, WHERE conditions, and HAVING one at a time to find where results break.
3. **Check column references** — ensure all non-aggregate columns in SELECT appear in GROUP BY.
4. **Check join conditions** — a missing ON/WHERE condition causes a Cartesian product.
5. **Check aliases** — ensure table aliases are consistent throughout.
6. **Test subqueries independently** — run each subquery alone first to verify it returns expected results.
7. **Use EXPLAIN** — `EXPLAIN SELECT ...` shows the execution plan and identifies missing indexes or full scans.
8. **Check NULL handling** — `= NULL` is always false; use `IS NULL` / `IS NOT NULL`.
9. **Check aggregate vs WHERE** — aggregate conditions belong in HAVING, not WHERE.

### How to interpret a SQL query?

Work clause by clause in execution order:
1. `FROM` — identify all tables (and joins) involved.
2. `WHERE` — identify which rows are kept.
3. `GROUP BY` — identify how rows are grouped.
4. `HAVING` — identify which groups are kept.
5. `SELECT` — identify what is returned.
6. `ORDER BY` — identify the sort order.

### How to complete an incomplete SQL query?

1. Identify what the question asks for (the *what*).
2. Identify which tables hold that data (the *from*).
3. Identify the join conditions linking tables.
4. Identify any filters (the *where*).
5. Identify whether grouping or aggregation is needed.
6. Check whether a correlated subquery, ALL/ANY, or EXISTS is required based on the type of comparison.

### How to write a SQL query for desired information?

1. **Identify output columns** → these go in `SELECT`.
2. **Identify all required tables** → these go in `FROM`.
3. **Write join conditions** → link primary/foreign keys in `WHERE` or `ON`.
4. **Add filter conditions** → add to `WHERE`.
5. **Check if aggregation needed** → add `GROUP BY` and `HAVING`.
6. **Check if correlated or ALL/ANY/EXISTS needed** → for "best", "highest", "not in", "at least one" type conditions.
7. **Add ORDER BY** if a sort order is required.

---

## 17. Practice Queries — All Three Schemas

### classicmodels — All Solutions

```sql
-- Q1: total customers from NYC
SELECT COUNT(*) FROM customers WHERE city = 'NYC';

-- Q2: count non-NULL priceeach for product 'S24_3969'
SELECT COUNT(priceeach) FROM orderdetails WHERE productcode = 'S24_3969';

-- Q3: count distinct non-NULL priceeach for product 'S24_3969'
SELECT COUNT(DISTINCT priceeach) FROM orderdetails WHERE productcode = 'S24_3969';

-- Q4: productcode and sum of quantityordered for 'S24_2840'
SELECT productcode, SUM(quantityordered) AS total_quantity
FROM orderdetails WHERE productcode = 'S24_2840';

-- Q5: total quantityordered across all orderdetails
SELECT SUM(quantityordered) FROM orderdetails;

-- Q6: weighted average priceeach for 'S24_2840'
SELECT AVG(priceeach) AS weighted_avg_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- Q7: unweighted average priceeach for 'S24_2840'
SELECT AVG(DISTINCT priceeach) AS unweighted_avg_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- Q8: variance of priceeach for 'S24_2840'
SELECT VARIANCE(priceeach) AS variance_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- Q9: min and max priceeach for 'S24_2840'
SELECT MIN(priceeach) AS min_price, MAX(priceeach) AS max_price
FROM orderdetails WHERE productcode = 'S24_2840';

-- Q10: products with at least 25 orders
SELECT productcode FROM orderdetails
GROUP BY productcode
HAVING COUNT(*) >= 25;

-- Q11: products where total quantityordered > 1000
SELECT productcode, SUM(quantityordered) AS total_qty FROM orderdetails
GROUP BY productcode
HAVING SUM(quantityordered) > 1000;

-- Q12: orders sorted by date ASC, customernumber DESC
SELECT ordernumber FROM orders ORDER BY orderdate ASC, customernumber DESC;

-- Q13: productcode, ordernumber, priceeach for 'S24_2840', sorted by priceeach DESC
SELECT productcode, ordernumber, priceeach FROM orderdetails
WHERE productcode = 'S24_2840'
ORDER BY 3 DESC;

-- Q14: customer info with order details (inner join across 4 tables)
SELECT c.customernumber, c.customername, o.ordernumber, o.orderdate,
       p.productcode, p.productname, od.quantityordered
FROM customers c, orders o, orderdetails od, products p
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode;

-- Q15: pairs of customers in the same city (self join)
SELECT c1.customername, c2.customername, c1.city
FROM customers c1, customers c2
WHERE c1.city = c2.city AND c1.customernumber < c2.customernumber;

-- Q16: customers who ordered at least one 'planes' product
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od, products p
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode
  AND p.productline    = 'planes';

-- Q17: customername, productname, shippeddate, quantityordered for shipped orders
SELECT c.customername, p.productname, o.shippeddate, od.quantityordered
FROM customers c, orders o, orderdetails od, products p
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode
  AND o.status         = 'shipped';

-- Q18: productcode, productname, total quantityordered per product
SELECT od.productcode, p.productname, SUM(quantityordered) AS totalquantity
FROM orderdetails od, products p
WHERE od.productcode = p.productcode
GROUP BY od.productcode;

-- Q19: all customers with their orders (LEFT OUTER JOIN — keeps customers without orders)
SELECT c.customernumber, c.customername, o.ordernumber
FROM customers AS c
LEFT OUTER JOIN orders AS o ON c.customernumber = o.customernumber;

-- Q20: all products with total quantityordered (RIGHT OUTER JOIN — keeps products without orders)
SELECT p.productcode, p.productname, SUM(od.quantityordered) AS total_qty
FROM orderdetails AS od
RIGHT OUTER JOIN products AS p ON od.productcode = p.productcode
GROUP BY p.productcode;

-- Q21: nested — customer name for order 10202
SELECT customername FROM customers
WHERE customernumber = (SELECT customernumber FROM orders WHERE ordernumber = '10202');

-- Q22: nested — customers who ordered 'S24_2840'
-- #1
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT customernumber FROM orders WHERE ordernumber IN (
        SELECT ordernumber FROM orderdetails WHERE productcode = 'S24_2840'
    )
);
-- #2
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S24_2840'
);

-- Q23: customers who ordered BOTH 'S24_2840' AND 'S50_1341'
-- #1
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT customernumber FROM orders WHERE ordernumber IN (
        SELECT ordernumber FROM orderdetails WHERE productcode = 'S24_2840'
    )
)
AND customernumber IN (
    SELECT customernumber FROM orders WHERE ordernumber IN (
        SELECT ordernumber FROM orderdetails WHERE productcode = 'S50_1341'
    )
);
-- #2
SELECT customername FROM customers
WHERE customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S24_2840'
)
AND customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber AND od.productcode = 'S50_1341'
);

-- Q24: correlated — products with at least 5 orders
SELECT p.productname FROM products p
WHERE (SELECT COUNT(*) FROM orderdetails od WHERE od.productcode = p.productcode) >= 5;

-- Q25: correlated — customers who ordered a product below its average price
SELECT c.customernumber, c.customername, p.productcode, p.productname,
       od.priceeach, od.quantityordered
FROM customers c, products p, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = p.productcode
  AND od.priceeach < (SELECT AVG(priceeach) FROM orderdetails WHERE productcode = p.productcode);

-- Q26: correlated — top 2 customers by number of orders
-- #1 straightforward
SELECT customernumber, customername FROM customers
WHERE customernumber IN (
    SELECT m1.customernumber
    FROM (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m1
    WHERE 2 > (
        SELECT COUNT(*) FROM
            (SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber) AS m2
        WHERE m1.num < m2.num
    )
);
-- #2 CTE
WITH corders AS (
    SELECT customernumber, COUNT(*) AS num FROM orders GROUP BY customernumber
),
top2 AS (
    SELECT co1.customernumber FROM corders co1
    WHERE 2 > (SELECT COUNT(*) FROM corders co2 WHERE co1.num < co2.num)
)
SELECT c.customernumber, c.customername
FROM customers c, top2 t2
WHERE c.customernumber = t2.customernumber;

-- Q27: customer who ordered 'S18_3136' at the highest price (>= ALL)
-- #1
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    >= ALL (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136');
-- #2
SELECT c.customernumber, c.customername FROM customers c
WHERE c.customernumber = (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND productcode = 'S18_3136'
      AND od.priceeach >= ALL (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136')
);
-- #3 (using MAX)
SELECT c.customernumber, c.customername FROM customers c
WHERE c.customernumber = (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND productcode = 'S18_3136'
      AND od.priceeach = (SELECT MAX(priceeach) FROM orderdetails WHERE productcode = 'S18_3136')
);

-- Q28: customers who ordered 'S18_3136' but NOT at the lowest price (> ANY)
-- #1
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    > ANY (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136');
-- #2
SELECT c.customernumber, c.customername FROM customers c
WHERE c.customernumber IN (
    SELECT o.customernumber FROM orders o, orderdetails od
    WHERE o.ordernumber = od.ordernumber
      AND productcode = 'S18_3136'
      AND od.priceeach > ANY (SELECT priceeach FROM orderdetails WHERE productcode = 'S18_3136')
);
-- #3 (using <> MIN)
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136'
  AND od.priceeach    <> (SELECT MIN(priceeach) FROM orderdetails WHERE productcode = 'S18_3136');

-- Q29: EXISTS — customers who ordered 'S18_3136'
SELECT c.customernumber, c.customername FROM customers c
WHERE EXISTS (
    SELECT * FROM orders o, orderdetails od
    WHERE o.ordernumber    = od.ordernumber
      AND o.customernumber = c.customernumber
      AND od.productcode   = 'S18_3136'
);

-- Q30: UNION — customers in 'Boston' OR who ordered 'S18_3136'
SELECT customernumber, customername FROM customers WHERE city = 'boston'
UNION
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND od.productcode   = 'S18_3136';

-- Q31: INTERSECT alternative — customers in 'Boston' AND who ordered 'S18_3136'
-- #1
SELECT c.customernumber, c.customername
FROM customers c, orders o, orderdetails od
WHERE c.customernumber = o.customernumber
  AND o.ordernumber    = od.ordernumber
  AND c.city = 'boston'
  AND od.productcode   = 'S18_3136';
-- #2
SELECT customernumber, customername FROM customers
WHERE city = 'boston'
  AND customernumber IN (
      SELECT c.customernumber FROM customers c, orders o, orderdetails od
      WHERE c.customernumber = o.customernumber
        AND o.ordernumber    = od.ordernumber
        AND od.productcode   = 'S18_3136'
  );

-- Q32: EXCEPT alternative — customers who have NOT ordered any product
SELECT customernumber, customername FROM customers
WHERE customernumber NOT IN (SELECT customernumber FROM orders);
```

### world — All Solutions

```sql
-- Q1: everything in country
SELECT * FROM country;

-- Q2: code and name
SELECT code, name FROM country;

-- Q3: countrycode from city
SELECT countrycode FROM city;

-- Q4: distinct countrycode
SELECT DISTINCT countrycode FROM city;

-- Q5: name, countrycode, population in thousands
SELECT name, countrycode, population / 1000 FROM city;

-- Q6: US cities
SELECT id, name, population FROM city WHERE countrycode = 'USA';

-- Q7: Indian cities with population > 1,000,000
SELECT id, name, population FROM city WHERE countrycode = 'IND' AND population > 1000000;

-- Q8: cities with population between 1M and 10M
SELECT id, name, population FROM city WHERE population BETWEEN 1000000 AND 10000000;

-- Q9: countries in Asia or Africa
SELECT code, name FROM country WHERE continent IN ('Asia', 'Africa');

-- Q10: countries with GovernmentForm containing 'Republic'
SELECT code, name FROM country WHERE governmentform LIKE '%republic%';

-- Q11: countries where IndepYear is NULL
SELECT code, name FROM country WHERE indepyear IS NULL;

-- Q12: count of 'Republic' countries
SELECT COUNT(*) FROM country WHERE governmentform = 'Republic';

-- Q13: count of region values (non-null)
SELECT COUNT(region) FROM country WHERE governmentform = 'Republic';

-- Q14: count of distinct regions
SELECT COUNT(DISTINCT region) FROM country WHERE governmentform = 'Republic';

-- Q15/16: total GNP for 'Republic' countries
SELECT SUM(GNP) FROM country WHERE governmentform = 'Republic';

-- Q17: weighted average GNP
SELECT AVG(GNP) AS weighted_average_GNP FROM country WHERE governmentform = 'Republic';

-- Q18: unweighted average GNP
SELECT AVG(DISTINCT GNP) AS unweighted_average_GNP FROM country WHERE governmentform = 'Republic';

-- Q19: variance of GNP
SELECT VARIANCE(GNP) AS variance_GNP FROM country WHERE governmentform = 'Republic';

-- Q20: min and max GNP
SELECT MIN(GNP) AS min_GNP, MAX(GNP) AS max_GNP FROM country WHERE governmentform = 'Republic';

-- Q21: countries with at least 3 cities
SELECT countrycode FROM city
GROUP BY countrycode
HAVING COUNT(*) > 2;

-- Q22: countries whose total city population > 100,000,000
SELECT countrycode FROM city
GROUP BY countrycode
HAVING SUM(population) > 100000000;

-- Q23: countries ordered by SurfaceArea DESC, IndepYear ASC
SELECT code, name, surfacearea, indepyear FROM country
ORDER BY surfacearea DESC, indepyear ASC;

-- Q24: countries ordered by column position 2 (name)
SELECT code, name, surfacearea, indepyear FROM country
ORDER BY 2;
```

### wine purchase order — All Solutions

```sql
-- W1: highest available_quantity per product type, sorted descending
SELECT prodtype, MAX(available_quantity) AS highest_quantity
FROM product
GROUP BY prodtype
ORDER BY highest_quantity DESC;

-- W2: products with highest available_quantity within their type
-- #1: subquery
SELECT p.prodname, p.prodtype, p.available_quantity
FROM product p,
    (SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
     FROM product GROUP BY prodtype) AS pm
WHERE p.prodtype = pm.prodtype AND p.available_quantity = pm.max_ava_quantity;

-- #2: CTE
WITH ptm AS (
    SELECT prodtype, MAX(available_quantity) AS max_ava_quantity
    FROM product GROUP BY prodtype
)
SELECT p.prodnr, p.prodname, p.prodtype, p.available_quantity
FROM product p JOIN ptm ON p.prodtype = ptm.prodtype
WHERE p.available_quantity = ptm.max_ava_quantity;

-- W3: highest purchase price per product type
SELECT p.prodtype, MAX(s.purchase_price)
FROM product p, supplies s
WHERE p.prodnr = s.prodnr
GROUP BY p.prodtype;

-- W4: most expensive wines per product type
WITH tp AS (
    SELECT p.prodtype, MAX(s.purchase_price) AS max_price
    FROM product p JOIN supplies s ON p.prodnr = s.prodnr
    GROUP BY p.prodtype
)
SELECT p.prodtype, p.prodnr, p.prodname
FROM product p, tp t, supplies s
WHERE p.prodtype = t.prodtype AND p.prodnr = s.prodnr AND s.purchase_price = t.max_price;

-- W5: total quantity ordered per product type
SELECT p.prodtype, SUM(pol.quantity) AS total_quantity
FROM product p, purchase_order po, po_line pol
WHERE p.prodnr = pol.prodnr AND pol.ponr = po.ponr
GROUP BY p.prodtype;

-- W6: most popular product type (most quantity ordered) per month
WITH mquan AS (
    SELECT MONTH(po.podate) AS month, p.prodtype AS product_type, COUNT(pol.quantity) AS total_quantity
    FROM purchase_order po, product p, po_line pol
    WHERE pol.prodnr = p.prodnr AND po.ponr = pol.ponr
    GROUP BY MONTH(po.podate), p.prodtype
),
maxquan AS (
    SELECT month, MAX(total_quantity) AS max_quantity FROM mquan GROUP BY month
)
SELECT m.month, m.product_type, m.total_quantity
FROM maxquan ma JOIN mquan m ON ma.month = m.month
WHERE m.total_quantity = ma.max_quantity;

-- W7: total orders by supplier city (including cities with no orders)
WITH suporder AS (
    SELECT supnr, COUNT(*) AS totorder
    FROM purchase_order GROUP BY supnr
)
SELECT r.supcity, SUM(so.totorder) AS tot_order_by_city
FROM supplier r LEFT OUTER JOIN suporder so ON r.supnr = so.supnr
GROUP BY r.supcity
ORDER BY 2 DESC;
```
