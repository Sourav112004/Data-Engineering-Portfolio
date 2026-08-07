#  Product ETL Pipeline | Python • Pandas • MySQL • REST API

> An end-to-end ETL (Extract, Transform, Load) pipeline built using Python that extracts product data from a REST API, performs real-world business transformations, handles nested JSON structures, and loads clean data into MySQL.

---

# 📌 Project Overview

This project demonstrates how a Data Engineer builds a complete ETL pipeline from scratch.

The pipeline:

- Extracts product data from a REST API
- Handles API Pagination
- Stores raw JSON
- Profiles data before transformation
- Cleans and standardizes product data
- Implements business logic
- Handles nested JSON objects
- Converts text-based fields into analytics-ready numerical values
- Loads transformed data into MySQL
- Organizes the project using a production-style folder structure

---

#  Architecture

```
                   DummyJSON REST API
                           │
                           ▼
                    Extract Layer
                           │
                           ▼
                Raw JSON (products.json)
                           │
                           ▼
                 Data Profiling (Pandas)
                           │
                           ▼
                  Transform Layer
      ┌───────────────────────────────────┐
      │ Remove unwanted columns           │
      │ Handle missing values             │
      │ Flatten nested JSON               │
      │ Business Rule Transformations     │
      │ Regex Transformations             │
      │ Standardize Data                  │
      └───────────────────────────────────┘
                           │
                           ▼
          Processed JSON (products_clean.json)
                           │
                           ▼
                     Load Layer
                           │
                           ▼
                        MySQL
```

---

# 🛠 Tech Stack

- Python
- Pandas
- Requests
- JSON
- Regex (re)
- MySQL
- mysql.connector

---

# 📂 Project Structure

```
Product_ETL/

│

├── config.py
├── main.py
├── extract.py
├── transform.py
├── load.py

│

├── data/
│   ├── raw/
│   │      products.json
│   │
│   └── processed/
│          products_clean.json

│

└── README.md
```

---

#  Extract Phase

## API Source

DummyJSON REST API

### Initial Extraction

Initially only 30 products were being downloaded.

Reason:

The API uses **Pagination**

Example Response

```
{
    "products":[...],
    "total":194,
    "limit":30,
    "skip":0
}
```

---

## Pagination Implementation

Instead of extracting only 30 products, pagination was implemented.

```
skip = 0
skip = 30
skip = 60
...
skip = 180
```

Every request downloads another page.

Finally,

```
194 Products
```

are merged into a single JSON file.

---

#  Data Profiling

Before transforming the data, profiling was performed inside Jupyter Notebook.

Checks performed:

- Missing Values
- Duplicate Records
- Data Types
- Summary Statistics
- Unique Categories
- Product Distribution

This step helped identify transformation requirements before modifying the dataset.

---

#  Transform Phase

## Removed Unnecessary Columns

Dropped columns that were not useful for analytics.

- images
- thumbnail
- meta
- reviews

This reduced storage and simplified reporting.

---

## Flattened Nested JSON

The API contained nested JSON objects.

Example

```
"dimensions":
{
    "width":12.4,
    "height":6.2,
    "depth":3.8
}
```

This was flattened into

```
width
height
depth
```

making the data relational and SQL friendly.

---

#  Business Logic Implementation

One objective of the project was making the data suitable for Logistics Dashboards.

The API returned shipping durations as text.

Example

```
"Shipping 3-5 Business Days"

"2 Weeks"

"Overnight Shipping"

"1 Month"
```

These values are difficult to visualize.

Therefore business rules were implemented.

| Original Value | Converted To |
|---------------|-------------|
| Overnight | 1 |
| 2 Weeks | 14 |
| 1 Month | 30 |
| 3 Business Days | 3 |

The output became numerical

```
shipping_days
```

making it dashboard ready.

---

# Warranty Transformation

Warranty information also arrived as text.

Examples

```
1 Year Warranty

6 Months Warranty

Lifetime Warranty

No Warranty
```

Converted into

```
365

180

NULL

0
```

This enables KPI calculations and warranty analytics.

---

# Regex Transformations

Regular Expressions were used to extract numbers from strings.

Example

```
"3 Business Days"

↓

3
```

Example

```
"2 Weeks"

↓

2

↓

2 × 7

↓

14
```

Regex allowed automatic extraction without hardcoding values.

---

# Missing Value Handling

The dataset contained missing values.

Example

```
Brand = NULL
```

Initially these produced MySQL errors during loading.

---

#  Major Debugging Challenges

## Challenge 1

### Error

```
Unknown column 'nan' in field list
```

### Cause

Returning

```
None
```

inside Python functions does **not** always remain `None`.

Pandas automatically converts missing values inside numeric columns into

```
numpy.nan
```

During loading MySQL interpreted

```
nan
```

as a SQL identifier instead of NULL.

---

### Solution

Before loading every row,

```
pd.isna()
```

was used.

Every

```
numpy.nan
```

was converted back into

```
None
```

allowing MySQL to insert SQL NULL correctly.

---

## Challenge 2

Incorrect Column Mapping

Error

```
Incorrect integer value:
'In Stock'
```

Cause

The tuple order did not match the INSERT statement.

Fix

Verified every SQL column matched the Python tuple position exactly.

---

## Challenge 3

Pagination Output Changed JSON Structure

Initially

```
{
   "products":[]
}
```

After pagination

```
[
   {},
   {},
   {}
]
```

Transform script had to be updated accordingly.

---

#  Load Phase

Processed JSON was loaded into MySQL using

```
mysql.connector
```

Workflow

```
Read JSON

↓

Connect MySQL

↓

Insert Row

↓

Commit Transaction

↓

Close Connection
```

---

# Production Improvements

The project was gradually improved to resemble a production ETL pipeline.

Implemented:

 Configuration File

```
config.py
```

for

- API URL
- Database Credentials
- File Paths

---

## Pipeline Orchestration

Instead of manually executing

```
extract.py

transform.py

load.py
```

a

```
main.py
```

script was created.

Running

```
python main.py
```

executes the complete ETL pipeline.

---

## Project Modularization

Separated pipeline into

- Extract
- Transform
- Load

Each module has a single responsibility.

This architecture makes future migration to Airflow straightforward.

---

#  Output

Final Dataset

- Analytics Ready
- Flattened
- Clean
- SQL Friendly
- Business Ready

Loaded into MySQL successfully.

---

# Key Concepts Learned

- REST API Integration
- API Pagination
- JSON Processing
- Data Profiling
- Data Cleaning
- Missing Value Handling
- Business Rule Implementation
- Regex Transformations
- Nested JSON Flattening
- Pandas
- ETL Architecture
- MySQL Loading
- Python Loops
- SQL Parameterized Queries
- Production ETL Design

---

# Future Improvements

- Logging
- Exception Handling
- Incremental Loading
- UPSERT Logic
- Airflow Orchestration
- Docker
- Azure Data Factory
- PySpark
- Databricks
- CI/CD Pipeline

---

# Final Outcome

This project was built to understand how production ETL pipelines work rather than simply moving data.

It demonstrates:

- Building a modular ETL architecture
- Solving real-world data quality issues
- Implementing business transformations
- Debugging production-style ETL problems
- Designing a scalable pipeline that can later be orchestrated using Apache Airflow.
