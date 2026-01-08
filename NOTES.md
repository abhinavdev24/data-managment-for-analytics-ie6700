# Database Interview Notes

## Data Fundamentals

- **Data definition** (Ref: Principles of Database Management, Ch. 1): Raw, unprocessed facts representing events, entities, or measurements, captured as text, numbers, media, or logs.
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
