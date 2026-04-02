# Chapter 7 Review Questions — Answers & Explanations

**Schema:**
- `SUPPLIER(SUPNR, SUPNAME, SUPADDRESS, SUPCITY, SUPSTATUS)`
- `PRODUCT(PRODNR, PRODNAME, PRODTYPE, AVAILABLE_QUANTITY)`
- `SUPPLIES(SUPNR, PRODNR, PURCHASE_PRICE, DELIV_PERIOD)`
- `PURCHASE_ORDER(PONR, PODATE, SUPNR)`
- `PO_LINE(PONR, PRODNR, QUANTITY)`

---

## Q7.1 — ON DELETE CASCADE ON UPDATE CASCADE

The following table with purchase orders is created:

```sql
CREATE TABLE PURCHASE_ORDER (
    PONR CHAR(7) NOT NULL PRIMARY KEY,
    PODATE DATE,
    SUPNR CHAR(4) NOT NULL,
    FOREIGN KEY (SUPNR) REFERENCES SUPPLIER (SUPNR)
        ON DELETE CASCADE ON UPDATE CASCADE
);
```

What happens upon deletion of a supplier?

- **a.** All purchase order records tied to that supplier are also deleted.
- **b.** The SUPNR of this supplier is replaced by a NULL value in PURCHASE_ORDER.
- **c.** The SUPNR of this supplier is deleted in PURCHASE_ORDER.
- **d.** The SUPNR of this supplier is only deleted in SUPPLIER.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | `ON DELETE CASCADE` automatically deletes all child rows in `PURCHASE_ORDER` that reference the deleted supplier. |
| b | ❌ Wrong | Setting SUPNR to NULL would be `ON DELETE SET NULL` behavior. |
| c | ❌ Wrong | Deleting only the SUPNR column value is not valid; cascade deletes the entire child row. |
| d | ❌ Wrong | Only deleting from SUPPLIER would be the default `RESTRICT`/`NO ACTION` behavior (which would error or block the delete). |

---

## Q7.2 — Pattern match for supplier names containing "wine"

We're interested in wine stores. We want to retrieve the SUPNR and SUPNAME of each store which contains "wine" in its store name. Which of the following queries can we use?

- **a.**
```sql
SELECT SUPNR, SUPNAME FROM SUPPLIER
WHERE SUPNAME = "WINE"
```
- **b.**
```sql
SELECT SUPNR, SUPNAME FROM SUPPLIER
WHERE SUPNAME IS "%WINE%"
```
- **c.**
```sql
SELECT SUPNR, SUPNAME FROM SUPPLIER
WHERE SUPNAME LIKE "%WINE%"
```
- **d.**
```sql
SELECT SUPNR, SUPNAME FROM SUPPLIER
WHERE SUPNAME IS "WINE"
```

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | `=` performs exact equality. Only matches a supplier named exactly "WINE". |
| b | ❌ Wrong | `IS` is reserved for NULL checks (`IS NULL`/`IS NOT NULL`), not string pattern matching. Syntax is invalid. |
| c | ✅ Correct | `LIKE '%WINE%'` uses `%` wildcards to match any name containing "wine" anywhere in the string. |
| d | ❌ Wrong | `IS "WINE"` is syntactically invalid; `IS` is only valid with NULL. |

---

## Q7.3 — Fastest delivery time for product 0185

Take the following extract from SUPPLIES:

| SUPNR | PRODNR | PURCHASE_PRICE | DELIV_PERIOD |
|-------|--------|----------------|--------------|
| 37    | 0185   | 32.99          | 3            |
| 84    | 0185   | 33.00          | 5            |
| 94    | 0185   | 32.99          | 1            |

We want to retrieve the fastest delivery time for product 0185. We type the following query:

```sql
SELECT PRODNR, MIN(DELIV_PERIOD) AS MIN_DELIV_PERIOD
FROM SUPPLIES
WHERE PRODNR = '0185'
```

What are the results? If you believe the query is correct, select answer **a**, otherwise choose which results you believe will be retrieved.

- **a.** The query is correct → one row: `PRODNR=0185, MIN_DELIV_PERIOD=1`
- **b.** One row: `PRODNR=0185, MIN_DELIV_PERIOD=3` (from SUPNR 37)
- **c.** One row: `PRODNR=0185, MIN_DELIV_PERIOD=1` but associated with SUPNR=37 (wrong row)
- **d.** Three rows: SUPNR 37, 84, 94 each with MIN_DELIV_PERIOD=1

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | The query is valid. `WHERE PRODNR='0185'` means all rows share the same PRODNR (unambiguous non-aggregate). `MIN(3,5,1) = 1`. One row is returned. |
| b | ❌ Wrong | Shows `DELIV_PERIOD=3` (SUPNR 37's value), not the minimum. |
| c | ❌ Wrong | MIN value is correct (1) but incorrectly associates it with the wrong row. |
| d | ❌ Wrong | Three rows would appear only without aggregation or with `GROUP BY SUPNR` — neither is in the query. |

---

## Q7.4 — ORDER BY AVAILABLE_QUANTITY DESC, PRODNAME

Consider the following query:

```sql
SELECT * FROM PRODUCT
WHERE PRODTYPE = 'red'
ORDER BY AVAILABLE_QUANTITY DESC, PRODNAME
```

Which of the following answers is **correct**?

- **a.** Result sorted by AVAILABLE_QUANTITY descending; ties broken alphabetically by PRODNAME ascending.
  *(e.g., for qty=147: "Chateau De La Tour…" before "Chateau Margaux…"; rows with qty=3 and qty=0 at bottom)*
- **b.** Result sorted by AVAILABLE_QUANTITY descending but ties broken with PRODNAME descending.
  *(e.g., "Chateau Margaux…" before "Chateau De La Tour…" at same qty)*
- **c.** Result sorted by AVAILABLE_QUANTITY **ascending** (lowest first).
  *(e.g., qty=0 row appears first)*
- **d.** A different subset of red wine products shown, not correctly matching the full red wine catalog.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | `ORDER BY AVAILABLE_QUANTITY DESC` puts highest qty first. For ties (qty=147), secondary sort `PRODNAME` ascending means 'D' (De La Tour) < 'M' (Margaux) — correct alphabetical order. |
| b | ❌ Wrong | Incorrect secondary sort — "Chateau Margaux" before "Chateau De La Tour" violates ascending PRODNAME. |
| c | ❌ Wrong | Starts from the lowest quantity, violating `DESC`. |
| d | ❌ Wrong | Shows a different/incomplete product set — does not match the correct sort of all red wines. |

---

## Q7.5 — Unique supplier numbers and statuses with at least one purchase order

We want to retrieve all unique supplier numbers and statuses of suppliers who have at least one outstanding purchase order. Which query is **correct**?

- **a.**
```sql
SELECT DISTINCT R.SUPNR, R.SUPSTATUS
FROM SUPPLIER R, PURCHASE_ORDER O
WHERE (R.SUPNR = O.SUPNR)
```
- **b.**
```sql
SELECT DISTINCT R.SUPNR, R.SUPSTATUS
FROM SUPPLIER R, PURCHASE_ORDER O
WHERE (R.SUPNR = O.SUPNR)
```
*(identical to a but without DISTINCT in some versions)*
- **c.**
```sql
SELECT DISTINCT R.SUPNR, R.SUPSTATUS
FROM SUPPLIER R, PURCHASE_ORDER O
WHERE (R.SUPNR = O.PONR)
```
- **d.**
```sql
SELECT R.SUPNR, R.SUPSTATUS
FROM PURCHASE_ORDER R
```

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | Joins `SUPPLIER` and `PURCHASE_ORDER` on `SUPNR`. `DISTINCT` removes duplicates for suppliers with multiple orders. Correctly retrieves unique suppliers with at least one order. |
| b | ❌ Wrong | Missing `DISTINCT` — suppliers with multiple purchase orders appear multiple times in the result. |
| c | ❌ Wrong | `WHERE R.SUPNR = O.PONR` joins supplier number with purchase order number — semantically wrong (different domains). |
| d | ❌ Wrong | Selects from `PURCHASE_ORDER` only; `SUPSTATUS` does not exist in that table — query fails. |

---

## Q7.6 — LEFT OUTER JOIN + GROUP BY — which statement is NOT correct?

Consider the following query:

```sql
SELECT P.PRODNR, P.PRODNAME, P.AVAILABLE_QUANTITY, SUM(L.QUANTITY) AS ORDERED_QUANTITY
FROM PRODUCT AS P LEFT OUTER JOIN PO_LINE AS L ON (P.PRODNR = L.PRODNR)
GROUP BY P.PRODNR
```

Which of the following statements is **not correct**?

- **a.** The query retrieves the product number, product name, and available quantity of each product thanks to the left outer join.
- **b.** The query retrieves for each product the total ordered quantity.
- **c.** The query result can never contain NULL values.
- **d.** If we remove the GROUP BY statement and P.PRODNR, P.PRODNAME, P.AVAILABLE_QUANTITY from the SELECT statement, the query will result in one row containing the total outstanding ordered quantity over all products in column "ORDERED_QUANTITY".

**✅ Answer: c** — Statement c is NOT correct.

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | The `LEFT OUTER JOIN` ensures all products are returned even if they have no matching `PO_LINE` rows. |
| b | ✅ Correct | `SUM(L.QUANTITY)` grouped by product gives the total ordered quantity per product. |
| c | ❌ NOT Correct (answer) | Products with no purchase orders produce no `PO_LINE` match. The LEFT JOIN returns NULL for `L.QUANTITY`, making `SUM(NULL) = NULL`. The result **can** contain NULL values in `ORDERED_QUANTITY`. |
| d | ✅ Correct | Without `GROUP BY` and non-aggregate columns, the query collapses to a single row with the grand total ordered quantity across all products. |

---

## Q7.7 — Products supplied by more than one supplier

Consider the following query:

```sql
SELECT DISTINCT P1.PRODNR, P1.PRODNAME
FROM PRODUCT P1, SUPPLIES S1
WHERE P1.PRODNR = S1.PRODNR
  AND 1 <= (SELECT COUNT(*) FROM SUPPLIES S2
            WHERE S2.SUPNR <> S1.SUPNR AND P1.PRODNR = S2.PRODNR)
ORDER BY PRODNR
```

The query retrieves:

- **a.** The number and name of all products that can only be supplied by one supplier.
- **b.** The number and name of all products that cannot be supplied by any supplier.
- **c.** The number and name of all products that can be supplied by more than one supplier.
- **d.** The number and name of all products that can be supplied by all suppliers.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Single-supplier products have COUNT = 0 (no other supplier exists for them), so `1 <= 0` is false — they are excluded. |
| b | ❌ Wrong | The outer `WHERE P1.PRODNR = S1.PRODNR` ensures we only process products that ARE in `SUPPLIES` (have at least one supplier). |
| c | ✅ Correct | The subquery counts suppliers for the same product where `SUPNR ≠ S1.SUPNR`. `COUNT >= 1` means at least one additional supplier exists, so the product has 2+ suppliers. |
| d | ❌ Wrong | "Supplied by all suppliers" requires relational division (double `NOT EXISTS`), not a simple count of 1+. |

---

## Q7.8 — Maximum total quantity ordered

Which of the following queries selects the name of the supplier, corresponding order number, and total ordered quantity of the order that has the **maximum** total quantity ordered?

- **a.**
```sql
SELECT R1.SUPNAME, POL1.PONR, SUM(POL1.QUANTITY)
FROM SUPPLIER R1, PURCHASE_ORDER PO1, PO_LINE POL1
WHERE R1.SUPNR = PO1.SUPNR AND PO1.PONR = POL1.PONR
GROUP BY POL1.PONR
HAVING SUM(POL1.QUANTITY) >= ANY
    (SELECT SUM(POL2.QUANTITY) FROM SUPPLIER R2, PURCHASE_ORDER PO2, PO_LINE POL2
     WHERE R2.SUPNR = PO2.SUPNR AND PO2.PONR = POL2.PONR
     GROUP BY POL2.PONR)
```
- **b.**
```sql
SELECT R1.SUPNAME, POL1.PONR, SUM(POL1.QUANTITY)
FROM SUPPLIER R1, PURCHASE_ORDER PO1, PO_LINE POL1
WHERE R1.SUPNR = PO1.SUPNR AND PO1.PONR = POL1.PONR
GROUP BY POL1.PONR
HAVING SUM(POL1.QUANTITY) <= ALL
    (SELECT SUM(POL2.QUANTITY) FROM SUPPLIER R2, PURCHASE_ORDER PO2, PO_LINE POL2
     WHERE R2.SUPNR = PO2.SUPNR AND PO2.PONR = POL2.PONR
     GROUP BY POL2.PONR)
```
- **c.**
```sql
SELECT R1.SUPNAME, POL1.PONR, SUM(POL1.QUANTITY)
FROM SUPPLIER R1, PURCHASE_ORDER PO1, PO_LINE POL1
WHERE R1.SUPNR = PO1.SUPNR AND PO1.PONR = POL1.PONR
GROUP BY POL1.PONR
HAVING SUM(POL1.QUANTITY) >= ALL
    (SELECT SUM(POL2.QUANTITY) FROM SUPPLIER R2, PURCHASE_ORDER PO2, PO_LINE POL2
     WHERE R2.SUPNR = PO2.SUPNR AND PO2.PONR = POL2.PONR
     GROUP BY POL2.PONR)
```
- **d.**
```sql
SELECT R1.SUPNAME, POL1.PONR, SUM(POL1.QUANTITY)
FROM SUPPLIER R1, PURCHASE_ORDER PO1, PO_LINE POL1
WHERE R1.SUPNR = PO1.SUPNR AND PO1.PONR = POL1.PONR
GROUP BY POL1.PONR
HAVING SUM(POL1.QUANTITY) <= ANY
    (SELECT SUM(POL2.QUANTITY) FROM SUPPLIER R2, PURCHASE_ORDER PO2, PO_LINE POL2
     WHERE R2.SUPNR = PO2.SUPNR AND PO2.PONR = POL2.PONR
     GROUP BY POL2.PONR)
```

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | `>= ANY` means "at least as large as at least one value." Returns all orders except the one with the absolute minimum — not just the maximum. |
| b | ❌ Wrong | `<= ALL` means "less than or equal to all values" → finds the **minimum** total, not the maximum. |
| c | ✅ Correct | `>= ALL` means "greater than or equal to every other total" → only the maximum order(s) satisfy this condition. |
| d | ❌ Wrong | `<= ANY` returns all orders except the absolute maximum — the opposite of what's needed. |

---

## Q7.9 — Double NOT EXISTS / EXISTS

Consider the following query:

```sql
SELECT SUPNAME, SUPADDRESS, SUPCITY FROM SUPPLIER R
WHERE NOT EXISTS (
    SELECT * FROM PRODUCT P
    WHERE EXISTS (
        SELECT * FROM SUPPLIES S
        WHERE R.SUPNR = S.SUPNR AND P.PRODNR = S.PRODNR))
```

This query selects:

- **a.** The supplier name, supplier address, and supplier city of all suppliers who cannot supply any products.
- **b.** The supplier name, supplier address, and supplier city of all suppliers who cannot supply all products.
- **c.** The supplier name, supplier address, and supplier city of all suppliers who can supply at least one product.
- **d.** The supplier name, supplier address, and supplier city of all suppliers who can supply all products.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | The inner `EXISTS` checks "does supplier R supply product P?" The outer `NOT EXISTS` negates it over all products → "there is NO product that R supplies" = R supplies zero products. |
| b | ❌ Wrong | "Cannot supply all products" would require a divisor-style double `NOT EXISTS` query, not this structure. |
| c | ❌ Wrong | "At least one product" would use `EXISTS` without the outer `NOT EXISTS` — the exact opposite condition. |
| d | ❌ Wrong | "Can supply all products" requires the classic relational division pattern: `NOT EXISTS(product P WHERE NOT EXISTS(supply row for R and P))`. |

---

## Q7.10 — Products where ordered quantity exceeds available

Consider the following query:

```sql
SELECT P.PRODNR, P.PRODNAME FROM PRODUCT P
WHERE EXISTS (
    SELECT * FROM PO_LINE POL
    WHERE P.PRODNR = POL.PRODNR
    GROUP BY POL.PRODNR
    HAVING SUM(POL.QUANTITY) > P.AVAILABLE_QUANTITY)
```

The query retrieves:

- **a.** The name and number of the product with the highest ordered quantity.
- **b.** The name and number of all products that are ordered and do not exceed their available quantity.
- **c.** The name and number of all products that are ordered and exceed their available quantity.
- **d.** The name and number of the product with the lowest ordered quantity.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The query does not find the single highest quantity — it compares ordered vs. available per product. |
| b | ❌ Wrong | "Do not exceed" would require `SUM(POL.QUANTITY) <= P.AVAILABLE_QUANTITY` (using `<=` not `>`). |
| c | ✅ Correct | `EXISTS` with `HAVING SUM(QUANTITY) > AVAILABLE_QUANTITY` returns all products where total ordered quantity exceeds current available stock. |
| d | ❌ Wrong | The lowest ordered quantity is irrelevant — the condition filters by stock exceedance, not order ranking. |

---

## Q7.11 — Scalar subquery in FROM

Consider the following query:

```sql
SELECT CS.CURRENT_STOCK - O.ORDERED AS NEW_STOCK
FROM (SELECT SUM(P.AVAILABLE_QUANTITY) AS CURRENT_STOCK
      FROM PRODUCT P) AS CS,
     (SELECT SUM(POL.QUANTITY) AS ORDERED
      FROM PO_LINE POL) AS O
```

The output of the query represents:

- **a.** A table summarizing for each product the increase in stock after the ordered products are delivered.
- **b.** A table summarizing for each product the decrease in stock after the ordered products are delivered.
- **c.** A scalar, summarizing the total quantity of products in stock after all the ordered products are delivered.
- **d.** A scalar, summarizing the decrease in total available quantity of all products after the ordered products are delivered.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The result is a single scalar (one number), not a per-product table. Also, this represents remaining stock, not an increase. |
| b | ❌ Wrong | Also not per-product. The value represents the remaining stock level (after deduction), not the decrease amount itself. |
| c | ✅ Correct | `CS` = total available quantity across all products (scalar); `O` = total quantity on all outstanding orders (scalar). `CURRENT_STOCK − ORDERED` = stock remaining after all orders are fulfilled. |
| d | ❌ Wrong | The decrease alone would be `O.ORDERED`. `CS − O` computes the resulting stock level, not the amount of decrease. |

---

## Q7.12 — Suppliers who can supply BOTH products 0832 and 0494

Given the task to retrieve the numbers of all suppliers who can supply products 0832 **and** 0494, which query is **correct**?

- **a.**
```sql
SELECT DISTINCT SUPNR FROM SUPPLIES
WHERE PRODNR IN (0832, 0494)
```
- **b.**
```sql
SELECT SUPNR FROM SUPPLIES WHERE PRODNR = 0832
UNION ALL
SELECT SUPNR FROM SUPPLIES WHERE PRODNR = 0494
```
- **c.**
```sql
SELECT SUPNR FROM SUPPLIES WHERE PRODNR = 0832
INTERSECT
SELECT SUPNR FROM SUPPLIES WHERE PRODNR = 0494
```
- **d.**
```sql
SELECT UNIQUE SUPNR FROM SUPPLIES
WHERE PRODNR IN (0832, 0494)
```

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | `IN (0832, 0494)` is OR logic — returns suppliers who can supply 0832 **or** 0494, not necessarily both. |
| b | ❌ Wrong | `UNION ALL` also produces OR logic (combining both sets with duplicates). Does not enforce the AND condition. |
| c | ✅ Correct | `INTERSECT` returns only suppliers appearing in **both** result sets — those who can supply 0832 **and** 0494. |
| d | ❌ Wrong | `SELECT UNIQUE` is non-standard SQL (not valid in most RDBMS). Also has the same OR logic flaw as option a. |

---

## Q7.13 — View WITH CHECK OPTION

Consider the following View definition and update statement:

```sql
CREATE VIEW TOPPRODUCTS(PRODNR, PRODNAME, QUANTITY) AS
    SELECT PRODNR, PRODNAME, AVAILABLE_QUANTITY
    FROM PRODUCT
    WHERE AVAILABLE_QUANTITY > 100
WITH CHECK OPTION;

UPDATE TOPPRODUCTS
SET QUANTITY = 80
WHERE PRODNR = 0153;
```

What will be the result of this?

- **a.** The update can be successfully made but only the PRODUCT table will be updated.
- **b.** The update can be successfully made and both the View and PRODUCT table will be updated.
- **c.** The update will be halted because of the WITH CHECK OPTION.
- **d.** The update can be successfully made but only the View will be updated.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The update will not succeed at all — `WITH CHECK OPTION` blocks it before any table is touched. |
| b | ❌ Wrong | Same — the update is rejected entirely. |
| c | ✅ Correct | `WITH CHECK OPTION` requires all modifications through the view to still satisfy the view's `WHERE` clause. Setting `AVAILABLE_QUANTITY = 80` violates `> 100`, so the RDBMS rejects the update. |
| d | ❌ Wrong | Views don't store data independently; updates through a view always modify the underlying base table. Regardless, the update is halted. |

---

## Q7.14 — COUNT(DISTINCT SUPNR) vs COUNT(SUPNR)

Compare the following two queries:

```sql
-- Query 1
SELECT COUNT(DISTINCT SUPNR) FROM PURCHASE_ORDER

-- Query 2
SELECT COUNT(SUPNR) FROM PURCHASE_ORDER
```

Which of the following statements is **correct**?

- **a.** Result query 1 is always = result query 2 because PURCHASE_ORDER contains only unique purchase orders.
- **b.** Result query 1 is always ≤ result query 2 because the DISTINCT operator counts only unique SUPNRs.
- **c.** Result query 1 is always ≥ result query 2 because query 1 sums the number of purchase orders per supplier while query 2 sums the number of purchase orders in total.
- **d.** Result query 1 is sometimes ≥ and sometimes ≤ result query 2 because the result depends on the number of suppliers and the number of purchase orders.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | PONR (order number) is unique per row, but SUPNR is not — one supplier can have many orders. So `COUNT(SUPNR)` > `COUNT(DISTINCT SUPNR)` when any supplier has 2+ orders. |
| b | ✅ Correct | `DISTINCT` collapses multiple rows for the same SUPNR into one. The distinct count can never exceed the total count. Equality holds only when every supplier has exactly one order. |
| c | ❌ Wrong | The reasoning is backwards. Query 1 counts unique suppliers (a smaller number); Query 2 counts all non-null SUPNR occurrences (larger or equal). |
| d | ❌ Wrong | The relationship is always deterministic — query 1 ≤ query 2. It is never the case that query 1 > query 2. |

---

## Q7.15 — GROUP BY PRODNR + HAVING SUM(QUANTITY) < 15

Consider the following query:

```sql
SELECT PRODNR, AVG(QUANTITY) AS AVG_QUANTITY
FROM PO_LINE
GROUP BY PRODNR
HAVING SUM(QUANTITY) < 15
```

What is the result?

- **a.** The query returns the PRODNR and average QUANTITY of each purchase order that has fewer than 15 purchase order lines.
- **b.** The query returns the PRODNR and average QUANTITY of each product that has fewer than 15 purchase order lines.
- **c.** The query returns the PRODNR and average QUANTITY of each product that has fewer than 15 orders.
- **d.** The query returns the PRODNR and average QUANTITY of each purchase order that has fewer than 15 orders.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Grouping is by `PRODNR` (product), not by `PONR` (purchase order). "Each purchase order" is incorrect. |
| b | ✅ Correct | `GROUP BY PRODNR` groups per product. `HAVING SUM(QUANTITY) < 15` filters products whose total ordered quantity (sum of all order line quantities) is below 15. |
| c | ❌ Wrong | "Fewer than 15 orders" implies `COUNT(*) < 15`. The query uses `SUM(QUANTITY)` which totals quantity values, not count of order rows. |
| d | ❌ Wrong | Grouping is by product (PRODNR), not by purchase order. |

---

## Q7.16 — Nested IN with AND (New York AND Washington)

Consider the following query:

```sql
SELECT PRODNAME FROM PRODUCT
WHERE PRODNR IN (SELECT PRODNR FROM SUPPLIES
                 WHERE SUPNR IN (SELECT SUPNR FROM SUPPLIER
                                 WHERE SUPCITY = 'New York'))
AND PRODNR IN (SELECT PRODNR FROM SUPPLIES
               WHERE SUPNR IN (SELECT SUPNR FROM SUPPLIER
                                WHERE SUPCITY = 'Washington'))
```

What is the result?

- **a.** The query retrieves the product name of each product that has a supplier in New York or Washington.
- **b.** The query retrieves the product name of each product that has both a supplier in New York and a supplier in Washington.
- **c.** The query retrieves the product name of each product along with all possible supplier cities.
- **d.** The query incorrectly combines every product name and supplier city.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | OR logic would require `UNION` in the subquery or `OR` between the two `IN` conditions in the `WHERE` clause. |
| b | ✅ Correct | `AND` between two `IN` conditions means both must be satisfied: the product must be in the New York supply set **and** in the Washington supply set simultaneously. |
| c | ❌ Wrong | The query does not join with or return city data — it purely filters products. No city column is in the output. |
| d | ❌ Wrong | The query is logically sound and well-formed; it does not produce a Cartesian product or incorrect combination. |

---

## Q7.17 — Available quantity of each ordered product of supplier "Ad Fundum"

We want to retrieve the available quantity of each ordered product of supplier Ad Fundum. Which of the following queries is **correct**?

- **a.**
```sql
SELECT PRODNR, AVAILABLE_QUANTITY FROM PRODUCT
WHERE PRODNR IN (SELECT PRODNR FROM PO_LINE)
  AND SUPNR IN (SELECT SUPNR FROM SUPPLIER WHERE SUPNAME = 'Ad Fundum')
```
- **b.**
```sql
SELECT PRODNR, AVAILABLE_QUANTITY FROM PRODUCT
WHERE SUPNR IN (SELECT SUPNR FROM SUPPLIER WHERE SUPNAME = 'Ad Fundum')
```
- **c.**
```sql
SELECT PRODNR, AVAILABLE_QUANTITY FROM PRODUCT
WHERE PRODNR IN (
    SELECT PRODNR FROM PO_LINE WHERE PONR IN (
        SELECT PONR FROM PURCHASE_ORDER WHERE SUPNR IN (
            SELECT SUPNR FROM SUPPLIER WHERE SUPNAME = 'Ad Fundum')))
```
- **d.**
```sql
SELECT PRODNR, AVAILABLE_QUANTITY FROM PRODUCT
WHERE PRODNR = (
    SELECT PRODNR FROM PO_LINE WHERE PONR = (
        SELECT PONR FROM PURCHASE_ORDER WHERE SUPNR = (
            SELECT SUPNR FROM SUPPLIER WHERE SUPNAME = 'Ad Fundum')))
```

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | `PRODUCT` has no `SUPNR` column. The `AND SUPNR IN (...)` clause applied to `PRODUCT` would cause a column-not-found error. |
| b | ❌ Wrong | Same issue — `PRODUCT` does not have a `SUPNR` attribute. The query fails. |
| c | ✅ Correct | Correctly traces the full join chain: `PRODUCT → PO_LINE → PURCHASE_ORDER → SUPPLIER`. Each `IN` subquery uses the correct foreign key at each level. |
| d | ❌ Wrong | Uses `=` (scalar comparison) instead of `IN` for subqueries that return multiple rows — causes a runtime error when there are multiple matching orders or products. |

---

## Q7.18 — Correlated subquery with COUNT

Consider the following query:

```sql
SELECT P1.PRODNR FROM PRODUCT P1
WHERE 5 <= (SELECT COUNT(*) FROM PRODUCT P2 WHERE P1.PRODNR < P2.PRODNR)
```

This query selects:

- **a.** The five highest product numbers.
- **b.** The five lowest product numbers.
- **c.** All product numbers except for the five lowest product numbers.
- **d.** All product numbers except for the five highest product numbers.

**✅ Answer: d**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The 5 highest products have 0–4 products above them → `COUNT < 5` → condition `5 <= COUNT` fails → they are **excluded**. |
| b | ❌ Wrong | The 5 lowest products have many products above them → `COUNT >> 5` → condition passes → they are **included** in results. |
| c | ❌ Wrong | The 5 lowest are included in the result (not excluded). This option is wrong. |
| d | ✅ Correct | `5 <= COUNT(products with higher PRODNR)` means at least 5 products have a higher number → this product is NOT in the top 5. All products **except** the 5 highest PRODNR values are returned. |

---

## Q7.19 — HAVING COUNT ≥ ALL

Consider the following query:

```sql
SELECT R1.SUPNAME, R1.SUPNR, COUNT(*)
FROM PURCHASE_ORDER PO1, SUPPLIER R1
WHERE PO1.SUPNR = R1.SUPNR
GROUP BY R1.SUPNR
HAVING COUNT(*) >= ALL (
    SELECT COUNT(*) FROM PURCHASE_ORDER PO2, SUPPLIER R2
    WHERE PO2.SUPNR = R2.SUPNR
    GROUP BY R2.SUPNR)
```

The query retrieves:

- **a.** The name, number, and total outstanding orders of all suppliers that have outstanding orders.
- **b.** The name, number, and total outstanding orders of all suppliers that have outstanding orders, except for the supplier(s) with the fewest outstanding orders.
- **c.** The name, number, and total outstanding orders of the supplier with the most outstanding orders.
- **d.** The name, number, and total outstanding orders of the supplier with the fewest outstanding orders.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | This would return all suppliers with at least one order — no `HAVING` needed for that. |
| b | ❌ Wrong | Excluding only the minimum would require `HAVING COUNT(*) > (SELECT MIN(...))` — a different condition. |
| c | ✅ Correct | `COUNT(*) >= ALL(all other per-supplier counts)` means this supplier's count is the maximum. Only the supplier(s) with the most outstanding orders satisfy this. |
| d | ❌ Wrong | "Fewest orders" would require `HAVING COUNT(*) <= ALL(...)`. |

---

## Q7.20 — EXCEPT with mismatched columns

Consider the following query:

```sql
SELECT P.PRODNR, P.PRODNAME FROM PRODUCT P
EXCEPT
SELECT POL.PRODNR FROM PO_LINE POL
```

The query retrieves:

- **a.** The number and name of all the products with no outstanding order.
- **b.** The number and name of all the products that are ordered.
- **c.** The query will not execute because both queries do not select the same columns.
- **d.** The query will not execute because both queries do not select the same rows.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The intended logic (products not in PO_LINE) is conceptually valid, but the query is structurally broken and will not run. |
| b | ❌ Wrong | Also moot — the query fails before producing any results. |
| c | ✅ Correct | `EXCEPT` (like `UNION`/`INTERSECT`) requires both `SELECT` clauses to have the **same number of columns**. The first returns 2 columns (`PRODNR`, `PRODNAME`); the second returns 1 (`PRODNR`). This mismatch causes an execution error. |
| d | ❌ Wrong | Matching column count and compatible data types is the requirement for set operations — not matching rows. |

---

## Q7.21 — NOT EXISTS for cheapest price

Consider the following query:

```sql
SELECT P1.PRODNR, P1.PRODNAME, S1.SUPNR, S1.PURCHASE_PRICE
FROM PRODUCT P1, SUPPLIES S1
WHERE P1.PRODNR = S1.PRODNR
AND NOT EXISTS (
    SELECT * FROM PRODUCT P2, SUPPLIES S2
    WHERE P2.PRODNR = S2.PRODNR
      AND P1.PRODNR = P2.PRODNR
      AND S1.PURCHASE_PRICE > S2.PURCHASE_PRICE)
```

And the following statements:

1. For each product, the supplier number of the supplier who can supply the product for the cheapest price is retrieved.
2. For each product, the supplier number of the supplier who supplies the product for the highest price is retrieved.
3. For each product, exactly one tuple is returned.
4. For each product, more than one tuple can be returned.

Which statements are true?

- **a.** 1 and 3.
- **b.** 1 and 4.
- **c.** 2 and 3.
- **d.** 2 and 4.

**✅ Answer: b**

| Statement | Verdict | Reason |
|-----------|---------|--------|
| 1 | ✅ True | `NOT EXISTS(a row where S2 is cheaper than S1)` = no cheaper supply option exists → S1's price IS the minimum for that product. |
| 2 | ❌ False | The query finds the minimum purchase price, not the maximum. |
| 3 | ❌ False | If two suppliers offer the exact same minimum price for a product, both rows satisfy `NOT EXISTS` and are returned (tied minimum = multiple tuples). |
| 4 | ✅ True | Ties in minimum price produce multiple tuples for the same product. |

| Option | Verdict | Reason |
|--------|---------|--------|
| a (1 & 3) | ❌ Wrong | Statement 3 is false — price ties yield multiple rows per product. |
| b (1 & 4) | ✅ Correct | Finds cheapest price suppliers (1), and ties mean more than one tuple per product is possible (4). |
| c (2 & 3) | ❌ Wrong | Statement 2 is false — it retrieves the cheapest price, not the highest. |
| d (2 & 4) | ❌ Wrong | Statement 2 is false. |

---

## Q7.22 — Scalar subquery in SELECT list

Consider the following query:

```sql
SELECT R.SUPNAME,
    (SELECT COUNT(PO.PODATE)
     FROM PURCHASE_ORDER PO
     WHERE R.SUPNR = PO.SUPNR) AS SUMMARY
FROM SUPPLIER R
```

The query selects:

- **a.** The name and total number of outstanding orders of all suppliers that have at least one outstanding order.
- **b.** The name and total number of outstanding orders of all suppliers.
- **c.** The supplier name and order date of each of his/her outstanding orders.
- **d.** The supplier name and order date of each of his/her outstanding orders. If a supplier does not have an outstanding order, she/he will be included in the output with a null value for the "SUMMARY" column.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The outer `FROM SUPPLIER R` returns ALL suppliers, not just those with orders. Suppliers with 0 orders appear with `SUMMARY = 0`, not excluded. |
| b | ✅ Correct | All suppliers are returned (outer `FROM SUPPLIER`). The correlated scalar subquery returns `0` (not NULL) for suppliers with no purchase orders, because `COUNT` on an empty set returns 0. |
| c | ❌ Wrong | The subquery returns a `COUNT` (a single integer), not individual order dates. The output has one row per supplier, not one per order. |
| d | ❌ Wrong | The SUMMARY value for suppliers with no orders is `0`, not NULL. `COUNT()` never returns NULL for an empty result — it returns 0. |
