☁️ Cloud-Based ETL Data Engineering Pipeline











An end-to-end cloud-based Python ETL pipeline that extracts customer data, validates and transforms records, stores raw and processed datasets in Amazon S3, and automatically validates the codebase using Pytest and GitHub Actions.

📌 Overview

This project demonstrates the design and implementation of a modular cloud-based ETL (Extract, Transform, Load) data pipeline using Python and AWS.

The pipeline takes customer data through a controlled processing workflow:

Extract customer data from CSV.
Upload the raw dataset to Amazon S3.
Download the raw dataset from S3.
Load the data into Pandas.
Validate the dataset schema and data quality.
Clean and transform customer records.
Remove duplicates and invalid records.
Create customer spending segments.
Save the processed dataset locally.
Upload the processed dataset to Amazon S3.
Run automated tests using Pytest.
Validate code changes through GitHub Actions.

The project follows a modular architecture with separate components for:

Data ingestion
Data transformation
Cloud storage
Configuration
Logging
Testing
Continuous integration
🎯 Project Objectives

The primary objectives of this project are to:

Build a reusable Python ETL pipeline
Integrate Python with Amazon S3 using Boto3
Separate raw and processed data layers
Implement data validation and quality checks
Clean and standardize customer records
Remove duplicate and invalid records
Create customer spending segments
Implement modular software architecture
Add automated testing with Pytest
Use mocked AWS operations for CI testing
Implement GitHub Actions continuous integration
Manage configuration through environment variables
Follow basic cloud security practices
Create a foundation for future production deployment
🏗️ System Architecture
flowchart TD
    A["Customer CSV"] --> B["Python ETL Pipeline"]

    B --> C["Upload Raw Data"]
    C --> D["Amazon S3 Raw Layer"]

    D --> E["Download Raw Data"]
    E --> F["Load with Pandas"]

    F --> G["Data Validation"]
    G --> H["Data Transformation"]

    H --> I["Clean Customer Data"]
    I --> J["Customer Segmentation"]

    J --> K["Processed CSV"]
    K --> L["Amazon S3 Processed Layer"]

    B --> M["Application Logging"]
    B --> N["Pytest Tests"]

    N --> O["GitHub Actions CI"]

For a detailed explanation of the architecture and design decisions, see:

docs/architecture.md

🔄 End-to-End ETL Workflow
1. Extract

The pipeline begins with the customer dataset stored in:

sample_data/customers.csv

The sample dataset contains customer information including:

Customer ID
Name
Email
Country
Signup date
Spend

The source dataset is uploaded to Amazon S3 before processing.

2. Store Raw Data

The original dataset is uploaded to the S3 raw layer:

s3://<bucket-name>/raw/customers.csv

The raw layer preserves the source data before transformation.

This creates a clear separation between:

Raw Data
    ↓
Processed Data
3. Ingest Data

The pipeline downloads the raw dataset from Amazon S3 and stores it locally:

data/raw/customers.csv

The ingestion functionality is implemented in:

src/ingestion/csv_ingestion.py

The ingestion layer:

Checks whether the input file exists
Loads the CSV using Pandas
Reports the number of rows and columns
Returns a Pandas DataFrame
4. Validate Data

Before transformation, the dataset is validated.

Required columns include:

customer_id
name
email
country
signup_date
spend

The validation layer checks for:

Missing required columns
Invalid email formats
Invalid spending values
Missing required values
Invalid dates
Negative spending
Duplicate customer records
5. Transform Data

The transformation logic is implemented in:

src/transformation/etl.py

The transformation process includes:

Email Normalization

Email addresses are converted to lowercase and unnecessary whitespace is removed.

Example:

 USER@EXAMPLE.COM

becomes:

user@example.com
Name and Country Standardization

Leading and trailing whitespace is removed from text fields.

Date Conversion

Signup dates are converted into datetime values.

Invalid dates are handled safely during processing.

Numeric Conversion

Customer spending values are converted into numeric values.

Invalid values are identified during validation.

Duplicate Removal

Duplicate customer records are removed using:

customer_id
Invalid Record Removal

Records missing required values are removed from the final processed dataset.

Negative Spend Removal

Negative spending values are excluded from the final dataset.

💰 Customer Segmentation

The pipeline creates customer spending segments based on customer spend.

Segment	Spending Range
Low	$0 - $500
Medium	$500 - $1,000
High	$1,000 - $2,000
Premium	$2,000+

This demonstrates how an ETL pipeline can perform not only data cleaning but also basic business-oriented transformation.

☁️ Amazon S3 Architecture

Amazon S3 is used as the cloud storage layer.

The bucket is organized into two logical data layers:

S3 Bucket
│
├── raw/
│   └── customers.csv
│
└── processed/
    └── customers_processed.csv
Raw Layer
raw/customers.csv

Contains the original source dataset.

Processed Layer
processed/customers_processed.csv

Contains the validated and transformed dataset.

This structure provides a simple foundation for a data-lake-style architecture.

💾 Local Data Flow

The pipeline also maintains local copies during execution:

sample_data/
└── customers.csv
        │
        ▼
data/raw/
└── customers.csv
        │
        ▼
ETL Transformation
        │
        ▼
data/processed/
└── customers_processed.csv

The processed dataset is subsequently uploaded to Amazon S3.

🛠️ Technology Stack
Technology	Purpose
Python 3.11+	Core programming language
Pandas	Data loading and transformation
Boto3	AWS SDK for Python
Amazon S3	Cloud object storage
Pytest	Automated testing
unittest.mock	Mocking AWS operations during tests
Git	Version control
GitHub	Source-code hosting
GitHub Actions	Continuous integration
python-dotenv	Environment configuration
Python Logging	Pipeline monitoring and diagnostics
📂 Project Structure
cloud-infrastructure-data-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── architecture.md
│   └── images/
│       ├── pipeline-run.png
│       └── tests-passed.png
│
├── sample_data/
│   └── customers.csv
│
├── data/
│   ├── raw/
│   │   └── customers.csv
│   │
│   └── processed/
│       └── customers_processed.csv
│
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── csv_ingestion.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── s3.py
│   │
│   ├── transformation/
│   │   ├── __init__.py
│   │   └── etl.py
│   │
│   ├── config.py
│   └── logger.py
│
├── tests/
│   ├── __init__.py
│   ├── test_etl.py
│   └── test_s3.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run_pipeline.py
📁 Directory Responsibilities
src/

Contains the main application and ETL processing logic.

src/ingestion/

Contains functionality for loading source data.

src/transformation/

Contains validation, cleaning, transformation, and customer segmentation logic.

src/storage/

Contains Amazon S3 integration functionality.

src/config.py

Loads environment-based configuration.

src/logger.py

Provides application logging.

tests/

Contains automated unit tests.

data/

Contains local raw and processed datasets generated or used during development.

sample_data/

Contains reproducible sample input data.

docs/

Contains architecture and supporting project documentation.

.github/workflows/

Contains GitHub Actions automation.

⚙️ Configuration

The pipeline uses environment variables rather than hard-coding environment-specific settings.

The following configuration values are used:

AWS_REGION
S3_BUCKET_NAME
S3_RAW_PREFIX
S3_PROCESSED_PREFIX

Example:

AWS_REGION=us-east-2
S3_BUCKET_NAME=your-bucket-name
S3_RAW_PREFIX=raw/
S3_PROCESSED_PREFIX=processed/

The repository includes:

.env.example

as a configuration template.

The actual .env file should remain local.

🔐 Security

Security is considered throughout the project.

The project follows these practices:

AWS credentials are not stored in source code.
.env is excluded through .gitignore.
Environment variables are used for configuration.
AWS operations are performed through Boto3.
CI unit tests mock AWS API operations.
GitHub Actions does not require personal AWS credentials to execute the unit test suite.
Production deployments should use IAM roles and temporary credentials where possible.

Never commit AWS access keys, secret keys, passwords, API keys, or other credentials to GitHub.

▶️ Getting Started
Prerequisites

Install the following:

Python 3.11 or newer
Git
AWS account
Amazon S3 bucket
AWS credentials configured through a supported credential provider
1. Clone the Repository
git clone https://github.com/Niha-23/cloud-infrastructure-data-pipeline.git

Navigate into the project:

cd cloud-infrastructure-data-pipeline
2. Create a Virtual Environment
Windows
python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv .venv

Activate it:

source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a local .env file based on .env.example.

Windows
copy .env.example .env
macOS / Linux
cp .env.example .env

Update .env with your AWS and S3 configuration.

Example:

AWS_REGION=us-east-2
S3_BUCKET_NAME=your-bucket-name
S3_RAW_PREFIX=raw/
S3_PROCESSED_PREFIX=processed/
☁️ AWS Setup

The project uses Amazon S3 for cloud storage.

Create an S3 bucket in the AWS region configured in your .env file.

The pipeline expects the following logical prefixes:

raw/
processed/

The application creates and accesses objects using these prefixes.

No AWS access keys should be stored inside the repository.

▶️ Running the Pipeline

Run the complete pipeline from the project root:

python run_pipeline.py

The pipeline performs:

Customer CSV
     ↓
Upload Raw Data
     ↓
Amazon S3 Raw Layer
     ↓
Download Raw Data
     ↓
Load with Pandas
     ↓
Validate Data
     ↓
Transform Data
     ↓
Create Customer Segments
     ↓
Save Processed CSV
     ↓
Upload to S3 Processed Layer
     ↓
Pipeline Complete
📊 Pipeline Output

The processed dataset is written locally to:

data/processed/customers_processed.csv

It is also uploaded to Amazon S3:

processed/customers_processed.csv

The application logs:

Pipeline start
S3 upload
S3 download
Data loading
Transformation
Output row counts
Processed data upload
Pipeline completion
🧪 Testing

The project uses Pytest for automated testing.

Run:

pytest

For detailed output:

pytest -v

The test suite validates the core ETL and S3 storage functionality.

ETL Tests

The ETL test suite covers:

Duplicate customer removal
Email normalization
Customer segmentation
Missing required columns
Invalid spend handling
S3 Tests

The S3 test suite covers:

S3 storage behavior
File existence checks
File download behavior

The AWS operations are mocked using Python's unittest.mock.

This allows the tests to run without requiring AWS credentials.

🔄 Continuous Integration

The project uses GitHub Actions for continuous integration.

The workflow is located at:

.github/workflows/ci.yml

The CI pipeline runs automatically when code is pushed to main or when a pull request targets main.

The workflow performs:

Git Push / Pull Request
          ↓
Checkout Repository
          ↓
Set Up Python
          ↓
Install Dependencies
          ↓
Run Pytest
          ↓
Pass / Fail

The CI pipeline helps detect regressions automatically and provides a repeatable validation process for code changes.

🧪 Testing Strategy

The project uses unit testing with mocked cloud interactions.

This provides two important advantages.

Fast Execution

Tests do not need to make network requests to Amazon S3.

Secure CI

GitHub Actions does not need personal AWS credentials simply to execute unit tests.

The tests therefore focus on verifying application behavior while keeping external infrastructure dependencies isolated.

📝 Logging

Application logging is implemented in:

src/logger.py

The pipeline records important execution events.

Examples include:

Starting customer data pipeline.

Uploading raw data to S3.

Downloading raw data from S3.

Loading CSV data.

Transforming customer records.

Saving processed data.

Uploading processed data to S3.

Pipeline completed successfully.

Logging also provides information about input and output row counts and operational errors.

🧩 Engineering Practices
Modular Architecture

The application separates:

Configuration
Data ingestion
Data transformation
Cloud storage
Logging
Testing

This makes individual components easier to maintain and test.

Separation of Concerns

S3 operations are separated from ETL transformation logic.

This allows the transformation layer to be tested independently from the cloud storage implementation.

Configuration Management

Environment-specific configuration is stored outside application code.

Automated Testing

Core pipeline behavior is covered by automated tests.

Continuous Integration

GitHub Actions automatically executes the test suite after repository changes.

Reproducibility

Sample data and dependency definitions allow the project to be recreated in a new development environment.

Cloud Integration

Amazon S3 is integrated through Boto3 to provide cloud-based storage for raw and processed datasets.

📸 Project Screenshots
Pipeline Execution




Automated Tests




📈 Current Project Capabilities

The current implementation provides:

Python ETL pipeline

CSV ingestion

Data validation

Data cleaning

Duplicate detection and removal

Email normalization

Date conversion

Spend validation

Customer segmentation

Amazon S3 integration

Raw data storage

Processed data storage

Application logging

Automated Pytest tests

Mocked S3 tests

GitHub Actions CI

Environment-based configuration

Security-conscious credential handling

Architecture documentation

☁️ Cloud Engineering Roadmap

The current project provides a foundation that can be expanded into a more production-oriented cloud data platform.

Potential future architecture:

                    Data Source
                        │
                        ▼
                  Amazon S3 Raw
                        │
                        ▼
                  ETL Processing
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
         Validation          Transformation
              │                   │
              └─────────┬─────────┘
                        ▼
                Amazon S3 Processed
                        │
                        ▼
                Analytics Layer

Future cloud capabilities may include:

AWS Lambda
Amazon EventBridge
AWS Glue
Amazon CloudWatch
Terraform
IAM role-based authentication
Data cataloging
Data-quality monitoring
Workflow orchestration
Analytics and BI integration
🚀 Future Improvements

Planned enhancements include:

Increase automated test coverage

Add test coverage reporting

Add advanced data-quality checks

Add pipeline metrics

Add structured logging

Add CloudWatch monitoring

Add automated pipeline scheduling

Add AWS Lambda execution

Add EventBridge scheduling

Add Infrastructure as Code using Terraform

Add Parquet output

Add data-quality reporting

Add analytics/BI integration

Add production deployment architecture

Add pipeline alerting

🎓 Skills Demonstrated
Programming
Python
Pandas
Modular programming
Exception handling
Environment configuration
Logging
Data Engineering
ETL pipeline design
Data ingestion
Data validation
Data cleaning
Data transformation
Data quality
Customer segmentation
Raw and processed data layers
Cloud
AWS
Amazon S3
Boto3
Cloud storage architecture
AWS configuration
Cloud security fundamentals
Testing
Pytest
Unit testing
Mocking
Test isolation
Regression testing
DevOps
Git
GitHub
GitHub Actions
Continuous Integration
CI/CD concepts
Software Engineering
Modular architecture
Separation of concerns
Configuration management
Logging
Documentation
Reproducible development environments
Version control
💡 Why This Project?

Modern data engineering requires more than simply transforming a CSV file.

This project demonstrates how a data-processing application can be structured as a maintainable cloud-based system with:

Clear separation of responsibilities
Cloud object storage
Data validation
Data transformation
Automated testing
Continuous integration
Environment-based configuration
Security-conscious development practices
Technical documentation

The architecture is intentionally modular so that the project can evolve from a local Python application into a more complete cloud-native data platform.

👩‍💻 Author
Niharika

Software Engineer | Cloud & Data Engineering

GitHub:
https://github.com/Niha-23

⭐ Project

If you find this project useful, feel free to explore the repository and follow its development as it evolves toward a production-oriented cloud data engineering platform.

📄 License

This project is intended for educational and portfolio purposes.