# SQL Analytics Portfolio — Project Journey & Future Improvements

---

## How We Built This Project

This document covers every phase followed to build this project from scratch,
and everything that can be done to extend it further in the future.

---

## Phase 1 — Schema Design

The first step was designing the database before writing a single line of code.
This is how real data projects work — you think about the data first.

We designed a 12-table e-commerce schema representing a realistic Indian online
shopping platform. Each table was planned in plain notebook-style notation first
(table name, column names, data types, constraints) before converting it to SQL.

The tables designed were:

- customer_segments — groups customers into tiers like Premium, Regular, New
- customers — stores customer profiles with location and demographic details
- categories — product category definitions like Electronics, Clothing, Books
- suppliers — vendor details including country and rating
- products — the product catalogue with selling price and cost price both stored
- coupons — discount codes with validity periods and discount percentages
- orders — order headers linking a customer, a coupon, and a status
- order_items — individual line items within each order
- payments — payment attempts per order with method and status
- shipments — shipment tracking with carrier and delivery dates
- returns — return requests with reasons like Damaged or Wrong Item
- reviews — customer ratings and written reviews per product

Key decisions made during schema design:

- Storing both price and cost_price on products so profit margin queries are possible
- Keeping payments as a separate table from orders to allow multiple payment attempts
- Keeping shipments separate so re-shipments after returns can be tracked
- Adding order_item_id to returns so we can query returns at the product level
- Using Indian carriers (BlueDart, DTDC, Delhivery, FedEx) and payment methods
  (UPI, Wallet, Net Banking) to make the dataset feel realistic and grounded

We also defined all cardinality relationships:
- Most relationships are one to many (1:N)
- The only one to one (1:1) relationship is between order_items and returns
- The natural many to many between orders and products is resolved by order_items

---

## Phase 2 — Data Generation (Module 2)

Once the schema was finalised we wrote generate_data.py inside the scripts/ folder.

This script:
- Connects to DuckDB and creates the database file at data/ecommerce.duckdb
- Drops all tables first (in reverse FK order) so the script is safe to re-run
- Recreates all 12 tables with proper constraints
- Populates every table with realistic fake data using the Faker library
- Uses a fixed random seed (42) so the data is identical on every run
- Inserts data in the correct order to respect all foreign key relationships
- Calculates derived columns like line_total and total_amount from base values

Row counts generated:
- customer_segments : 5
- customers         : 500
- categories        : 15
- suppliers         : 30
- products          : 100
- coupons           : 50
- orders            : 2000
- order_items       : ~5900
- payments          : 2000
- shipments         : ~1150
- returns           : 300
- reviews           : 1000

Two bugs were fixed during this phase:
- Coupon codes were duplicating due to a small random number range — fixed by
  widening the range and tracking used codes in a set
- Product price was being indexed incorrectly (index 3 instead of 4) causing a
  TypeError — fixed by correcting the tuple index

---

## Phase 3 — SQL Queries (Module 3)

We wrote 20 SQL query files across three difficulty levels. Each file follows
the same format — a comment block at the top explaining the business question
and SQL concept, followed by the actual query.

Beginner queries (queries/01_beginner/) cover:
- Basic SELECT, WHERE, ORDER BY, LIMIT
- GROUP BY and HAVING
- COUNT, SUM, AVG aggregations
- Date filtering

Intermediate queries (queries/02_intermediate/) cover:
- INNER JOIN and LEFT JOIN across multiple tables
- Subqueries
- CTEs (WITH clause)
- CASE WHEN for conditional logic
- NULLIF for safe division
- Multi-table aggregations

Advanced queries (queries/03_advanced/) cover:
- RANK, DENSE_RANK, ROW_NUMBER window functions
- LAG and LEAD for comparing across rows
- Running totals with SUM OVER
- EXPLAIN for reading query execution plans

Business questions answered range from simple counts to revenue analysis,
return rate by category, coupon effectiveness, supplier profit margins,
month-on-month growth, and customer ranking by city.

---

## Phase 4 — Report Generation (Module 4)

We wrote two files for this phase:

scripts/template.html — a Jinja2 HTML template that defines the structure
of the report. It has placeholders for the query filename, business question,
concept, SQL code, and result table. Jinja2 fills these placeholders in at
runtime with real data.

scripts/run_queries.py — a Python script that:
- Connects to the DuckDB database
- Loops through all .sql files in all three query folders in order
- Parses the comment block from each file to extract the business question
  and concept
- Executes each query and captures the result as a pandas DataFrame
- Passes everything to the Jinja2 template
- Renders and saves the final report to reports/index.html

One bug was fixed during this phase:
- Windows was trying to write the HTML file using cp1252 encoding which could
  not handle some characters generated by Faker — fixed by explicitly specifying
  UTF-8 encoding on both the file read and file write operations

---

## Phase 5 — GitHub Actions Automation (Module 5)

We wrote .github/workflows/run_and_publish.yml — the automation workflow.

This workflow:
- Triggers automatically on every push to the queries/ folder
- Sets up a fresh Ubuntu environment with Python 3.11
- Installs all dependencies from requirements.txt
- Runs generate_data.py to recreate the database
- Runs run_queries.py to execute all queries and generate the report
- Uploads the reports/ folder as a GitHub Pages artifact
- Deploys it live to GitHub Pages

This means any time a new query is added or an existing one is modified and
pushed, the live report updates automatically within a few minutes. No manual
steps needed.

---

## Phase 6 — Documentation (Module 6)

We wrote the final README.md covering:
- Project overview and purpose
- Live report link and workflow status badge
- Full schema table with descriptions of all 12 tables
- Complete query index with business questions for all 20 queries
- Folder structure
- How to run the project locally step by step
- Full list of SQL concepts covered
- Tech stack

---

## Project Folder Structure

sql-analytics-portfolio/

├── schema/

│   └── schema.sql                  ← all CREATE TABLE statements

├── data/

│   └── ecommerce.duckdb            ← auto-generated, gitignored

├── queries/

│   ├── 01_beginner/                ← queries 01 to 06

│   ├── 02_intermediate/            ← queries 07 to 14

│   └── 03_advanced/                ← queries 15 to 20

├── scripts/

│   ├── generate_data.py            ← generates the dataset

│   ├── run_queries.py              ← executes queries, renders report

│   └── template.html               ← Jinja2 HTML template

├── reports/

│   └── index.html                  ← auto-generated report

├── .github/

│   └── workflows/

│       └── run_and_publish.yml     ← GitHub Actions workflow

├── .gitignore

├── requirements.txt

└── README.md

---

## Tech Stack Used

- DuckDB — in-process analytical database, no server needed
- Python — scripting language for data generation and report rendering
- Faker — generates realistic fake data
- pandas — handles query results as DataFrames
- Jinja2 — HTML templating engine
- GitHub Actions — automates the pipeline on every push
- GitHub Pages — hosts the live HTML report publicly

---

## Future Improvements

Everything listed below can be added to this project at any point without
breaking what already exists.

---

### 1. Add more queries

The simplest extension. Just drop a new .sql file into the right folder with
the same comment block format and the pipeline picks it up automatically.

Ideas for new queries:
- Customer lifetime value (total spend per customer since signup)
- Average delivery time per carrier
- Products that have never been ordered
- Customers who placed orders but never left a review
- Revenue contribution of top 10% of customers (Pareto analysis)
- Cohort analysis — retention of customers by signup month
- Day of week with highest order volume
- Payment failure rate by payment method

---

### 2. Upgrade the report to a Streamlit dashboard

Instead of a static HTML file, build an interactive Streamlit app where:
- You can select any query from a dropdown
- Results display as a table with sorting and filtering
- Charts appear alongside the results for numeric queries
- You can write and run custom SQL directly in the browser

This would turn the project from a static report into a live analytics tool.

---

### 3. Add data visualisations to the HTML report

Without switching to Streamlit, you can add Plotly charts directly into the
existing HTML template using Plotly.js. For example:
- A bar chart for orders by status
- A line chart for monthly revenue
- A pie chart for payment method distribution

The run_queries.py script would generate the chart JSON and pass it to the
Jinja2 template alongside the table data.

---

### 4. Add a second dataset

Swap out the e-commerce data for a different domain and run the same pipeline
on it. Good options:
- A healthcare dataset (patients, diagnoses, prescriptions, billing)
- A logistics dataset (warehouses, shipments, routes, delivery times)
- A university dataset (students, courses, grades, attendance)

The automation stays exactly the same — only generate_data.py and the .sql
files change.

---

### 5. Add query performance benchmarking

For each query, record the execution time and display it in the report. Over
time this builds a record of which queries are slow and which are fast. You
can then show the before and after execution times when you add an index or
rewrite a query using a CTE instead of a subquery.

This directly demonstrates query optimisation skills.

---

### 6. Add data quality checks

Before running the queries, add a data_quality_checks.py script that:
- Verifies row counts are within expected ranges
- Checks for NULL values in NOT NULL columns
- Verifies foreign key integrity
- Checks for duplicate primary keys

If any check fails, the GitHub Actions workflow stops and posts a warning
before the report is generated.

---

### 7. Schedule the workflow to run daily

Currently the workflow only triggers on a push to queries/. You can add a
scheduled trigger so it also runs every day at a fixed time:

```yaml
on:
  push:
    paths:
      - 'queries/**'
  schedule:
    - cron: '0 6 * * *'
```

This keeps the live report always fresh even without any code changes.

---

### 8. Connect to a real data source

Instead of generating fake data, pull real data from a public API or dataset:
- Government open data portals (data.gov.in)
- Kaggle datasets downloaded via the Kaggle API
- Public e-commerce datasets from UCI or Hugging Face

The rest of the pipeline stays the same — only generate_data.py changes.

---

### 9. Integrate with other portfolio projects

This project's database can be directly reused in other projects from the
portfolio list:
- A/B Testing Engine (Project 10) — run statistical tests on orders data
- Customer Churn Prediction (Project 12) — use customers and orders as the
  training dataset
- Automated EDA Reporter (Project 04) — point the EDA reporter at any table
  exported from this database

---

### 10. Add a dark mode to the HTML report

A simple CSS addition to template.html using the prefers-color-scheme media
query. No backend changes needed.

---

### 11. Export query results to CSV

Add an option in run_queries.py to also save each query result as a .csv file
in a results/ folder alongside the HTML report. Useful for sharing raw data
with others or loading results into other tools.

---

### 12. Add pagination to the report

Currently the report shows the first 20 rows of each query result. For queries
with many rows, add pagination controls to the HTML so you can browse through
all results without the page becoming too long.