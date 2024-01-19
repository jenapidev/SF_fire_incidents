# Project description 
Project for extracting and standarizing data from the san francisco fire department. includes a summary of each (non-medical) incident to which the SF Fire Department responded. Each incident record includes the call number, incident number, address, number and type of each unit responding, call type (as determined by dispatch), prime situation (field observation), actions taken, and property loss.
### Data Source
[sfgov.org](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data)

# Depends
This project relies on python, postgreSQL and Docker (optional)

# Setting up
## using docker
run
'''
    $ docker-compose up
'''

## using pip
### this requires to use .env or any other environment variables library such as direnv 

install dependencies with pip
'''
pip install -r non-docker-requirements.txt
'''

create .env file following .env.example with the variables of the database

Create db schema 
'''
    python setup.py
'''
run ETL process 
'''
    python main.py
'''

# Inspecting the data
## Using docker
you have containers of jupyter notebooks, postgrSQL, and pgadmin. This allowing you to inspect all the project's ETL efectiveness and data integrity
- to use jupyter type http://localhost:8888/?token=easy in the searchbar and use the data_exploring .ipynb
- to use pgadmin type http://localhost:5050 in the searchbar and login as user: admin@admin password: admin

## without docker
it's higly recomended to use docker to avoid any further inconvenience produced by the instalation process of any of the recomended tools to inspect the data flow


# Process of planning and thinking
## Data understanding
The propouse of the project is to create a functional Pipeline with data extraction, data transforms, and loading the processed data into a wharehouse.

SF.gov/API ----> ETL ----------------------------------> Reporting
                    |----> Data extraction                  (report made with powerBI to filter incidents by date and by Battalion)
                    |----> Data transforms
                    |           |
                    |           |------> Data standarization
                    |           |------> Data modeling
                    |                       (model data into dimensions and facts structure for Wharehousing)
                    |
                    |------------------> Data uploading into wharehouse system
