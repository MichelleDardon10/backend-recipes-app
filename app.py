# Import necessary modules from Flask framework
import sys

from flask import Flask, jsonify, request
import mysql.connector
# Import the create_tables function from the models module
from models import create_tables, create_mysql_connection
# Import the insert_recipe function from the models module
from models import insert_recipe
from mysql.connector import Error
import os
import json
from flask_cors import CORS

# Create a Flask application
app = Flask(__name__)
CORS(app)

# Define a route for retrieving all recipes
@app.route("/recipes", methods=["GET"])
def get_recipes():
    connection = create_mysql_connection()
    if not connection:
        # If connection fails, return an error message in JSON format
        return jsonify({"error": "Unable to connect to the database"})

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM tblrecipes"
    cursor.execute(query)
    recipes = cursor.fetchall()
    cursor.close()
    connection.close()

    for recipe in recipes:
        # Add ingredients, comments, and steps to each recipe entry
        recipe["ingredients"] = get_recipe_ingredients(recipe["id"])
        recipe["comments"] = get_recipe_comments(recipe["id"])
        recipe["steps"] = get_recipe_steps(recipe["id"])

    # Return the list of recipes in JSON format
    return jsonify({"recipes": recipes})


@app.route('/search', methods=['GET'])
def search_recipes():
    search_query = request.args.get('term', '').lower()
    print("query: " + search_query)
    connection = create_mysql_connection()
    if not connection:
        return jsonify({'error': 'Unable to connect to the database'})

    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM tblrecipes WHERE name LIKE '{search_query}'"

    print(query)

    cursor.execute(query)

    matching_recipes = cursor.fetchall()
    cursor.close()
    connection.close()

    for recipe in matching_recipes:
        # Add ingredients, comments, and steps to each recipe entry
        recipe["ingredients"] = get_recipe_ingredients(recipe["id"])
        recipe["comments"] = get_recipe_comments(recipe["id"])
        recipe["steps"] = get_recipe_steps(recipe["id"])

    # Return the list of recipes in JSON format
    return jsonify({"recipes": matching_recipes})

# Function to get ingredients for a recipe
def get_recipe_ingredients(recipe_id):
    connection = create_mysql_connection()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM tblrecipeingredients WHERE recipe_id = {recipe_id}"
    cursor.execute(query)
    ingredients = cursor.fetchall()
    cursor.close()
    connection.close()
    return ingredients


# Function to get comments for a recipe
def get_recipe_comments(recipe_id):
    connection = create_mysql_connection()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM tblrecipecomments WHERE recipe_id = {recipe_id}"
    cursor.execute(query)
    comments = cursor.fetchall()
    cursor.close()
    connection.close()
    return comments


# Function to get steps for a recipe
def get_recipe_steps(recipe_id):
    connection = create_mysql_connection()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM tblrecipesteps WHERE recipe_id = {recipe_id}"
    cursor.execute(query)
    steps = cursor.fetchall()
    cursor.close()
    connection.close()
    return steps


# Function to read and parse the JSON data from a file
def read_json_file(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


# Run the setup code before starting the Flask app
# Define the path to the JSON file
json_file_path = os.path.join("backup-data", "Data.json")

# Read the recipes data from the JSON file
recipes_data = read_json_file(json_file_path)
connection = create_mysql_connection()
print("connection")
if connection:
    # Create database tables if the connection is successful
    create_tables(connection)
    print("tables created")
    connection.close()

    # Loop through the recipe data and insert each recipe into the database
    for recipe_data in recipes_data:
        if insert_recipe(recipe_data):
            print(f"Recipe with ID {recipe_data['id']} has been inserted into the database.")
        else:
            print(f"Recipe with ID {recipe_data['id']} already exists in the database or an error occurred.")
    connection.close()


# Start the Flask application
print("Starting the application...")
app.run(host="0.0.0.0", port=5001, debug=True)
