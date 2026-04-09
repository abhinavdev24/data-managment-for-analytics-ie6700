# Chapter 9: Extended Relational Databases

## Chapter Objectives
- Identify the shortcomings of the relational model
- Define and use triggers and stored procedures
- Understand how RDBMSs can be extended with OO concepts (UDTs, UDFs, inheritance, behavior, polymorphism, collection types, LOBs)
- Define and use recursive SQL queries

---

## 9.1 Limitations of the Relational Model

The relational model is built on two key building blocks:
- **Tuple**: a composition of values of attribute types describing an entity (created using a tuple constructor)
- **Relation**: a mathematical set of tuples describing similar entities (created using a set constructor)

The relational model is also called a **value-based model** because primary–foreign key relationships are based on actual, observable data values (vs. OO's identity-based model using unobservable object identifiers).

### Key Shortcomings

| Limitation | Explanation |
|---|---|
| **Flat structure** | Normalization means data is fragmented across multiple relations; expensive joins needed to defragment |
| **No specialization/aggregation** | Modeling concepts like specialization, categorization, aggregation cannot be directly supported |
| **Two type constructors only** | Tuple constructor (atomic values only → no composite types) and set constructor (tuples only → no multi-valued types); they cannot be nested |
| **No behavior storage** | Cannot store functions inside the DBMS runtime; reduces reuse and functional independence |
| **Poor multimedia support** | No built-in support for audio, video, or text files |

> **Exam Tip**: The relational model has only TWO type constructors (tuple + set) that are NOT orthogonal (cannot be nested). This prevents composite and multi-valued attributes.

---

## 9.2 Active RDBMS Extensions

### Key Terms

| Term | Definition |
|---|---|
| **Passive** | Traditional RDBMS that only executes transactions explicitly invoked by users/applications |
| **Active** | Modern RDBMS that can autonomously take initiative for action when specific situations occur |

Two key components of active RDBMSs: **triggers** and **stored procedures**.

---

### 9.2.1 Triggers

**Trigger**: A piece of SQL code (declarative and/or procedural) stored in the RDBMS catalog. It is **automatically activated ("fired")** by the RDBMS whenever a specific event (INSERT, UPDATE, DELETE) occurs AND a specific condition is evaluated as true.

> Unlike CHECK constraints, triggers can reference attribute types in **other tables**. → Used to enforce complex semantic constraints.

#### Trigger Syntax
```sql
CREATE TRIGGER trigger-name
BEFORE | AFTER trigger-event ON table-name
[ REFERENCING old-or-new-values-alias-list ]
[ FOR EACH { ROW | STATEMENT } ]
[ WHEN (trigger-condition) ]
trigger-body;
```

#### After Trigger vs. Before Trigger

| Term | Definition |
|---|---|
| **After trigger** | Executes trigger body AFTER the triggering event (e.g., INSERT, UPDATE, DELETE) takes place |
| **Before trigger** | Executes trigger body BEFORE the triggering event takes place; can modify the new row before it is inserted |

#### Example — After Trigger (update TOTAL-SALARY when new employee is inserted):
```sql
CREATE TRIGGER SALARYTOTAL
AFTER INSERT ON EMPLOYEE
FOR EACH ROW
WHEN (NEW.DNR IS NOT NULL)
UPDATE DEPARTMENT
SET TOTAL-SALARY = TOTAL-SALARY + NEW.SALARY
WHERE DNR = NEW.DNR
```

#### Example — Before Trigger (set default salary/bonus from WAGE table):
```sql
CREATE TRIGGER WAGEDEFAULT
BEFORE INSERT ON EMPLOYEE
REFERENCING NEW AS NEWROW
FOR EACH ROW
SET (SALARY, BONUS) =
  (SELECT BASE_SALARY, BASE_BONUS
   FROM WAGE
   WHERE JOBCODE = NEWROW.JOBCODE)
```

#### Advantages of Triggers
- Automatic monitoring/verification when specific events occur
- Modeling extra semantics/integrity rules without changing application code
- Assigning default values to attribute types for new tuples
- Synchronic updates during data replication
- Automatic auditing and logging
- Automatic exporting of data (e.g., to the web)

#### Disadvantages/Risks of Triggers
- **Hidden functionality** — hard to follow-up and manage
- **Cascade effects** — a trigger triggering another trigger → infinite loop
- **Uncertain outcomes** — if multiple triggers defined for the same event
- **Deadlock situations** — if trigger and event pertain to different transactions
- **Debugging complexity** — they don't reside in an application environment
- **Maintainability and performance problems**

> **Exam Tip**: Triggers are IMPLICITLY fired; stored procedures are EXPLICITLY called.

#### Schema-Level Triggers (DDL Triggers)
Also called **DDL triggers** — fired after changes to the DBMS schema (creating, dropping, or altering tables, views, etc.).

---

### 9.2.2 Stored Procedures

**Stored procedure**: A piece of SQL code (declarative and/or procedural) stored in the RDBMS catalog. It must be **invoked explicitly** by calling it from an application or command prompt.

> Key difference from triggers: stored procedures are **explicitly called**; triggers are **implicitly fired**.

#### Example:
```sql
CREATE PROCEDURE REMOVE-EMPLOYEES
(DNR-VAR IN CHAR(4), JOBCODE-VAR IN CHAR(6)) AS
BEGIN
  DELETE FROM EMPLOYEE
  WHERE DNR = DNR-VAR AND JOBCODE = JOBCODE-VAR;
END
```

Called via JDBC:
```java
CallableStatement cStmt = conn.prepareCall("{call REMOVE-EMPLOYEES(?, ?)}");
cStmt.setString(1, "D112");
cStmt.setString(2, "JOB124");
cStmt.execute();
```

#### Advantages of Stored Procedures
- Store behavior in the database; compiled upfront → better performance
- Reduce network traffic (calculations done "close to the data")
- Application-independent; shareable across applications/programming languages
- Improve data and functional independence; support customized security rules
- Container for several SQL instructions that logically belong together
- Easier to debug than triggers (explicitly called)

#### Disadvantage
- Main disadvantage: **maintainability** (like triggers)

---

## 9.3 Object-Relational RDBMS Extensions

**Object-Relational DBMS (ORDBMS)**: Combines the best of RDBMS and OODBMS. Keeps the relation as the fundamental building block and SQL as the core DDL/DML, but extends them with OO concepts.

OO Extensions added by ORDBMSs:
1. User-defined types (UDTs)
2. User-defined functions (UDFs)
3. Inheritance
4. Behavior
5. Polymorphism
6. Collection types
7. Large objects (LOBs)

> Popular ORDBMSs: **PostgreSQL** (open-source), Oracle, Microsoft SQL Server, IBM DB2.

---

### 9.3.1 User-Defined Types (UDTs)

**User-defined types (UDTs)**: Define customized data types with specific properties, extending standard SQL data types (char, varchar, int, float, double, date, time, boolean).

**Five types of UDTs:**

| UDT Type | Definition |
|---|---|
| **Distinct data type** | Extends an existing SQL data type (inherits its properties) |
| **Opaque data type** | Entirely new data type, NOT based on any existing SQL data type |
| **Unnamed row type** | Composite data type using the ROW keyword; cannot be reused in other tables or used to define a table |
| **Named row type** | Groups a coherent set of data types into a new composite type with a meaningful name; CAN be reused and used to define tables |
| **Table data type** | Defines the type of a table, like a class in OO; used to instantiate multiple tables with the same structure |

---

#### 9.3.1.1 Distinct Data Types

**Distinct data type**: A user-defined data type that **specializes** a standard, built-in SQL data type. Inherits all properties of the underlying SQL type.

**Key advantage**: Prevents erroneous calculations or comparisons between semantically different types (e.g., EUR vs. USD amounts).

```sql
CREATE DISTINCT TYPE US-DOLLAR AS DECIMAL(8,2)
CREATE DISTINCT TYPE EURO AS DECIMAL(8,2)

CREATE TABLE ACCOUNT
(ACCOUNTNO SMALLINT PRIMARY KEY NOT NULL,
 AMOUNT-IN-DOLLAR US-DOLLAR,
 AMOUNT-IN-EURO EURO)
```

When a distinct type is defined, the ORDBMS **automatically creates two casting functions**:
- One to cast values from the user-defined type → underlying built-in type
- One to cast values from the built-in type → user-defined type

```sql
-- This FAILS due to type incompatibility (EURO vs DECIMAL):
SELECT * FROM ACCOUNT WHERE AMOUNT-IN-EURO > 1000

-- This WORKS (cast 1000 to EURO first):
SELECT * FROM ACCOUNT WHERE AMOUNT-IN-EURO > EURO(1000)
```

---

#### 9.3.1.2 Opaque Data Types

**Opaque data type**: An **entirely new**, user-defined data type, NOT based upon any existing SQL data type.

Examples: image, audio, video, fingerprints, text, spatial data, RFID tags, QR codes.

- Requires user-defined functions to work with the type
- Can be used anywhere a standard SQL data type can be used

```sql
CREATE OPAQUE TYPE IMAGE AS <...>
CREATE OPAQUE TYPE FINGERPRINT AS <...>

CREATE TABLE EMPLOYEE
(SSN SMALLINT NOT NULL,
 FNAME CHAR(25) NOT NULL,
 ...
 EMPFINGERPRINT FINGERPRINT,
 PHOTOGRAPH IMAGE)
```

---

#### 9.3.1.3 Unnamed Row Types

**Unnamed row type**: Includes a **composite data type** in a table using the keyword `ROW`. Consists of a combination of built-in types, distinct types, opaque types, etc.

**Limitation**: Cannot be re-used in other tables (must be explicitly redefined wherever needed) and **cannot be used to define a table**.

```sql
CREATE TABLE EMPLOYEE
(SSN SMALLINT NOT NULL,
 NAME ROW(FNAME CHAR(25), LNAME CHAR(25)),
 ADDRESS ROW(
   STREET_ADDRESS CHAR(20) NOT NULL,
   ZIP_CODE CHAR(8),
   CITY CHAR(15) NOT NULL),
 ...)
```

> Using unnamed/named row types implies the **end of the First Normal Form** (1NF no longer required in ORDBMSs).

---

#### 9.3.1.4 Named Row Types

**Named row type**: A user-defined data type that groups a coherent set of data types into a new composite data type and **assigns a meaningful name** to it.

- Can be reused in table definitions, queries, or anywhere a standard SQL data type can be used
- Can be used to define a table (unlike unnamed row types)
- Can be used as type for input/output parameters of SQL routines/functions
- Individual components accessed using the **dot (.) operator**

```sql
CREATE ROW TYPE ADDRESS AS
(STREET_ADDRESS CHAR(20) NOT NULL,
 ZIP_CODE CHAR(8),
 CITY CHAR(15) NOT NULL)

CREATE TABLE EMPLOYEE
(SSN SMALLINT NOT NULL,
 FNAME CHAR(25) NOT NULL,
 LNAME CHAR(25) NOT NULL,
 EMPADDRESS ADDRESS,
 ...)

-- Access components with dot operator:
SELECT LNAME, EMPADDRESS
FROM EMPLOYEE
WHERE EMPADDRESS.CITY = 'LEUVEN'
```

---

#### 9.3.1.5 Table Data Types

**Table data type** (typed table): Defines the **type of a table**, much like a class in OO. Used to instantiate multiple tables with the same structure.

- A column of a table type definition can refer to another table type using the keyword `REF`
- REF in ORDBMSs is the counterpart of OIDs in OODBMSs, but can be explicitly requested and visualized
- Use `DEREF` function to replace a reference with the actual data it refers to

```sql
CREATE TYPE EMPLOYEETYPE AS
(SSN SMALLINT NOT NULL, FNAME CHAR(25) NOT NULL, LNAME CHAR(25) NOT NULL,
 EMPADDRESS ADDRESS, ...)

-- Instantiate multiple tables from one type:
CREATE TABLE EMPLOYEE OF TYPE EMPLOYEETYPE PRIMARY KEY (SSN)
CREATE TABLE EX-EMPLOYEE OF TYPE EMPLOYEETYPE PRIMARY KEY (SSN)

-- REF to another table type:
CREATE TYPE DEPARTMENTTYPE AS
(DNR SMALLINT NOT NULL,
 DNAME CHAR(25) NOT NULL,
 DLOCATION ADDRESS,
 MANAGER REF(EMPLOYEETYPE))
```

---

### 9.3.2 User-Defined Functions (UDFs)

**User-defined functions (UDFs)**: Allow users to extend built-in functions (MIN, MAX, AVG) by explicitly defining their own functions. Similar to methods in OODBMSs.

- Work on both built-in and user-defined data types
- Every UDF has: a name, input/output arguments, and an implementation
- Implementation can be written in proprietary procedural SQL extensions or external languages (C, Java, Python)
- Stored in the ORDBMS → encapsulation/information hiding
- Most ORDBMSs **overload UDFs** → UDFs operating on different data types can have the same name

**Three types of UDFs:**

| UDF Type | Definition |
|---|---|
| **Sourced function** | UDF based on an existing, built-in function; often used with distinct data types |
| **External scalar function** | Explicitly defined in an external host language (Java, C, Python); returns a **single value (scalar)** |
| **External table function** | Explicitly defined in an external host language; returns a **table of values** |

#### Example — Sourced Function:
```sql
CREATE DISTINCT TYPE MONETARY AS DECIMAL(8,2)

CREATE FUNCTION AVG(MONETARY)
RETURNS MONETARY
SOURCE AVG(DECIMAL(8,2))

-- Use it:
SELECT DNR, AVG(SALARY)
FROM EMPLOYEE
GROUP BY DNR
```

---

### 9.3.3 Inheritance

The relational model is **flat** — no superclass-subclass relationships, no inheritance. ORDBMSs add explicit support for inheritance at both data type and typed table levels.

Inheritance is specified using the keyword **`UNDER`**.

#### 9.3.3.1 Inheritance at Data Type Level

A child data type inherits all properties of a parent data type and can be further specialized.

```sql
CREATE ROW TYPE ADDRESS AS
(STREET_ADDRESS CHAR(20) NOT NULL, ZIP_CODE CHAR(8), CITY CHAR(15) NOT NULL)

-- Subtype adds COUNTRY:
CREATE ROW TYPE INTERNATIONAL_ADDRESS AS
(COUNTRY CHAR(25) NOT NULL) UNDER ADDRESS

-- Use in table:
CREATE TABLE EMPLOYEE
(..., EMPADDRESS INTERNATIONAL_ADDRESS, ...)

-- Query using inherited CITY attribute:
SELECT FNAME, LNAME, EMPADDRESS
FROM EMPLOYEE
WHERE EMPADDRESS.COUNTRY = 'Belgium' AND EMPADDRESS.CITY LIKE 'Leu%'
```

> INTERNATIONAL_ADDRESS inherits CITY from ADDRESS (its supertype).

#### 9.3.3.2 Inheritance at Table Type Level

Table hierarchy mirrors the type hierarchy. Use `UNDER` for tables as well.

```sql
CREATE TYPE EMPLOYEETYPE AS (SSN SMALLINT NOT NULL, FNAME CHAR(25) NOT NULL, ...)
CREATE TYPE ENGINEERTYPE AS (DEGREE CHAR(10) NOT NULL, LICENSE CHAR(20) NOT NULL) UNDER EMPLOYEETYPE
CREATE TYPE MANAGERTYPE AS (STARTDATE DATE, TITLE CHAR(20)) UNDER EMPLOYEETYPE

CREATE TABLE EMPLOYEE OF TYPE EMPLOYEETYPE PRIMARY KEY (SSN)
CREATE TABLE ENGINEER OF TYPE ENGINEERTYPE UNDER EMPLOYEE
CREATE TABLE MANAGER OF TYPE MANAGERTYPE UNDER EMPLOYEE
```

**Key rules:**
- Primary key is only defined for the **maximal supertable**; inherited by all subtables
- Most RDBMSs do NOT support multiple inheritance (a subtype can have at most one supertype)
- Type/table hierarchy can be multiple levels deep; no cyclic references allowed

**Query behavior with inheritance:**
```sql
-- Returns SSN, FNAME, LNAME for ALL employees (including managers and engineers):
SELECT SSN, FNAME, LNAME FROM EMPLOYEE

-- Returns ONLY pure employees (excludes subtables):
SELECT SSN, FNAME, LNAME FROM ONLY EMPLOYEE

-- Returns manager-specific data (ORDBMS auto-fetches inherited columns from EMPLOYEE):
SELECT SSN, FNAME, LNAME, STARTDATE, TITLE FROM MANAGER
```

---

### 9.3.4 Behavior

An ORDBMS can include the **signature/interface of a method** in the definitions of data types and tables — the implementation remains hidden (information hiding). This behavior can be considered as **virtual columns** in a table.

```sql
CREATE TYPE EMPLOYEETYPE AS
(...,
 FUNCTION AGE(EMPLOYEETYPE) RETURNS INTEGER)

CREATE TABLE EMPLOYEE OF TYPE EMPLOYEETYPE PRIMARY KEY (SSN)

-- AGE acts like a virtual column:
SELECT SSN, FNAME, LNAME, PHOTOGRAPH
FROM EMPLOYEE
WHERE AGE = 60
```

Users do not need to know whether AGE is a real column or a virtual column (function). This enforces encapsulation.

---

### 9.3.5 Polymorphism

**Polymorphism**: A subtype inherits both attribute types and functions of its supertype. It can also **override functions** to provide more specialized implementations. The same function call can invoke different implementations depending on the data type it is related to.

```sql
-- Base function for all employees:
CREATE FUNCTION TOTAL_SALARY(EMPLOYEE E)
RETURNING INT
AS SELECT E.SALARY

-- Overridden function for managers (adds monthly bonus):
CREATE FUNCTION TOTAL_SALARY(MANAGER M)
RETURNING INT
AS SELECT M.SALARY + <monthly_bonus>

-- This query uses the correct implementation automatically:
SELECT TOTAL_SALARY FROM EMPLOYEE
-- (ORDBMS picks the right version depending on whether the tuple is a manager or not)
```

---

### 9.3.6 Collection Types

ORDBMSs provide **type constructors** to define collection types. A collection type can be instantiated as a collection of instances of standard data types or UDTs.

> Using collection types implies the **end of First Normal Form** (1NF).

**Four collection types:**

| Collection Type | Description |
|---|---|
| **Set** | Unordered collection, **no duplicates** |
| **Multiset / Bag** | Unordered collection, **duplicates allowed** |
| **List** | Ordered collection, duplicates allowed |
| **Array** | Ordered and indexed collection, duplicates allowed |

#### Example — SET for multiple phone numbers:
```sql
CREATE TYPE EMPLOYEETYPE AS
(..., TELEPHONE SET(CHAR(12)), FUNCTION AGE(EMPLOYEETYPE) RETURNS INTEGER)

CREATE TABLE EMPLOYEE OF TYPE EMPLOYEETYPE (PRIMARY KEY SSN)

-- Query using IN operator on a set:
SELECT SSN, FNAME, LNAME
FROM EMPLOYEE
WHERE '2123375000' IN (TELEPHONE)

-- THE keyword: transforms subquery result (set of sets) into atomic values:
SELECT T.TELEPHONE
FROM THE (SELECT TELEPHONE FROM EMPLOYEE) AS T
ORDER BY T.TELEPHONE
```

#### REF + DEREF with Collection Types:
```sql
CREATE TYPE DEPARTMENTTYPE AS
(DNR CHAR(3) NOT NULL, DNAME CHAR(25) NOT NULL,
 MANAGER REF(EMPLOYEETYPE),
 PERSONNEL SET(REF(EMPLOYEETYPE)))   -- set of references to employees

CREATE TABLE DEPARTMENT OF TYPE DEPARTMENTTYPE (PRIMARY KEY DNR)

-- Without DEREF: returns meaningless references
SELECT PERSONNEL FROM DEPARTMENT WHERE DNR = '123'

-- With DEREF: returns actual data
SELECT DEREF(PERSONNEL).FNAME, DEREF(PERSONNEL).LNAME
FROM DEPARTMENT WHERE DNR = '123'
```

**DEREF**: Function that replaces a reference (REF) with the actual data it points to. Enables navigational access via **path expressions** (dot notation).

---

### 9.3.7 Large Objects (LOBs)

**Large objects (LOBs)**: Introduced by ORDBMSs to handle large data items like audio, video, photos, text files, maps, etc.

> Traditional relational DBMSs provide no adequate support for large data items.

**Storage**: LOB data is stored in a **separate table and tablespace**; the base table includes a LOB indicator (pointer) to that location.

**Three types of LOBs:**

| LOB Type | Definition |
|---|---|
| **BLOB (binary large object)** | Variable-length **binary** string whose interpretation is left to an external application (e.g., images, video) |
| **CLOB (character large object)** | Variable-length **character** strings made up of **single-byte** characters (e.g., large text documents) |
| **DBCLOB (double byte character large object)** | Variable-length character strings made up of **double-byte** characters (e.g., Chinese, Japanese text) |

ORDBMSs provide customized SQL functions for LOB data (e.g., functions to search in image or video data, access text at a specified position).

---

## 9.4 Recursive SQL Queries

**Recursive SQL queries**: A powerful SQL extension that allows formulation of complex queries involving hierarchies. They compensate for the cumbersome way hierarchies are modeled in the relational model via foreign keys.

**Use case**: Querying hierarchies to an arbitrary level or depth (e.g., finding all subordinates of an employee).

### Structure of a Recursive Query

A recursive SQL query always contains **three parts**:

1. **Base/Anchor query** — the seed; selects the starting point(s)
2. **Recursive query** — references the temporary view being defined
3. **UNION ALL** — joins both result sets

```sql
WITH SUBORDINATES(SSN, NAME, SALARY, MNGR, LEVEL) AS
(
  -- Part 1: Base/anchor query (start with CEO, MNGR=NULL)
  SELECT SSN, NAME, SALARY, MNGR, 1
  FROM EMPLOYEE
  WHERE MNGR=NULL

  UNION ALL

  -- Part 2: Recursive query
  SELECT E.SSN, E.NAME, E.SALARY, E.MNGR, S.LEVEL+1
  FROM SUBORDINATES AS S, EMPLOYEE AS E
  WHERE S.SSN=E.MNGR
)
-- Final query on the temporary view:
SELECT * FROM SUBORDINATES
ORDER BY LEVEL
```

### How it works (step by step):
1. **Base query** runs first → returns the root (e.g., Jones, LEVEL=1)
2. **Recursive step** runs → finds direct subordinates of Jones (LEVEL=2)
3. **Recursive step repeats** → finds subordinates of those (LEVEL=3)
4. Process stops when no more rows can be added

### Example with Employee Hierarchy:

Given: `Employee(SSN, Name, Salary, MNGR)` where MNGR is a NULL-ALLOWED FK to SSN.

| SSN | Name | Salary | MNGR |
|---|---|---|---|
| 1 | Jones | 10,000 | NULL |
| 2 | Baesens | 2,000 | 3 |
| 3 | Adams | 5,000 | 1 |
| 4 | Smith | 6,000 | 1 |
| 5 | vanden Broucke | 3,000 | 3 |
| 6 | Lemahieu | 2,500 | 3 |

**Full result** (all subordinates of Jones):

| SSN | Name | Salary | MNGR | LEVEL |
|---|---|---|---|---|
| 1 | Jones | 10,000 | NULL | 1 |
| 3 | Adams | 5,000 | 1 | 2 |
| 4 | Smith | 6,000 | 1 | 2 |
| 2 | Baesens | 2,000 | 3 | 3 |
| 5 | vanden Broucke | 3,000 | 3 | 3 |
| 6 | Lemahieu | 2,500 | 3 | 3 |

To find subordinates of **Adams** instead, change the base query:
```sql
WHERE NAME='ADAMS'
```

---

## Key Terms Glossary

| Term | Definition |
|---|---|
| **active** | An RDBMS that can autonomously take initiative for action when specific situations occur (via triggers/stored procedures) |
| **after trigger** | A trigger that executes its body AFTER the triggering event (INSERT/UPDATE/DELETE) has taken place |
| **before trigger** | A trigger that executes its body BEFORE the triggering event takes place; can modify new data before it is stored |
| **BLOB (binary large object)** | Variable-length binary string stored in separate tablespace; interpretation left to external application |
| **CLOB (character large object)** | Variable-length character string (single-byte characters) stored as a LOB |
| **DBCLOB (double byte character large object)** | Variable-length character string of double-byte characters (e.g., for Asian scripts) stored as a LOB |
| **distinct data type** | A user-defined type that specializes an existing SQL built-in type; prevents meaningless cross-type comparisons |
| **external scalar function** | A UDF written in an external host language (C, Java, Python) that returns a single scalar value |
| **external table function** | A UDF written in an external host language that returns a table of values |
| **large objects (LOBs)** | Data types introduced by ORDBMSs to handle large items (audio, video, text); stored separately from the base table |
| **named row type** | A composite user-defined type with a meaningful name; reusable across tables and functions |
| **opaque data type** | An entirely new user-defined type NOT based on any existing SQL type (e.g., IMAGE, FINGERPRINT) |
| **passive** | A traditional RDBMS that only executes transactions explicitly invoked by users/applications |
| **schema-level triggers** | Also called DDL triggers; fired after changes to the DBMS schema (CREATE, DROP, ALTER on tables/views) |
| **sourced function** | A UDF based on an existing built-in function; often used with distinct data types |
| **stored procedure** | SQL code stored in the RDBMS catalog; must be explicitly called from an application or command prompt |
| **table data type** | A type that defines the structure of a table (like a class in OO); used to instantiate multiple tables with the same structure |
| **trigger** | SQL code stored in the RDBMS catalog; automatically fired when a specific event occurs and a condition is true |
| **unnamed row type** | A composite type using the ROW keyword; not reusable in other tables and cannot define a table |
| **user-defined functions (UDFs)** | Functions defined by users to extend built-in RDBMS functions; stored in the ORDBMS; supports overloading |
| **user-defined types (UDTs)** | Customized data types defined by users to extend standard SQL types (5 kinds: distinct, opaque, unnamed row, named row, table) |

---

## Summary

Three extensions to traditional RDBMSs discussed in this chapter:

| Extension | Key Concepts |
|---|---|
| **Active extensions** | Triggers (implicit, event-driven) and Stored Procedures (explicit, called by application) |
| **Object-relational extensions** | UDTs, UDFs, Inheritance, Behavior, Polymorphism, Collection Types, LOBs |
| **Recursive SQL queries** | WITH clause + UNION ALL + anchor query + recursive query; for querying hierarchies to arbitrary depth |

**ORDBMSs** extend RDBMSs with OO facilities while retaining the relation as the fundamental building block and SQL as the core DML. This provides a "best of both worlds" approach.

> **Exam Tip (Review Question 9.1 Answer)**: In the relational model, the tuple constructor can **only** be used on atomic values and the set constructor can **only** be used on tuples. This is statement **a** — the correct one.

---

## Quick Reference: SQL Syntax Cheat Sheet

```sql
-- Trigger
CREATE TRIGGER name BEFORE|AFTER event ON table
FOR EACH ROW WHEN (condition) body;

-- Stored Procedure
CREATE PROCEDURE name (param IN type) AS BEGIN ... END

-- Distinct Type
CREATE DISTINCT TYPE name AS base-type

-- Opaque Type
CREATE OPAQUE TYPE name AS <...>

-- Named Row Type
CREATE ROW TYPE name AS (field type, ...)

-- Subtype (Inheritance)
CREATE ROW TYPE subname AS (extra-field type) UNDER parentname

-- Table Data Type
CREATE TYPE name AS (fields...)
CREATE TABLE tablename OF TYPE name PRIMARY KEY (pk)

-- Table Inheritance
CREATE TABLE subtable OF TYPE subtype UNDER supertable

-- UDF Sourced
CREATE FUNCTION name(input-type) RETURNS return-type SOURCE builtin(base-type)

-- Polymorphic UDF
CREATE FUNCTION name(subtype param) RETURNING type AS SELECT ...

-- Collection in type
TELEPHONE SET(CHAR(12))
PERSONNEL SET(REF(EMPLOYEETYPE))

-- DEREF
SELECT DEREF(col).field FROM table WHERE ...

-- Recursive Query
WITH viewname(cols) AS (
  SELECT ... FROM ... WHERE ...   -- anchor
  UNION ALL
  SELECT ... FROM viewname AS v, table AS t WHERE ...  -- recursive
)
SELECT * FROM viewname ORDER BY LEVEL
```
