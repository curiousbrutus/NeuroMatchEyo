# IN4110 strømpris assignment 5

## Introduction

This project focuses on creating a web-based visualization of energy prices in Norway using the Hva Koster Strømmen API. Users can interact with the data through a web interface built with FastAPI, Altair for visualization, Pandas for data manipulation, and Requests for API requests.

## Install dependencies:

'''
pip install -r requirements.txt
'''

## Dependencies

All the dependencies required to run this project:

- Python 3.x
- FastAPI
- Altair
- Pandas
- Requests

## Testing
Terminal in the assignment5 directory write
'''
pytest -v tests/
'''

## Bonus task Klima (which was really tangled for me) 

Are implemented in separate files located in the klima directory.

You can run it:
'''
python app.py
'''


## Project Structure 

assignment5/
├── klima
├── app.py
├── strompris.py
├── templates
├── requirements.txt
├── pyproject.toml
├── http_cache.sqlite
├── venv/
└── README.md

( There is more than these files that i mention but these are most important ones. For seeing the files you can run ''' tree ''' in terminal)

- app.py: Contains the FastAPI application logic.
- strompris.py: Utility functions for retrieving electricity prices.
- templates/: HTML templates for the FastAPI application.
- klima: Contains bonus task for global temperatures.

