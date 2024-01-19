# Data pipeline for Fire Incidents analysis

## Project Overview

### San Francisco Fire Department Data Standardization 

### Description
This project focuses on extracting and standardizing data from the San Francisco Fire Department. It aims to provide a comprehensive overview of each non-medical incident responded to by the SF Fire Department. The dataset includes detailed records such as call numbers, incident numbers, addresses, responding unit types and numbers, dispatch-determined call types, field observations, actions taken, and property loss assessments.

### Objective
Our primary objective is to develop a robust and efficient data pipeline that allows for the extraction, transformation, and loading (ETL) of this valuable data into a data warehouse, enabling deeper insights and analysis.

### Data Source
For detailed incident data, we utilize the publicly available dataset from the San Francisco government's website: [Fire Incidents Data](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data)

## Project Dependencies
This project is built using several key technologies:
- **Python**: For scripting and running the ETL processes.
- **PostgreSQL**: As the database management system.
- **Docker**: Optional, for containerization and easy deployment.

## Setting Up the Project

### Using Docker (Recommended)
To initiate the project with Docker, simply run the following command:
```
$ docker-compose up
```

### Using Python and Pip (Non-Docker Setup)
For a non-Docker setup, follow these steps:

1. **Install Dependencies**:
   Install necessary Python packages using pip:
   ```
   pip install -r non-docker-requirements.txt
   ```

2. **Database Configuration**:
   - Create a `.env` file based on the provided `.env.example`.
   - Fill in the database variables as per your setup.

3. **Database Schema Creation**:
   Set up the database schema using:
   ```
   python setup.py
   ```

4. **Running the ETL Process**:
   Execute the ETL process by running:
   ```
   python main.py
   ```

## Data Inspection and Analysis

### With Docker
The project includes Docker containers configured for Jupyter Notebooks, PostgreSQL, and PgAdmin. These tools facilitate the inspection and analysis of the ETL process and data integrity.

- **Jupyter Notebooks**: Access by navigating to `http://localhost:8888/?token=easy`. Use the `data_exploring.ipynb` notebook for data analysis.
- **PgAdmin**: Access PgAdmin at `http://localhost:5050`. Login with the credentials `user: admin@admin` and `password: admin`.

### Without Docker
It is strongly recommended to use Docker to avoid complications arising from the installation of the recommended tools for data analysis. However, alternative methods can be explored based on individual setup and preferences.

## Project Methodology

### Understanding the Data
The project is centered around creating a functional and efficient data pipeline. The stages include:

1. **Data Extraction**: Acquiring data from the specified source.
2. **Data Transformation**: Standardizing and processing the data for analytical readiness.
3. **Data Loading**: Storing the processed data in a data warehouse for further analysis.

---

SF.gov/API ----> ETL ----------------------------------> Reporting
                    |----> Data extraction                  (report made with powerBI to filter incidents by date and by Battalion)
                    |----> Data transforms
                    |           |
                    |           |------> Data standarization
                    |           |------> Data modeling
                    |                       (model data into dimensions and facts structure for Wharehousing)
                    |
                    |------------------> Data uploading into wharehouse system
```
