# Quiz 4 — Chapter 9 & Chapter 11 Review Questions

---

## Part 1: Chapter 9 — Advanced SQL and ORDBMS (Pages 597–600)

---

## Q9.1 — Which statement is correct?

- **a.** In the relational model, the tuple constructor can only be used on atomic values and the set constructor can only be used on tuples.
- **b.** In the relational model, the tuple constructor allows defining composite attribute types.
- **c.** In the relational model, the set constructor allows defining multi-valued attribute types.
- **d.** In the relational model, the tuple and set constructor can be used in a nested way.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | The tuple constructor is not limited to atomic values — it is specifically used for composite (ROW) types. The set constructor is not limited to tuples either. |
| b | ❌ Wrong | While technically true that the tuple constructor creates composite types, this statement is incomplete and misleading as a standalone "correct" answer given the options. |
| c | ✅ Correct | In the ORDBMS/extended relational model, the **set constructor** is specifically used to define multi-valued attribute types (collection types), which is a key extension over the traditional relational model. |
| d | ❌ Wrong | Although nesting is possible in ORDBMS, this option overstates the claim and is not the most precise characterization of what these constructors are designed to do. |

---

## Q9.2 — Which of the following is NOT an advantage of triggers?

- **a.** Triggers support automatic monitoring and verification in case of specific events or situations.
- **b.** Triggers allow avoidance of deadlock situations.
- **c.** Triggers allow modeling extra semantics and/or integrity rules without changing the user front-end or application code.
- **d.** Triggers allow performance of synchronic updates in case of data replication.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong (i.e., this IS an advantage) | Triggers fire automatically on defined events, enabling monitoring and verification without manual invocation — a genuine advantage. |
| b | ✅ Correct (i.e., this is NOT an advantage) | Triggers do **not** avoid deadlocks. In fact, poorly designed triggers can **cause** deadlocks by locking resources in unexpected sequences. |
| c | ❌ Wrong (i.e., this IS an advantage) | Triggers encapsulate business logic at the database level, so no changes to application code or front-end are needed — a clear advantage. |
| d | ❌ Wrong (i.e., this IS an advantage) | Triggers can be used to keep replicated data in sync by propagating updates automatically — a legitimate advantage. |

---

## Q9.3 — The key difference between stored procedures and triggers is that:

- **a.** Stored procedures are explicitly invoked whereas triggers are implicitly invoked.
- **b.** Stored procedures cannot have input variables whereas triggers can.
- **c.** Stored procedures are stored in the data catalog, whereas triggers are not.
- **d.** Stored procedures are more difficult to debug than triggers.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | Stored procedures must be **explicitly called** by a user or application. Triggers fire **automatically (implicitly)** in response to DML events (INSERT, UPDATE, DELETE). |
| b | ❌ Wrong | It is the **opposite**: stored procedures CAN have input parameters; triggers **cannot** accept parameters — they execute automatically without arguments. |
| c | ❌ Wrong | **Both** stored procedures and triggers are stored in the database catalog (data dictionary). |
| d | ❌ Wrong | This is subjective and not the defining or key difference between the two constructs. |

---

## Q9.4 — Which of the following is correct?

- **a.** A distinct data type is a user-defined data type which specializes a standard, built-in SQL data type.
- **b.** An opaque data type is an entirely new, user-defined data type, which is not based upon any existing SQL data type.
- **c.** An unnamed row type allows inclusion of a composite data type in a table by using the keyword ROW.
- **d.** A named row type is a user-defined data type that groups a coherent set of data types into a new composite data type and assigns a meaningful name to it.
- **e.** All of the above are correct.

**✅ Answer: e**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | A **distinct type** is created from an existing built-in SQL type (e.g., creating `EURO` from `DECIMAL`) — it inherits the representation but not the functions. |
| b | ✅ Correct | An **opaque type** is a completely new type with no inherited behavior from existing SQL types; its internal structure is hidden from the DBMS. |
| c | ✅ Correct | An **unnamed row type** uses the `ROW(...)` keyword inline within a `CREATE TABLE` statement to define a composite column without giving the type a reusable name. |
| d | ✅ Correct | A **named row type** (created with `CREATE ROW TYPE`) defines a reusable composite type with a meaningful name that can be referenced across multiple table definitions. |
| e | ✅ Correct | All four preceding definitions are accurate, so **e** is the correct answer. |

---

## Q9.5 — Which of the following is correct?

- **a.** User-defined functions (UDFs) can only work on user-defined data types.
- **b.** A sourced function is a user-defined function (UDF) that is based on an existing, built-in function.
- **c.** User-defined functions (UDFs) can only be defined in SQL.
- **d.** User-defined functions (UDFs) must be stored in the application, and not in the catalog.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | UDFs can operate on **both** user-defined types and standard built-in SQL types. |
| b | ✅ Correct | A **sourced function** is a specific type of UDF that overloads or adapts an existing built-in function to work with a new user-defined type. |
| c | ❌ Wrong | UDFs can be written in **external languages** (e.g., C, Java) in addition to SQL, making them more flexible. |
| d | ❌ Wrong | UDFs are stored **in the database catalog**, not in the application — this is a key reason to use them (centralized logic). |

---

## Q9.6 — An ORDBMS will typically support inheritance…

- **a.** only at tuple level.
- **b.** only at data type level.
- **c.** only at table type level.
- **d.** at both data type and table type level.

**✅ Answer: d**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | "Tuple level" is not the standard term for ORDBMS inheritance and this omits the full scope. |
| b | ❌ Wrong | While ORDBMSs do support **type inheritance** (subtype/supertype hierarchies for UDTs), they also support table inheritance — so "only" is incorrect. |
| c | ❌ Wrong | Similarly, while **table inheritance** (subtables inheriting columns from supertables) is supported, type inheritance is also supported — "only" is incorrect. |
| d | ✅ Correct | An ORDBMS supports inheritance at **both levels**: (1) **data type level** (UDT hierarchies) and (2) **table type level** (table hierarchies where subtables inherit structure from supertables). |

---

## Q9.7 — Which of these statements is correct?

- **a.** A set is an ordered collection with no duplicates.
- **b.** A bag is an unordered collection which may contain duplicates.
- **c.** A list is an ordered collection which cannot contain duplicates.
- **d.** An array is an unordered collection which can contain duplicates.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | A **set** is an **unordered** collection with no duplicates. Order is not guaranteed in a set. |
| b | ✅ Correct | A **bag** (also called a multiset) is indeed an **unordered** collection that **allows duplicates** — it is like a set but without the uniqueness constraint. |
| c | ❌ Wrong | A **list** is ordered but it **can** contain duplicates. The uniqueness restriction does not apply to lists. |
| d | ❌ Wrong | An **array** is an **ordered** (indexed) collection that can contain duplicates. Order is a defining property of arrays. |

---

## Q9.8 — Which data type can be used to store image data?

- **a.** BLOB.
- **b.** CLOB.
- **c.** DBCLOB.
- **d.** None of the above.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | **BLOB** (Binary Large OBject) is designed for large binary data such as images, audio, and video files. |
| b | ❌ Wrong | **CLOB** (Character Large OBject) stores large amounts of character/text data (e.g., long documents), not binary image data. |
| c | ❌ Wrong | **DBCLOB** (Double-Byte Character Large OBject) stores large text data using double-byte character sets (e.g., for Asian languages), not binary image data. |
| d | ❌ Wrong | BLOB is a valid data type for image storage, so "none of the above" is incorrect. |

---

## Q9.9 — Recursive queries are a powerful SQL extension which allow formulation of complex queries such as…

- **a.** queries that need to combine data from multiple tables.
- **b.** queries that need to get access to multimedia data.
- **c.** queries that need to navigate through a hierarchy of tuples.
- **d.** queries that have multiple subqueries.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Combining data from multiple tables is accomplished with **JOINs**, not recursive queries. |
| b | ❌ Wrong | Accessing multimedia data is handled by **LOB data types** (BLOB/CLOB) and UDTs, not recursive queries. |
| c | ✅ Correct | Recursive queries (using `WITH RECURSIVE` / Common Table Expressions) are specifically designed to **traverse hierarchical structures** — e.g., org charts, bill-of-materials, category trees — where you need to follow parent-child relationships across an unknown number of levels. |
| d | ❌ Wrong | Having multiple subqueries is a standard SQL feature and does not require recursion. Recursive queries solve a fundamentally different problem. |

---

## Q9.10 — In industry, ORDBMSs have…

- **a.** been very successful since they replaced RDBMSs as the mainstream database technology.
- **b.** had modest success, with most companies only implementing a carefully selected set of extensions.
- **c.** not been successful at all.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | ORDBMSs have **not** replaced RDBMSs. Traditional relational databases remain dominant in enterprise settings. |
| b | ✅ Correct | Major RDBMS vendors (Oracle, IBM DB2, PostgreSQL) incorporated **selective ORDBMS features** (e.g., UDTs, stored procedures, LOBs) into their products, but the full ORDBMS vision was never universally adopted. |
| c | ❌ Wrong | ORDBMS extensions did achieve real adoption — just not as a wholesale replacement for the relational model. Calling them completely unsuccessful is inaccurate. |

---

## Part 2: Chapter 11 — NoSQL Databases (Pages 798–802)

---

## Q11.1 — Which of the following statements describes NoSQL databases best?

- **a.** A NoSQL database offers no support for SQL.
- **b.** NoSQL databases do not support joins.
- **c.** NoSQL databases are non-relational.
- **d.** NoSQL databases are not capable of dealing with large datasets.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | "NoSQL" does **not** mean "no SQL." Many NoSQL databases (e.g., Cassandra with CQL, Couchbase with N1QL) offer SQL-like query languages. The term means "Not only SQL." |
| b | ❌ Wrong | While many NoSQL databases lack join support, this is not universal and is not the defining characteristic. Some NewSQL/document stores do support forms of joins. |
| c | ✅ Correct | The best and most accurate description is that NoSQL databases are **non-relational** — they do not rely on the relational model (tables, rows, foreign keys) as their primary data model. |
| d | ❌ Wrong | This is the **opposite** of reality. NoSQL databases were largely developed to handle **massive, large-scale datasets** that exceed the scaling limits of traditional RDBMSs. |

---

## Q11.2 — Which of the following is NOT an example of a NoSQL database?

- **a.** Graph-based databases.
- **b.** XML-based databases.
- **c.** Document-based databases.
- **d.** All three can be regarded as NoSQL databases.

**✅ Answer: d**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong (it IS NoSQL) | Graph databases (e.g., Neo4j) are a recognized NoSQL category, storing data as nodes and edges rather than relational tables. |
| b | ❌ Wrong (it IS NoSQL) | XML-based databases store semi-structured data in XML format and are considered a non-relational (NoSQL) database type. |
| c | ❌ Wrong (it IS NoSQL) | Document stores (e.g., MongoDB, CouchDB) are one of the most widely used NoSQL database categories. |
| d | ✅ Correct | All three — graph-based, XML-based, and document-based — are valid examples of NoSQL databases. There is no option among a, b, or c that is "not" a NoSQL database. |

---

## Q11.3 — Which of the following is NOT a property of a good hash function for use in key–value-based storage structures?

- **a.** A hash function should always return the same output for the same input.
- **b.** A hash function should return an output of fixed size.
- **c.** A good hash function should map its inputs as evenly as possible over the output range.
- **d.** Two hashes from two inputs that differ little should also differ as little as possible.

**✅ Answer: d**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong (this IS a property) | **Determinism** — the same input must always produce the same hash output — is a fundamental requirement of any hash function. |
| b | ❌ Wrong (this IS a property) | Producing a **fixed-size output** regardless of input size is essential so keys can be stored and compared efficiently. |
| c | ❌ Wrong (this IS a property) | **Uniform distribution** across the output range minimizes collisions and ensures even load distribution across nodes in a distributed system. |
| d | ✅ Correct (this is NOT a property) | This describes the **opposite** of what is desired. A good hash function should exhibit the **avalanche effect**: even a tiny change in input should produce a drastically different output. Hashes that change "little" for similar inputs would cluster similar keys together, causing load imbalance and collisions. |

---

## Q11.4 — Which of the following is correct?

- **a.** The fact that most NoSQL databases adopt an eventual consistency approach is due to the CAP theorem, which states that strong consistency cannot be obtained when availability and partitioning have to be ensured.
- **b.** Replicas in a distributed NoSQL environment relate to making periodic backups of the database to a second system.
- **c.** Stabilization relates to the waiting time between the start-up of a NoSQL system and when the system becomes available to receive user queries.
- **d.** Some relational constructs, such as the many-to-many relationship, are harder to express using graph databases.

**✅ Answer: a**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ✅ Correct | The **CAP theorem** states that a distributed system can guarantee at most 2 of 3: **C**onsistency, **A**vailability, and **P**artition tolerance. Since NoSQL systems prioritize Availability + Partition tolerance (AP), they sacrifice strong consistency, leading to **eventual consistency**. |
| b | ❌ Wrong | **Replicas** in NoSQL refer to **live, synchronized copies** of data distributed across nodes for fault tolerance and read scalability — not periodic backups. Backups are a separate concept. |
| c | ❌ Wrong | **Stabilization** (or "settling") in NoSQL refers to the time for all replicas to converge to a consistent state **after a write** propagates through the cluster — not system start-up time. |
| d | ❌ Wrong | Graph databases are actually **superior** at modeling many-to-many relationships because relationships (edges) are first-class citizens. It is relational and document databases that struggle comparatively with many-to-many. |

---

## Q11.5 — Which of the following is correct?

- **a.** Document stores require users to define document schemas before data can be inserted.
- **b.** Document stores require that you perform all filtering and aggregation logic in your application.
- **c.** Document stores are built on the same ideas as key–value- and tuple-based database systems.
- **d.** Document stores do not provide SQL-like capabilities.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Document stores are **schema-flexible (schema-less)**. Documents in the same collection can have different fields — no pre-defined schema is required before insertion. |
| b | ❌ Wrong | Modern document stores (e.g., MongoDB) provide built-in **aggregation pipelines**, MapReduce, and query operators — you do not have to handle all logic in the application layer. |
| c | ✅ Correct | Document stores extend **key–value stores** (a document is a structured "value" retrieved by a key) and share ideas with **tuple-based systems** (documents resemble rows with named fields, and some implementations like Cassandra blend tuple and document concepts). |
| d | ❌ Wrong | Many document stores now offer **SQL-like query languages** (e.g., Couchbase's N1QL, MongoDB's MQL with SQL compatibility layers), so this is no longer generally true. |

---

## Q11.6 — When are column-oriented databases more efficient?

- **a.** When many columns of a single group need to be fetched at the same time.
- **b.** When inserts are performed where all of the row data are supplied at the same time.
- **c.** When aggregates need to be calculated over many or all rows in the dataset.
- **d.** When a lot of joins need to be performed in queries.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Fetching many columns for a **single row** (or group) is exactly where **row-oriented** databases excel — all column values for a row are stored contiguously. Column stores would need to read from multiple column files. |
| b | ❌ Wrong | Full-row inserts (supplying all column data at once) are more efficient in **row-oriented** stores. Column stores must write each column value to a separate location, making individual inserts more costly. |
| c | ✅ Correct | Column-oriented databases shine for **analytical aggregations** (SUM, AVG, COUNT) across a single column over millions of rows — only the relevant column is scanned, and columnar data compresses very well, minimizing I/O. |
| d | ❌ Wrong | Joins require correlating data across multiple attributes of the same row, which is more efficient in **row-oriented** databases where all row data is co-located. |

---

## Q11.7 — Which of the following statements is NOT correct?

- **a.** Graphs are mathematical structures consisting of nodes and edges.
- **b.** Graph models are not capable of modeling many-to-many relationships.
- **c.** Edges in graphs can be uni- or bidirectional.
- **d.** Graph databases work particularly well on tree-like structures.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong (this IS correct) | By definition, a graph is a mathematical structure of **nodes (vertices)** and **edges**, used to represent relationships. |
| b | ✅ Correct (this is NOT correct) | Graph models are **excellent** at modeling many-to-many relationships — each edge directly represents a relationship between two nodes, making many-to-many natural and efficient. This is one of the key strengths of graph databases. |
| c | ❌ Wrong (this IS correct) | Edges can be **directed** (uni-directional, e.g., A→B) or **undirected** (bidirectional, e.g., A—B), depending on the relationship being modeled. |
| d | ❌ Wrong (this IS correct) | Trees are a special case of graphs (acyclic connected graphs). Graph databases handle tree-like hierarchical structures (e.g., org charts, file systems) very naturally. |

---

## Q11.8 — What does the following Cypher query express?

```cypher
OPTIONAL MATCH (user:User)-[:FRIENDS_WITH]-(friend:User)
WHERE user.name = "Bart Baesens"
RETURN user, count(friend) AS NumberOfFriends
```

- **a.** Get the node for Bart Baesens and a count of all his friends, but only if at least one FRIENDS_WITH relation exists.
- **b.** Get the node for Bart Baesens and a count of all his friends, even if no FRIENDS_WITH relation exists.
- **c.** This query will fail if Bart Baesens is FRIENDS_WITH himself.
- **d.** Get the node for Bart Baesens and all his friends.

**✅ Answer: b**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | This describes a regular `MATCH`, which would return nothing if no FRIENDS_WITH relation exists. `OPTIONAL MATCH` behaves differently. |
| b | ✅ Correct | `OPTIONAL MATCH` is analogous to a **LEFT OUTER JOIN** — it returns the `user` node even if no matching `friend` nodes are found (friend will be `null`, and `count(friend)` returns 0). |
| c | ❌ Wrong | The query does not fail on self-references; Cypher handles this gracefully. There is no inherent error condition from self-referential edges. |
| d | ❌ Wrong | The query returns `user` and a **count** of friends (`count(friend)`), not the individual friend nodes themselves. |

---

## Q11.9 — Using Cypher, how do you get a list of all movies Wilfried Lemahieu has liked, when he has given at least four stars?

**a.**
```cypher
SELECT (b:User)--(m:Movie)
WHERE b.name = "Wilfried Lemahieu"
AND m.stars >= 4
```

**b.**
```cypher
MATCH (b:User)-[l:LIKES]-(m:Movie)
WHERE b.name = "Wilfried Lemahieu"
AND m.stars >= 4
RETURN m
```

**c.**
```cypher
MATCH (b:User)-[l:LIKES]-(m:Movie)
WHERE b.name = "Wilfried Lemahieu"
AND l.stars >= 4
RETURN m
```

**d.**
```cypher
MATCH (b:User)--(m:Movie)
WHERE b.name = "Wilfried Lemahieu"
AND l.stars >= 4
RETURN m
```

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | Uses `SELECT`, which is **SQL syntax**, not Cypher. Cypher uses `MATCH`/`RETURN`. Also, the relationship type is unspecified and there is no `RETURN` clause. |
| b | ❌ Wrong | Filters on `m.stars` — the **movie's** star property. The star rating (how many stars the user gave) is a property of the **LIKES relationship**, not the movie node itself. |
| c | ✅ Correct | Correctly names the relationship `[l:LIKES]` and filters on `l.stars >= 4` — the **relationship property** that stores the user's rating. This is the proper Cypher pattern when a property belongs to the relationship rather than either endpoint node. |
| d | ❌ Wrong | Uses `--` (anonymous relationship with no variable binding), so `l` is never defined, making `l.stars` an undefined reference. This query would produce an error. |

---

## Q11.10 — What does the following Cypher query express?

```cypher
MATCH (bart:User {name:'Bart'})-[:KNOWS*2]->(f)
WHERE NOT((bart)-[:KNOWS]->(f))
RETURN f
```

- **a.** Return all of Bart's friends, and their friends as well.
- **b.** Do not return Bart's friends, but return their friends.
- **c.** Do not return Bart's friends, but return their friends if Bart does not know them.
- **d.** Return Bart's friends who have exactly one other friend.

**✅ Answer: c**

| Option | Verdict | Reason |
|--------|---------|--------|
| a | ❌ Wrong | `[:KNOWS*2]` means **exactly 2 hops**, not 1 or 2 hops. Bart's direct friends (1 hop) are not included by the MATCH pattern. The WHERE NOT further filters results. |
| b | ❌ Wrong | This is partially right (direct friends are excluded by `*2` which only traverses 2 hops), but it misses the crucial `WHERE NOT` clause that **additionally excludes** friends-of-friends that Bart already knows directly. |
| c | ✅ Correct | `[:KNOWS*2]` finds users reachable by **exactly 2 KNOWS hops** (friends-of-friends). The `WHERE NOT((bart)-[:KNOWS]->(f))` clause then **excludes** any of those who Bart already knows directly, returning only those "friends of friends" that Bart does **not** already know. |
| d | ❌ Wrong | Nothing in the query restricts `f` to having exactly one friend. `*2` refers to the path length from Bart, not the degree of `f`. |
