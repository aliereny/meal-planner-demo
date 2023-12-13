# Meal Planner
## Description
This is a meal planner app that allows users to create a weekly meal plan and generate a shopping list based on the recipes they have selected. Users can also add their own recipes to the database and edit or delete them as needed.
## Installation
In this project we use pipenv. To install pipenv, run the following command in your terminal:
```
pip install pipenv
```
To install the dependencies for this project, run the following command in your terminal:
```
pipenv install
```
## Usage
To run the app, run the following command in your terminal:
```
streamlit run main.py
```
## Engine
This project was built using Python 3.11. The dependencies for this project are listed in the Pipfile.

## Environment Variables
This project uses environment variables to connect to the database. To run this project locally, you will need to create a .env file in the root directory and add the following variables:
```
OPENAI_API_KEY = "your_openai_api_key"
```