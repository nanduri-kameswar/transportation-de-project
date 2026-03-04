# Transportation End-To-End Real-Time Data Engineering Project (2026)

## Project Overview
This project simulates a real-time taxi/ride-booking system (similar to Uber or Ola) to build a production-grade data engineering solution. It covers the entire lifecycle of data, from **real-time event ingestion** to **dimensional modeling** in a Gold layer, utilizing a **Medallion Architecture** (Bronze, Silver, and Gold).

## System Architecture
The architecture follows a **Publisher-Subscriber (Pub/Sub)** model to handle high-velocity streaming data.

1.  **Data Production:** A custom **Fast API web application** simulates ride bookings, producing real-time events.
2.  **Ingestion Hub:** **Azure Event Hub** (a managed instance of Apache Kafka) acts as the central channel for storing ordered events.
3.  **Batch Ingestion:** **Azure Data Factory (ADF)** is used for **metadata-driven ingestion** of historical and mapping data from GitHub APIs into **Azure Data Lake Storage (ADLS) Gen2**.
4.  **Processing & Transformation:** **Azure Databricks** serves as the primary consumer, utilizing **Spark Declarative Pipelines (SDP)**—the modern upgrade to Apache Spark—for incremental and stateful processing.
5.  **Storage:** Data is organized in a data lake using **Delta format** across the Medallion layers.

## Tech Stack
*   **Languages:** Python (Fast API, PySpark), SQL, Jinja2 (Templating).
*   **Orchestration:** Azure Data Factory (ADF) & Databricks Jobs.
*   **Streaming:** Azure Event Hub (Kafka-compatible) & Spark Structured Streaming.
*   **Data Warehouse/Lake:** Azure Data Lake Storage Gen2 & Azure Databricks (Unity Catalog).
*   **Framework:** Spark Declarative Pipelines (SDP/DLT).

## Key Features

### 1. Metadata-Driven Ingestion
Instead of hardcoding individual pipelines for every file, this project utilizes **metadata-driven architectures**. 
*   **ADF Dynamic Pipelines:** Uses a `files_array.json` config and **Lookup/For-Each activities** to ingest multiple mapping files dynamically.
*   **Jinja2 SQL Templating:** Implements a modular transformation framework in Databricks. By using Jinja2, the project generates complex **One Big Table (OBT)** joins dynamically based on a configuration file, allowing for future enhancements without modifying core code.

### 2. Medallion Architecture
*   **Bronze Layer:** Contains the exact replica of source data. Real-time events from Event Hub are captured into `rides_raw` streaming tables.
*   **Silver Layer:** Consolidates initial bulk loads and incremental real-time streams into a single **OBT (One Big Table)** using **Append Flows**. This layer provides a decentralized data source for various business domains.
*   **Gold Layer:** Implements a **Star Schema** with six dimension tables and one centralized fact table.

### 3. Advanced Data Modeling (SCD Type 2)
To handle changing contextual data (e.g., city names or regions), the project implements **Slowly Changing Dimensions (SCD) Type 2** using the **autoCDC** (Apply Changes) API in SDP. This ensures historical data is preserved by tracking "start" and "end" dates for dimension records.

## Pipeline Details
*   **Real-time Stream:** Event Hub -> Databricks (SDP) -> Bronze Streaming Table.
*   **Watermarking:** Implemented in the Silver layer to handle late-arriving data and manage stateful streaming joins.
*   **Fact Table:** Aggregates numerical "facts" (fares, distances, ratings) and links them to dimension keys for analytical reporting.

## How to Run
1.  **Azure Setup:** Create a Resource Group, Event Hub (Standard Tier), ADLS Gen2 account, and Data Factory instance.
2.  **Web App:** Run the Fast API application (`api.py`) to start producing simulated ride events to Event Hub.
3.  **ADF Pipeline:** Trigger the `HTTP_to_ADLS` pipeline to migrate mapping data.
4.  **Databricks SDP:** Create an ETL Pipeline in Databricks, pointing to the source code in the `Databricks Files` folder to build the Bronze, Silver, and Gold layers.

---
*This project was built following the instructional guidance of Ansh Lamba.*

