# End-to-End Customer Churn Data Engineering Pipeline

## Overview

An end-to-end layered data pipeline that supports churn model training and incremental batch scoring using MySQL and Python, built from a Data Engineering perspective.

The system implements structured data modelling (raw → cleaned → feature), logical data freshness through SQL views, and separation of training and inference workflows. 

The project build a complete end-to-end customer churn prediction system integrating data engineering, machine learning (XGBoost), and Power BI visualization.


---

## Purpose

To demonstrate strong Data Engineering fundamentals, including layered modelling, data lineage awareness, and production-style batch inference design.

---

## Architecture

```
raw_customers (table)
    ↓
cleaned_customers (view)
    ↓
feature_customers (view)
    ↓
Model Training (Python)
    ↓
Saved Model (.pkl)
    ↓
Incremental Batch Inference
    ↓
churn_predictions (table)
```


## Project Structure

```
Customer-Churn-Data-Engineering-Pipeline/
│
│   ├── config/
│   │   ├── __init__.py
│   │   └── db_config.py
│
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   ├── train_model copy.py
│   │   └── predict.py
│
│   ├── models/
│   │   └── churn_model.pkl
│
│   ├── outputs/
│   │   └── wrong_predictions.csv
│
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── run_pipeline.py
│   │   ├── data_loader.py
│   │   ├── db_setup.py
│   │   ├── generate_new_customers.py
│   │   ├── reset_tables.py
│   │   ├── reset_predictions_table.py
│   │   └── check_counts.py
│
│   ├── sql/
│   │   ├── 01_create_db_churn_pipeline.sql
│   │   ├── 02_create_table_raw_customers.sql
│   │   ├── 03_create_view_cleaned_customers.sql
│   │   ├── 04_create_view_feature_customers.sql
│   │   └── 05_create_table_churn_predictions.sql
│
│   ├── dashboard.pbix
│   ├── dashboard.png
│   ├── data.csv
│   └── project_report.pdf
```

## Key Features

* Layered data architecture (raw → cleaned → feature)
* SQL views for dynamic data freshness
* Logistic Regression with class imbalance handling
* Model persistence using `joblib`
* Incremental, idempotent batch scoring
* Separation of training and inference pipelines

---

## Technology Stack

* Python
* MySQL
* Pandas
* Scikit-learn
* Joblib
* Power BI (Visualization)  


---

## Key Features
* End-to-end automated pipeline
* SQL + Python integration
* ML-based churn prediction
* Real-time prediction storage
* Business-focused dashboard

---

## How to Run

You can run this project in two ways:

###  Option 1: Run Full Pipeline (Recommended)
* First setup db_config
* Second run db.setup.py 
* Third run pipeline: python -m pipeline.run_pipeline
  
This will execute the entire workflow automatically:

This runs:
1. Reset tables  
2. Load data  
3. Train model  
4. Generate predictions  

---

### Option 2: Run Step-by-Step (Manual Execution)

#### 1. Setup Database
python -m pipeline.db_setup

#### 2. Reset Tables (Optional)
python -m pipeline.reset_tables
python -m pipeline.reset_predictions_table

#### 3. Load Data
python -m pipeline.data_loader

#### 4. Train Model
python -m ml.train_model

#### 5. Run Predictions
python -m ml.predict

#### 6. Check Data
python -m pipeline.check_counts

---

### Running Instructions File
You can also refer to:
run.txt


This file contains all commands required to execute the pipeline.

---

###  Pipeline Flow (run_pipeline.py)

The pipeline executes the following steps:

```python
print("Starting Pipeline")

reset_tables()
load_raw_data()
train_model()
run_predictions()

print("Pipeline completed successfully")

---



