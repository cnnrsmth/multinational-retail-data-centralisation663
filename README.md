# Sales Data Centralization Project

![Sales Data Banner](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHJudzcxNjQwbHc4ZWJ5cDAwYmNkbG1kamJhZnRtNnN0N2psZDM2ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5n5XtiSL93rVKCN2oy/giphy.gif)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Introduction

Welcome to the Sales Data Centralization Project! This project is a part of the AI Core program. The goal of this project is to centralize the sales data from multiple sources into a single database, making it easily accessible and analysable. This centralized database will act as a single source of truth for the company's sales data, enabling more data-driven decisions.

### What It Does

The project extracts sales data from various sources, cleans and transforms it, and then loads it into a centralized database. This system ensures that the sales data is consistent, accurate, and up-to-date.

### Aim of the Project

- **Centralize Sales Data:** Consolidate data from multiple sources into a single database.
- **Ensure Data Quality:** Clean and transform the data to ensure its accuracy and consistency.
- **Enable Data-Driven Decisions:** Provide a reliable source of sales data for analysis and decision-making.

### What You Learned

- Data extraction from various sources.
- Data cleaning and transformation techniques.
- Database interaction and data loading.
- Writing reusable and maintainable Python code.

## Features

- **Data Extraction:** Extracts data from various sources such as AWS RDS, CSV files, and JSON files.
- **Data Cleaning:** Cleans and transforms the data to ensure consistency and accuracy.
- **Data Loading:** Loads the cleaned data into a centralized database.
- **Automated Pipeline:** Automates the entire process from extraction to loading.

## Project Structure

```sh
sales-data-centralization/
├── __pycache__                   # Compiled bytecode files
├── .gitignore                    # Git ignore file
├── data_cleaning.py              # Contains the DataCleaning class with data cleaning methods
├── data_extraction.py            # Contains the DataExtraction class with data extraction methods
├── database_utils.py             # Contains the DatabaseConnector class for database interactions
├── requirements.txt              # List of required packages
├── task1main.py                  # Main script for task 1 (card details ETL)
├── task2main.py                  # Main script for task 2 (card details ETL)
├── task3main.py                  # Main script for task 3 (cleaning store data)
├── task4main.py                  # Main script for task 4 (completion of task 6)
├── task5main.py                  # Main script for task 5 (task 7)
├── task6main.py                  # Main script for task 6 (task 8 complete)
├── README.md                     # Project documentation
├── local_db_creds.yaml           # Local database credentials (not included in the repository)
├── aws_db_creds.yaml             # AWS RDS credentials (not included in the repository)
```
