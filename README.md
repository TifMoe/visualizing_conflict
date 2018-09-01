# visualizing_conflict
Explore Dash framework for creating visualization of world conflict
Data from the [ACLED](https://www.acleddata.com/about-acled/), accessed through [data.world](https://data.world/makeovermonday/2018w34-visualizing-conflict)

![dashboard example](https://github.com/TifMoe/visualizing_conflict/blob/master/static/dashboard2.0.png)

## Prerequisites
This application runs inside a Docker container. Please install Docker on your local machine before running. You can find a free version of Docker [here](https://www.docker.com/get-started).

## Running the application
After you have cloned this repository and Docker is running and accessible from terminal run the following commands to build the docker image and run the application locally:

```bash
# From the root of this project on your machine run:
$ docker build -t dashboards:first . # This will build the image

$ docker run -i -t -d -p 127.0.0.1:8000:5000 dashboards:first # This runs the container, you will see the id populate below
0ccb6fa460f74cac4ad2bbc388c437406f0576b21c7310442db9eb2687b986de

$ docker ps # This command will let you see all running containers so you can verify it's working
CONTAINER ID  IMAGE             COMMAND          CREATED          STATUS         PORTS                     NAMES
0ccb6fa460f7  dashboards:first  "python app.py"  20 seconds ago   Up 18 seconds  127.0.0.1:8000->5000/tcp  vigilant_perlman
```

After your docker container is running, you should be able to open a tab in your browser and navigate to your local host port 8000 to view the running application. 

To stop the container run:
```bash
$ docker stop 0ccb6fa460f7
```

## TODO
1) Move off of the default development server to a production server
2) Deploy dockerized web app to cloud server
3) Optimize performance of dashboard by caching or aggregating data before plotting
