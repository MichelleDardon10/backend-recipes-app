# Use the official MySQL image as a base image
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=recipes

# Expose the MySQL port
EXPOSE 3306

# Create a directory for MySQL data persistence
RUN mkdir -p /var/lib/mysql-persistent

# Define a volume for MySQL data
VOLUME /var/lib/mysql-persistent
