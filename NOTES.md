# Database Interview Notes

## Data Fundamentals

- **Database definition**: A structured collection of interrelated data, managed by a Database Management System (DBMS). It is designed for efficient storage, retrieval, and manipulation of data.
- **Data definition** (Ref: Principles of Database Management, Ch. 1): Raw, unprocessed facts representing events, entities, or measurements, captured as text, numbers, media, or logs.

> **Interview Tip:** When asked to define a database, always mention the DBMS. It's the software that makes the data useful and accessible. Highlighting the DBMS shows you understand the difference between a passive collection of files and an active, managed system.

- **Context matters**: The same value can mean different things depending on metadata (e.g., `42` as order quantity vs. department id).
- **Example**: A row `{"student_id": 17, "exam": "Normalization", "score": 92}` is data until we interpret it within grading rules or trends.

> **Interview Tip:** Expect to be asked to distinguish _data_ (facts) from _information_ (interpreted facts)—always mention metadata and context to earn full credit.

## Big Data Essentials

- **Definition**: Data whose size, speed, or diversity exceeds the capacity of conventional relational systems, requiring distributed storage/processing (Ch. 2).
- **Common triggers**: Real-time telemetry, clickstream analytics, IoT sensor fleets, multi-modal logs.
- **Example**: Storing and aggregating petabytes of mobile usage events per hour across regions pushes you toward Hadoop/Spark, not a single-instance OLTP DB.

> **Interview Tip:** When defining Big Data, describe _why_ traditional RDBMS scaling (vertical) fails and mention at least one distributed technology you would consider.

## Five Vs of Big Data

- **Volume**: Massive data quantities measured in TB/PB; drives storage partitioning.
- **Velocity**: High ingestion rates (streams, CDC feeds) that demand low-latency pipelines.
- **Variety**: Structured, semi-structured (JSON), and unstructured (audio, logs) formats.
- **Veracity**: Data quality/completeness; impacts model trust.
- **Value**: Business outcomes extracted through analytics; without it, the other Vs are cost.

> **Interview Tip:** Hiring managers often ask for trade-offs—tie each V to a design decision (e.g., velocity -> streaming platform) to show practical understanding.

## Data Analytics Lifecycle

- **Extract** sources (operational DBs, APIs) and land them in staging.
- **Transform & clean** using SQL, Spark, or Pandas to normalize formats and fix anomalies.
- **Analyze** with statistical models or rule-based scoring to answer business questions.
- **Visualize & communicate** insights via dashboards or alerts for decision-makers.
- **Iterate**: Incorporate feedback, refresh questions, and recalibrate pipelines.

> **Interview Tip:** Highlight tooling with verbs (“ingest via Airflow, cleanse in dbt, model in Python”) to demonstrate end-to-end ownership.

## Data ➜ Information ➜ Knowledge ➜ Decisions

- **Data**: Facts captured at the source (sensor reading `temp=88°F`).
- **Information**: Data plus context/aggregation (average oven temp per batch).
- **Knowledge**: Patterns or rules derived from information (temps above 85°F shorten shelf life).
- **Predictions/Decisions**: Actions informed by knowledge (lower oven setting to 82°F to reduce waste).

> **Interview Tip:** Map this chain to a concrete situation from your experience; quantifying the decision’s impact shows business acumen.

## A Brief History of Data Storage

- **Punched Cards**: One of the earliest forms of data storage, punched cards represent data using holes in predefined positions on a piece of cardstock. They were instrumental in the early days of computing and were used for data input, output, and storage. Herman Hollerith's use of punched cards to process the 1890 U.S. Census is a famous example of their success.

- **Magnetic Tape**: Replacing punched cards as the primary storage medium in the 1960s, magnetic tape offered higher storage capacity and faster access speeds. Data is stored on a long strip of plastic film with a magnetic coating. While sequential access is a limitation, tape is still used today for data archiving and backups due to its low cost and high capacity.

> **Interview Tip:** While you won't be asked to design a system using punched cards, showing awareness of the historical evolution of data storage (from cards to tape to disks to cloud) demonstrates a broader understanding of the field. Mentioning the trade-offs of each technology (e.g., cost, capacity, speed, access method) will impress interviewers.

## Types of Databases

- **Relational Databases (SQL)**:

  - **Structure**: Data is organized in tables with rows and columns, and relationships between tables are maintained using keys.
  - **Use Cases**: Best for structured data and applications requiring strong consistency (ACID compliance), such as financial systems, e-commerce platforms, and transactional applications.
  - **Examples**: MySQL, PostgreSQL, Oracle, SQL Server.

- **NoSQL Databases (Non-Relational)**: A category of databases that do not use the traditional table-based relational model. They are built for scalability, flexibility, and speed.

  - **Document Databases**: Store data in flexible, JSON-like documents.
    - **Use Cases**: Content management, mobile apps, and applications with rapidly evolving schemas.
    - **Examples**: MongoDB, Couchbase.
  - **Key-Value Stores**: The simplest NoSQL databases, storing data as a collection of key-value pairs.
    - **Use Cases**: Caching, session management, and real-time bidding.
    - **Examples**: Redis, Amazon DynamoDB.
  - **Wide-Column Stores**: Store data in columns instead of rows, which is efficient for querying large datasets.
    - **Use Cases**: Big data analytics, time-series data, and IoT applications.
    - **Examples**: Apache Cassandra, HBase.

- **Graph Databases**:
  - **Structure**: Use nodes to store entities and edges to store relationships between entities.
  - **Use Cases**: Ideal for applications that need to model and query complex relationships, such as social networks, recommendation engines, and fraud detection.
  - **Examples**: Neo4j, Amazon Neptune.

> **Interview Tip:** Be prepared to discuss the trade-offs between different database types. A common interview question is "What database would you choose for [scenario]?" Frame your answer around the specific requirements of the scenario, such as data structure, scalability needs, and consistency guarantees. For example, for a social media feed, you might suggest a graph database for the social network and a wide-column store for the activity feed.

## File-Based vs. Database Approach

### The File-Based Approach

In a file-based approach, data is stored in discrete files (e.g., `.txt`, `.csv`), and is accessed by application programs that read and write to these files.

**Drawbacks:**

- **Data Redundancy and Inconsistency**: The same data may be duplicated across multiple files, leading to inconsistencies if one file is updated and the others are not.
- **Data Isolation**: Data is scattered across different files, making it difficult to access and query data from multiple files simultaneously.
- **Data Dependence**: Applications are tightly coupled to the file structure. Any change to the file format requires changes to the application code.
- **Lack of Concurrency Control**: Managing simultaneous access by multiple users is difficult and can lead to data corruption.
- **Limited Security**: It's hard to enforce granular security policies. Access is often controlled at the file level (all or nothing).

### The Database Approach

The database approach uses a Database Management System (DBMS) to manage a central repository of data. The DBMS provides a unified interface for storing, retrieving, and managing data.

**Benefits:**

- **Centralized Data Management**: Reduces data redundancy and improves consistency.
- **Data Independence**: The DBMS separates the logical view of the data from its physical storage, so changes to the physical storage do not affect application code.
- **Concurrency Control**: The DBMS handles concurrent access to ensure data integrity.
- **Improved Security**: The DBMS provides mechanisms for access control and authentication.
- **Data Integrity**: The DBMS can enforce constraints to ensure the data is accurate and consistent.

> **Interview Tip:** While the database approach is superior in most cases, be prepared to acknowledge scenarios where a file-based approach is acceptable. For simple, single-user applications with a small amount of data (e.g., configuration files, logs), a file-based approach can be a simpler and more lightweight solution. Showing this nuance demonstrates practical judgment.

## Elements of a Database System

### Database Model (Schema) vs. Instance

- **Database Model (Schema)**: The blueprint of the database. It defines the structure of the data, including the tables, columns, data types, and the relationships between them. The schema is static and does not contain any actual data.

- **Database Instance**: A snapshot of the data in the database at a specific point in time. It is the actual data stored in the database, and it changes as data is added, updated, and deleted.

> **Interview Tip:** A great analogy is the blueprint of a house versus the house itself. The blueprint is the **schema**: it defines the structure, but you can't live in it. The house with all its furniture and people is the **instance**: it's the real-world implementation of the blueprint, and its contents change over time. Using this analogy shows you have a clear and intuitive understanding of the concept.

### Database Data Models

A data model defines the logical structure of a database. The most common data models are:

- **Relational Model**: The most widely used model. Data is stored in tables (relations), and relationships are represented by common columns between tables.
- **Hierarchical Model**: Organizes data in a tree-like structure with a single root. Each record has one parent and can have multiple children.
- **Network Model**: An extension of the hierarchical model, allowing a record to have multiple parent and child records, forming a graph-like structure.
- **Object-Oriented Model**: Data is represented as objects, with properties and methods, similar to object-oriented programming.

> **Interview Tip:** While it's good to be aware of the different data models, the relational model is by far the most dominant in the industry for structured data. For most interviews, a deep understanding of the relational model and a high-level awareness of NoSQL models will be sufficient.

### Three-Schema Architecture

The three-schema architecture (also known as the three-level architecture) provides a framework for modern database design. It separates the user's view of the database from the physical storage of the database.

- **External Level (View Level)**: The highest level of abstraction. It defines how a particular user or group of users sees the data. There can be multiple external views for a single database.
- **Conceptual Level (Logical Level)**: A unified view of the entire database. It describes what data is stored and the relationships between the data, without getting into the physical storage details.
- **Internal Level (Physical Level)**: The lowest level of abstraction. It describes how the data is physically stored on the storage medium.

> **Interview Tip:** The key takeaway of the three-schema architecture is **data independence**. There are two types:
>
> 1.  **Logical Data Independence**: Changes to the conceptual schema (e.g., adding a new table) do not require changes to the external schemas.
> 2.  **Physical Data Independence**: Changes to the internal schema (e.g., changing the storage method) do not require changes to the conceptual schema.
>     Mentioning both types of data independence shows a deep understanding of the benefits of this architecture.

### Database Catalog

The database catalog (also known as the data dictionary or system catalog) is the "database of the database". It's a metadata repository that contains information about all the objects in the database, such as:

- Table and view definitions
- Column names and data types
- Index definitions
- User permissions
- Stored procedures

The DBMS uses the catalog to understand the structure of the database and to process queries.

> **Interview Tip:** A simple analogy for the database catalog is a library catalog. You wouldn't search the entire library for a book; you'd start with the catalog to find out where the book is located. Similarly, the DBMS uses the database catalog to efficiently locate and manage data.

### Types of Database Users

Database users can be categorized by their level of expertise and how they interact with the system:

- **Database Administrator (DBA)**: The most privileged user, responsible for managing the entire database system. This includes security, backups, performance tuning, and user management.
- **Application Programmers**: Developers who write applications that interact with the database. They typically use a programming language and a library (like JDBC or an ORM) to access the data.
- **Sophisticated Users**: Users who are comfortable writing their own queries in a language like SQL to directly access the database for analysis or reporting.
- **Naive/End-Users**: The majority of users, who interact with the database through pre-built applications with graphical user interfaces. They don't need to know anything about the underlying database.

> **Interview Tip:** When discussing database users, the role of the DBA is often a key focus. Be prepared to talk about the responsibilities of a DBA, such as ensuring data availability, security, and recoverability. This shows you understand the operational side of database management.

### Database Languages

Database languages are used to read, store, and update data in a database. They are often grouped into the following categories, which are all part of SQL:

- **Data Definition Language (DDL)**: Used to define and manage the database structure.

  - `CREATE`: Creates database objects (e.g., `CREATE TABLE`).
  - `ALTER`: Modifies the structure of database objects (e.g., `ALTER TABLE`).
  - `DROP`: Deletes database objects (e.g., `DROP TABLE`).

- **Data Manipulation Language (DML)**: Used to manipulate the data within the database.

  - `SELECT`: Retrieves data from the database.
  - `INSERT`: Adds new data to the database.
  - `UPDATE`: Modifies existing data in the database.
  - `DELETE`: Removes data from the database.

- **Data Control Language (DCL)**: Used to control access to the database.

  - `GRANT`: Gives user access privileges.
  - `REVOKE`: Removes user access privileges.

- **Transaction Control Language (TCL)**: Used to manage transactions in the database.
  - `COMMIT`: Saves the work done in a transaction.
  - `ROLLBACK`: Undoes the work done in a transaction.

> **Interview Tip:** SQL (Structured Query Language) is the standard language for relational databases and encompasses all four of these categories. While different databases may have their own procedural extensions to SQL (like PL/SQL for Oracle or T-SQL for SQL Server), a strong foundation in standard SQL is a must-have skill for almost any data-related role.
