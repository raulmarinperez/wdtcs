# World Domination Through Container Sensoring
WDTCS is a simple demo to show MongoDB's geospatial capabilities. In order to make easier to understand the contents in the MongoDB database and queries issued against it, we (Rubén Terceño and I) have worked in this 'faked' initiative to conquer the World through ship containers.

The following are the three main components:

- **MongoDB backend -** the data folder contains a dump of the database. The database's name is WDTCS and has five collections (only three of them are used at the time of writing): containers, countries, oceans, ports and ships. The containers and ships collections have one 2dsphere index each one.
- **Web server/REST API -** to facilitate its deployment and usage, the web server and a light REST API layer have been developed using CherryPy(http://www.cherrypy.org/).
- **Front-end -** a very simple front-end (hey! we're engineers, don't expect a super-duper interface) displaying a small map, a couple of panels and a textbox + a combobox for filtering. It uses jQuery, Bootstrap and the Google Maps API.

To make it work you just have to clone the repo, satisfy the dependencies (Python + CherryPy, front-end dependencies are included) and start up the server by issuing the following command line:

```shell
$ python wrdt.py
[05/Jun/2016:20:13:11] ENGINE Listening for SIGHUP.
[05/Jun/2016:20:13:11] ENGINE Listening for SIGTERM.
[05/Jun/2016:20:13:11] ENGINE Listening for SIGUSR1.
[05/Jun/2016:20:13:11] ENGINE Bus STARTING
[05/Jun/2016:20:13:11]  vpath: img/dummy.html
[05/Jun/2016:20:13:11]  vpath: css/dummy.html
[05/Jun/2016:20:13:11]  vpath: js/dummy.html
[05/Jun/2016:20:13:11]  vpath: dummy.html
[05/Jun/2016:20:13:11] ENGINE Started monitor thread '_TimeoutMonitor'.
[05/Jun/2016:20:13:11] ENGINE Started monitor thread 'Autoreloader'.
[05/Jun/2016:20:13:12] ENGINE Serving on 0.0.0.0:8080
[05/Jun/2016:20:13:12] ENGINE Bus STARTED
```

Open a web browser and point it out to the URL where the web server is accepting requests (i.e. `http://localhost:8080`).

The following actions are currently implemented:

- **Zoom in and out the map -** zoom out to cover more area and display ships available.
- **Get ship's info -** click markers to retrieve information from ships.
- **Get ship's cargo -** click ship's name from the left panel to get ship's cargo. This info will be displayed in the right panel.
- **Filter ships by content/cargo -** provide the cargo type you want to filter by. More than one cargo type can be specified by separating them by commas (it will perform an OR query). If, for some reason ;), you want to know which ships are carrying out Gold and Uranium, just type `Gold,Uranium` in the contents text box.
- **Filter ships by sea -** choose the sea that will filter the ships within the map. At the moment only North Atlantic and Caribbean sea display ships.
- **Filter ships by sea and content/cargo -** just use the two previous filtering options at a time.

The following people have been involved in this short demo:

- **[Norberto Leite (Curriculum Engineer)](https://www.linkedin.com/in/norbertoleite) -** A guest star that is part of the story when we introduce the demo.
- **[Rubén Terceño (Senior Solutions Architect)](https://www.linkedin.com/in/rubenterceno) -** The brain behind this project. He designed the idea and the script, and built this original database. If you guess where the data is coming from, contact him... he will be very happy.
- **[Raúl Marín (Senior Consulting Engineer)](https://www.linkedin.com/in/raulmarinperez) -** Application designer and developer. 

Please, use this software at your own risk. We don't assume any responsability if you finally decide to 'disturb' any of the sailors that are carrying out the containers. Be respectful :)
