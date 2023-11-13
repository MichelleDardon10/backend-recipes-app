import mysql.connector
from mysql.connector import Error


# Define a function to create a MySQL connectiong
def create_mysql_connection():
    connection = None
    try:
        # Attempt to create a connection to the MySQL database
        connection = mysql.connector.connect(
            host="172.17.0.2",
            user="root",
            password="password",
            database="recipes",
        )
        return connection
    except Error as e:
        # Handle any errors that occur during connection creation
        print(f"Error creating MySQL connection: {e}")
        return None


# crea las tablas
def create_tables(connection):
    cursor = connection.cursor()

    # Define the table creation SQL statements for your models
    table_creation_sql = [
        """
        CREATE TABLE IF NOT EXISTS tblrecipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            post_by VARCHAR(150),
            valoration FLOAT,
            image VARCHAR(255),
            category VARCHAR(150),
            destacado INT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tblrecipeingredients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ingredient_name VARCHAR(255) NOT NULL,
            recipe_id INT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES tblrecipes (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tblrecipecomments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            comment_text VARCHAR(300) NOT NULL,
            posted_by VARCHAR(150) NOT NULL,
            recipe_id INT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES tblrecipes (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tblrecipesteps (
            id INT AUTO_INCREMENT PRIMARY KEY,
            step_text VARCHAR(255) NOT NULL,
            recipe_id INT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES tblrecipes (id)
        )
        """,
    ]

    for sql in table_creation_sql:
        try:
            cursor.execute(sql)
            connection.commit()
        except Error as e:
            print(f"Error creating table: {e}")

    cursor.close()


# Function to insert a recipe into the database if it doesn't exist
def insert_recipe(recipe_data):
    connection = create_mysql_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Check if the recipe already exists in the database
        query = "SELECT id FROM tblrecipes WHERE id = %s"
        cursor.execute(query, (recipe_data["id"],))
        existing_recipe = cursor.fetchone()

        if existing_recipe:
            print(f"Recipe with ID {recipe_data['id']} already exists in the database.")
            return False
        else:
            # Insert the recipe into the database
            query = "INSERT INTO tblrecipes (id, name, post_by, valoration, image, category, destacado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                query,
                (
                    recipe_data["id"],
                    recipe_data["name"],
                    recipe_data["post_by"],
                    recipe_data["valoration"],
                    recipe_data["image"],
                    recipe_data["category"],
                    recipe_data["destacado"],
                ),
            )

            # Insert ingredients
            for ingredient_name in recipe_data["ingredients"]:
                query = "INSERT INTO tblrecipeingredients (ingredient_name, recipe_id) VALUES (%s, %s)"
                cursor.execute(query, (ingredient_name, recipe_data["id"]))

            # Insert comments
            for comment in recipe_data["comments"]:
                query = "INSERT INTO tblrecipecomments (comment_text, posted_by, recipe_id) VALUES (%s, %s, %s)"
                cursor.execute(
                    query,
                    (comment["comment_text"], comment["posted_by"], recipe_data["id"]),
                )

            # Insert steps
            for step_text in recipe_data["steps"]:
                query = (
                    "INSERT INTO tblrecipesteps (step_text, recipe_id) VALUES (%s, %s)"
                )
                cursor.execute(query, (step_text, recipe_data["id"]))

            connection.commit()
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error inserting recipe: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return False


# prueba webhook2
# por favor coca
