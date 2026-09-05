\# System Architecture



\## Overview



The Cloud Infrastructure Data Pipeline is a Python-based ETL pipeline that

uses Amazon S3 as the cloud storage layer.



The pipeline performs the following operations:



1\. Reads customer CSV data.

2\. Uploads raw data to Amazon S3.

3\. Downloads the raw data from S3.

4\. Loads the data using Pandas.

5\. Validates and transforms the customer records.

6\. Removes duplicates and invalid records.

7\. Creates customer spending segments.

8\. Saves the processed dataset locally.

9\. Uploads the processed dataset to Amazon S3.

10\. Logs pipeline execution details.

11\. Runs automated tests through GitHub Actions.



\---



\## Architecture Diagram



```mermaid

flowchart TD

&#x20;   A\[Customer CSV] --> B\[Python ETL Pipeline]



&#x20;   B --> C\[Upload Raw Data]

&#x20;   C --> D\[Amazon S3 Raw Layer]



&#x20;   D --> E\[Download Raw Data]

&#x20;   E --> F\[Load CSV with Pandas]



&#x20;   F --> G\[Validate Data]

&#x20;   G --> H\[Transform Data]



&#x20;   H --> I\[Remove Duplicates]

&#x20;   I --> J\[Validate Email and Spend]

&#x20;   J --> K\[Create Customer Segments]



&#x20;   K --> L\[Processed CSV]

&#x20;   L --> M\[Amazon S3 Processed Layer]



&#x20;   B --> N\[Application Logging]

&#x20;   B --> O\[Pytest Tests]



&#x20;   O --> P\[GitHub Actions CI]

