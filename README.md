### Recipes Backend

### STEP 1: you need to get the mysql-container ip
If you follow the instructions from the mysql_docker the container name will be `` my-mysql-container ``
You run the following command:
```
docker inspect -f '{{.NetworkSettings.IPAddress}}' my-mysql-container  
```
and it will display an ip in the console.
### STEP 2: Replace the ip in to the connection host 
Copy the ip and put it in the host field, like this:
```
connection = mysql.connector.connect(
            host="ip-that-appeared-in-the-console",
            user="root",
            password="password",
            database="recipes",
        )
```
this code you can find it in ``models.py``

### STEP 3: Build the dockerfile
Build the Docker image from the Dockerfile (assuming the Dockerfile is saved as Dockerfile in your project directory):
``` bash
docker build -t backend .
```
- ``docker build``: This is the Docker command for building a Docker image. You use this command to create a new Docker image based on the instructions provided in a Dockerfile.
- ``-t backend``: The -t flag is used to specify a tag for the image. The tag is a user-friendly name for the image. In this case, you're naming the image "backend" Tags are often used to identify and version Docker images.
- ``.``: The period (dot) at the end of the command tells Docker to look for the Dockerfile in the current directory. This is where Docker will find the instructions for building the image.

### STEP 4: Run the container


Run the backend container:
````bash
docker run -d -p5001:5001 --name backend backend
````
docker run: This command is used to create and start a new Docker container based on a specified Docker image.
- ``-d``: This flag runs the container in detached mode, meaning it runs in the background. This allows you to continue using your terminal for other tasks without it being tied to the running container.
- ``-p 5001:5001``: This flag specifies port mapping. It maps port 5001 from the container to port 5001 on the host machine. In other words, if your Flask app inside the container is listening on port 5001, you can access it on your host machine using http://localhost:5001.
- ``--name backend``: This flag specifies a name for the container. In this case, the container will be named "backend."
- ``backend``: This is the name of the Docker image that you want to run as a container. It's assumed that you have already built or pulled the "backend" Docker image.

### STEP 5: Test your enpoint!
Go to any browser and try to access it!
```
http://127.0.0.1:5001/recipes
```
should return a list of recipes!


