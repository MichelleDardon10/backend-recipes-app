## MySQL Docker


### Step1: Build Docker Image
Build the Docker image from the Dockerfile (assuming the Dockerfile is saved as Dockerfile in your project directory):
``` bash
docker build -t my-mysql-image .
```
- ``docker build``: This is the Docker command for building a Docker image. You use this command to create a new Docker image based on the instructions provided in a Dockerfile.
- ``-t my-mysql-image``: The -t flag is used to specify a tag for the image. The tag is a user-friendly name for the image. In this case, you're naming the image "my-mysql-image." Tags are often used to identify and version Docker images.
- ``.``: The period (dot) at the end of the command tells Docker to look for the Dockerfile in the current directory. This is where Docker will find the instructions for building the image.
### Step 2: Create a Local Directory
Create a directory on your local computer where MySQL data will be persisted. For example, create a directory named mysql-data in your home directory:
```` bash
mkdir ~/mysql-data
````
### Step 3: Run the MySQL Container
Run the MySQL container with the volume mounted to your local folder:
````bash
docker run -d --name my-mysql-container -p 3306:3306 -v ~/mysql-data:/var/lib/mysql-persistent my-mysql-image
````

-`` docker run``: This is the Docker command for running a container based on a Docker image.
- ``-d``: The -d flag stands for "detached" mode. It runs the container in the background, allowing you to continue using your terminal without being attached to the container's console.
- ``--name my-mysql-container``: The --name flag is used to specify a name for the container. In this case, you're naming the container "my-mysql-container."
- ``-p 3306:3306``: The -p flag is used to specify port mapping. In this case, it maps port 3306 from the host to port 3306 inside the container. This is necessary to allow your local computer to connect to the MySQL server running in the container.
- ``-v ~/mysql-data``:/var/lib/mysql-persistent: The -v flag is used to create a volume. It binds a local directory to a directory inside the container. In this case, it's binding the local directory ~/mysql-data to /var/lib/mysql-persistent inside the container. This volume ensures that the MySQL data is persisted on your local machine in the mysql-data directory.
- ``my-mysql-image``: This is the name of the Docker image that you want to use to create the container. It refers to the image you built using the docker build command and tagged as "my-mysql-image."

