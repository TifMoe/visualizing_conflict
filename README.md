# visualizing_conflict
Explore Dash framework by creating a dashboard visualization of world conflict
Data from [ACLED](https://www.acleddata.com/about-acled/), accessed through [data.world](https://data.world/makeovermonday/2018w34-visualizing-conflict)

![dashboard example](https://github.com/TifMoe/visualizing_conflict/blob/master/static/dashboard2.0.png)

## Prerequisites
This application runs inside a Docker container. Please install Docker on your local machine before running. You can find a free version of Docker [here](https://www.docker.com/get-started).

## Setup
To build the Docker container with all the necessary dependencies and data to run this application, please enter the followin g command from the root of this project's directory:
```bash
# From the root of this project on your machine run:
$ docker build -t dashboards:first . # This will build the image

# You should see your new docker image listed here if the build was successful
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
dashboards          first               52d74ee14dc6        2 minutes ago       551MB
```
You should only ever need to run this once unless you are altering the source code

## Running the application
After you have cloned this repository and Docker is running and accessible from terminal run the following commands to build the docker image and run the application locally:

```bash
# This runs the container, you will see the id populate below
$ docker run -i -t -d -p 127.0.0.1:8000:5000 dashboards:first 
0ccb6fa460f74cac4ad2bbc388c437406f0576b21c7310442db9eb2687b986de

# This command will let you see all running containers so you can verify it's working
$ docker ps 
CONTAINER ID  IMAGE             COMMAND          CREATED          STATUS         PORTS                     NAMES
0ccb6fa460f7  dashboards:first  "python app.py"  20 seconds ago   Up 18 seconds  127.0.0.1:8000->5000/tcp  vigilant_perlman
```

After your docker container is running, you should be able to open a tab in your browser and navigate to your local host port 8000 to view the running application. **`http://127.0.0.1:8000/`**

To stop the container run:
```bash
$ docker stop 0ccb6fa460f7
```

## TODO
1) Move off of the default development server to a production server
2) Deploy dockerized web app to cloud server
3) Improve dashboard:
> - Optimize performance by caching or aggregating data before plotting
> - Capture state in clickable interactions to enable 'unclick' functionality
> - Aggregate conflicts to city level for map (after other filters applied) and size by count
