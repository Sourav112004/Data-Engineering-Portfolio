# CSV-to-MySQL ETL Pipeline

A production-style ETL (Extract, Transform, Load) pipeline built with Python and MySQL using a real-world messy e-commerce dataset. This project focuses on data validation, business rule implementation, logging, exception handling, modular architecture, and loading clean data into a relational database.

---

# Project Overview

This project simulates how raw business data arrives in an organization and is transformed into clean, analysis-ready data before being loaded into a MySQL database.

The objective was not only to clean the data, but also to build the pipeline using software engineering best practices that can later be migrated into Apache Airflow.

---

# Dataset

**Dataset:** Messy E-Commerce Sales Dataset (Kaggle)

The dataset intentionally contains real-world data quality issues such as:

- Mixed date formats
- Duplicate records
- Missing values
- Invalid quantities
- Inconsistent payment methods
- Inconsistent country names
- Missing customer ratings
- Missing shipping cities

---

# Project Structure

```
CSV-MySQL-ETL-Pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── rejected/
│   └── invalid_quantity.csv
│
├── logs/
│   └── etl.log
│
├── extract.py
├── validation.py
├── transform.py
├── load.py
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ETL Architecture

```
                Raw CSV
                   │
                   ▼
              Extract Layer
                   │
                   ▼
           Data Validation Layer
                   │
                   ▼
          Data Transformation Layer
                   │
                   ▼
           Clean Processed CSV
                   │
                   ▼
             MySQL Database
```

---

# Pipeline Workflow

## 1. Extract

Reads the raw CSV dataset.

Tasks:

- Load CSV into Pandas
- Validate file existence
- Handle empty files
- Log extraction details

---

## 2. Validation

Before transforming the data, validation checks were performed.

Checks included:

- Total rows
- Total columns
- Duplicate records
- Invalid quantities
- Missing shipping cities
- Missing customer ratings
- Delivered orders with missing ratings

Example Validation Output

```
Rows                          : 12180
Columns                       : 13
Duplicate Orders              : 180
Invalid Quantity              : 186
Missing Shipping City         : 494
Delivered Missing Rating      : 643
```

---

## 3. Transformation

Business rules were implemented based on realistic scenarios.

### Duplicate Removal

Removed only completely duplicated rows while keeping the first occurrence.

```python
df.drop_duplicates(keep="first")
```

---

### Missing Discounts

Business Rule

Missing discounts imply no discount was applied.

```
NULL → 0
```

---

### Missing Shipping City

Business Rule

Missing shipping cities were replaced with

```
Unknown
```

This ensures Power BI dashboards do not display blank categories.

---

### Payment Method Standardization

Different representations were standardized.

Example

```
upi
UPI
U.P.I

↓

UPI
```

Similarly,

```
credit card
Credit_Card

↓

Credit Card
```

---

### Date Standardization

The dataset contained multiple formats.

Examples

```
2025-01-06
06 Jan 2025
01-14-2025
26/08/2024
```

All dates were converted into a standard format using

```python
pd.to_datetime(format="mixed")
```

---

### Invalid Quantity Handling

Business Rule

Orders with

```
Quantity <= 0
```

were treated as invalid.

Instead of deleting them permanently,

they were moved into

```
rejected/invalid_quantity.csv
```

for future investigation.

This mimics how production ETL pipelines preserve bad records.

---

### Country Standardization

Examples

```
USA
U.S.A
US

↓

United States
```

```
UK
U.K.
United Kingdom

↓

United Kingdom
```

---

# Loading into MySQL

The cleaned dataset is loaded into MySQL using

- mysql-connector-python
- Parameterized INSERT statements
- NULL handling
- Transaction commit

Example

```python
cursor.execute(sql, values)
```

---

# Logging

Instead of using multiple log files,

the entire pipeline writes into a centralized

```
etl.log
```

This provides a complete execution timeline.

Example

```
ETL Started

Extract Started

12180 rows extracted

Transformation Started

Duplicate Rows Removed

Invalid Quantity Rows Rejected

Processed CSV Saved

Loaded 11814 Records into MySQL

ETL Completed Successfully
```

---

# Exception Handling

Each ETL stage contains dedicated exception handling.

Examples

- FileNotFoundError
- EmptyDataError
- KeyError
- MySQL Connection Errors
- Unexpected Exceptions

Errors are logged before terminating the pipeline.

---

# Configuration Management

All configurable values were separated into

```
config.py
```

Examples

- File paths
- MySQL credentials
- Database name

This avoids hardcoding values throughout the project.

---

# Main Pipeline

Instead of executing each script manually,

a central

```
main.py
```

acts as the pipeline orchestrator.

Execution Flow

```
Extract

↓

Validate

↓

Transform

↓

Load
```

This structure closely resembles how Apache Airflow DAGs orchestrate ETL jobs.

---

# Technologies Used

- Python
- Pandas
- MySQL
- MySQL Connector
- VS Code
- Logging Module

---

# Skills Demonstrated

- ETL Development
- Data Cleaning
- Data Validation
- Business Rule Implementation
- MySQL
- Pandas
- Exception Handling
- Logging
- Modular Python Development
- Configuration Management
- Production-ready Project Structure

---

# Challenges Faced

## 1. Mixed Date Formats

Challenge

The dataset contained several inconsistent date formats.

Solution

Used

```python
pd.to_datetime(format="mixed", errors="coerce")
```

to standardize all dates safely.

---

## 2. Duplicate Records

Challenge

Differentiate between duplicated rows and legitimate repeated order IDs.

Solution

Only removed rows that were completely identical using

```python
drop_duplicates()
```

---

## 3. Invalid Quantities

Challenge

Negative and zero quantities appeared in the dataset.

Solution

Instead of deleting them,

invalid rows were stored inside

```
rejected/
```

for auditing.

---

## 4. Country Standardization

Challenge

The same country appeared under several names.

Solution

Used mapping dictionaries to standardize all country values.

---

## 5. Payment Method Inconsistency

Challenge

Payment methods had inconsistent casing and formatting.

Solution

Applied lowercase conversion followed by dictionary mapping.

---

## 6. Logging Architecture

Initially,

each module generated its own log file.

Later,

logging was centralized into a single

```
etl.log
```

using Python's logging module and named loggers.

---

## 7. Modular ETL Design

Initially,

each script executed independently.

The project was later refactored into reusable functions orchestrated through

```
main.py
```

making the pipeline easier to maintain and closer to production ETL systems.

---

# Future Enhancements

- Apache Airflow orchestration
- Incremental loading
- Data quality reports
- Email alerts
- Docker containerization
- Unit testing with pytest
- Environment variables using `.env`
- Logging rotation
- CI/CD using GitHub Actions
- Cloud deployment

---

# Learning Outcomes

This project helped me understand

- End-to-end ETL development
- Building modular Python applications
- Production logging practices
- Exception handling
- Business-driven data transformation
- Data validation
- MySQL integration
- Preparing ETL pipelines for orchestration using Apache Airflow

---

# Author

**Sourav Prakash**

Aspiring Data Engineer | SQL | Python | MySQL | ETL | Power BI

```




