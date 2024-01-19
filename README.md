Certainly! I'll integrate this data flow diagram into the enhanced README.md to provide a clearer visual representation of the project's ETL process. This addition will help users understand the sequential steps and components involved in the data pipeline.

---

# Enhanced README.md with Data Flow Diagram

## Project Overview

### Title: San Francisco Fire Department Data Standardization and Extraction

### Description
This project aims to extract, standardize, and analyze data from the San Francisco Fire Department, focusing on non-medical incidents. It involves a detailed ETL process to ensure data quality and usability for reporting purposes, particularly in PowerBI.

### Objective
To develop a comprehensive data pipeline for extracting, transforming, and loading (ETL) incident data, enabling advanced analysis and insights through a structured data warehouse.

### Data Source
Incident data is sourced from the San Francisco government's public dataset: [Fire Incidents Data](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data)

## Project Dependencies
- **Python**
- **PostgreSQL**
- **Docker** (optional)

## Setting Up the Project

### Using Docker
Run:
```
$ docker-compose up
```

### Using Python and Pip (Non-Docker)
1. Install dependencies:
   ```
   pip install -r non-docker-requirements.txt
   ```

2. Configure database using `.env` file as per `.env.example`.

3. Create database schema:
   ```
   python setup.py
   ```

4. Run ETL process:
   ```
   python main.py
   ```

## Data Inspection and Analysis

### With Docker
- **Jupyter Notebooks**: `http://localhost:8888/?token=easy` 
- **PgAdmin**: `http://localhost:5050` (Credentials: `admin@admin` / `admin`)

### Without Docker
Using Docker is recommended to avoid setup complexities.

## Data Flow Diagram

The ETL process consists of several key stages, each critical to the data pipeline's success:

1. **Data Extraction**: 
   - Source: `SF.gov/API`

2. **Data Transformation**: 
   - Data Standardization
   - Data Modeling (structuring data into dimensions and facts for warehousing)

3. **Data Loading**:
   - Uploading processed data into the warehouse system

4. **Reporting**:
   - Utilizing PowerBI for creating reports to filter incidents by date and Battalion

```
SF.gov/API ----> ETL ----------------------------------> Reporting
                                      |----> Data extraction                  
                                      |                                                                  
                                      |----> Data transforms
                                      |           |
                                      |           |------> Data standardization
                                      |           |------> Data modeling
                                      |
                                      |------------------> Data uploading into wharehouse system
```