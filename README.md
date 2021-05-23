# Brevet time calculator clone with additional features and services
## Background
The Randonneurs USA (RUSA) time calculator is a tool used for calculating control times for a brevet. A brevet is a timed, long distance road cycling event. A control point refers to a point where a rider must obtain proof of passage (which shows that a rider completed the entire course without shortcutting and that they finished it within the allotted time limi). Control times are the minimum and maximum times by which the rider must arrive at the location (of the control point).

## Project Overview
The original version of the main web service: https://rusa.org/octime_acp.html. The updated main web service is located in the 'brevetCalculatorWebsite' directory.

* Additional features to the main web service include: 
    * Dynamic open and close time fields (implemented using Ajax)
    * Save distance and open and close times (implemented using MongoDB)
    * Display saved distance and open and close times

* Additional services include:
    * A "producer" (API) service found in the directory titled 'api'. This service handles retrieving data from a database formatting the data (JSON and CSV), and making requested data avaliable. 
    * A "Consumer" service found in the directory titled 'apiDataWebsite' This service makes all the requests detailed in the 'functionality' section and displays them on one web page. Note: The top 'n' open and close times are demoed for n=3, but the api service allows n to be any number.

Docker and Docker Compose were used for testing and deployment of the above services.

## What is in this repository
* docker-compose file (docker-compose.yml) and docker files (Dockerfile) are for containment and interaction between services.

* screenshots (directory) contains screenshots of each of the services described working. 

* 3 main services were implemented for this project:
    1. A main web service: brevet calculator (in the 'brevetCalculatorWebsite' directory). This service handles the logic for calculating the brevet open and close times, sending (form) data to a database (MongoDB), and creation of the brevet calculator web page.

        * In this service's directory:
            * static (directory)
            CSS and JS files necessary for HTML presentation and 'moment' library utilized in HTML pages.

            * templates (directory)
            HTML templates to be completed with 'session' data. For example, calc.html is dynamically updated with open/close times.

            * acp_times.py
            Logic for open and close time calculation based on the algorithm from https://rusa.org/pages/acp-brevet-control-times-calculator .

            * brevet_calc.py
            Framework for running our program (using Flask) which renders apprpriate HTML pages and handles AJAX requests (sent from template/calc.html)

            * config.py
            Configures from app.ini and credentials.ini and conigures Flask application object.

    2. A "producer" (API) service found in the directory titled 'api'. This service handles retrieving data from a database, formatting the data (JSON and CSV), and making requested data avaliable.
        * In this service's directory:
            * api.py
            Exposes/retrieves requested data from database

    3. A "Consumer" service found in the directory titled 'apiDataWebsite'. This service makes all the requests detailed in the 'functionality' section and displays them on one web page. Note: The top 'n' open and close times are demoed for n=3, but the api service allows n to be any number. This is all handled in index.php. 

## System Information
* All services were tested and deployed using Docker Compose on a virtual machine (VirtualBox Version 6.0.24) running Linux Mint 19.3 MATE.

* Installing Docker and Docker Compose on Linux Mint:
https://computingforgeeks.com/install-docker-and-docker-compose-on-linux-mint-19/

## How to use
1. Naviagate to DockerRestAPI
2. $ docker-compose up
3. To use the web service: http://0.0.0.0:5000/
4. To view API data in browser: see api-service port given in terminal and follow the URIs in the API Information section below.
5. To view the consumer service: see api-data-website_1 port number assigned in terminal upon startup.

## API Information

* RESTful service exposing what is stored in MongoDB with the following three basic APIs:
    * "http://<host:port>/listAll" returns all open and close times in the database
    * "http://<host:port>/listOpenOnly" returns open times only
    * "http://<host:port>/listCloseOnly" returns close times only

* Also two different representations for each of the basic APIs: one in csv and one in json. JSON is the default representation for the three basic APIs.
    * "http://<host:port>/listAll/csv" returns all open and close times in CSV format
    * "http://<host:port>/listOpenOnly/csv" returns open times only in CSV format
    * "http://<host:port>/listCloseOnly/csv" returns close times only in CSV format

    * "http://<host:port>/listAll/json" returns all open and close times in JSON format
    * "http://<host:port>/listOpenOnly/json" returns open times only in JSON format
    * "http://<host:port>/listCloseOnly/json" returns close times only in JSON format

* Also, a query parameter to get top "k" open and close times. For examples, see below.

    * "http://<host:port>/listOpenOnly/csv?top=3" returns top 3 open times only (in ascending order) in CSV format
    * "http://<host:port>/listOpenOnly/json?top=5" returns top 5 open times only (in ascending order) in JSON format
    * "http://<host:port>/listCloseOnly/csv?top=6" returns top 5 close times only (in ascending order) in CSV format
    * "http://<host:port>/listCloseOnly/json?top=4" returns top 4 close times only (in ascending order) in JSON format

* Consumer programs (e.g., in jQuery) use the services exposed (see the apiDataWebsite directory).

## Implementation details
* In api.py (api/api.py)
    * The DB only holds one entry at a time containing a key for each of the fields and their values in an array. Because of this, the MongoDB method find_one() is used over find().

    * The DB stores JSON objects by default. Therefore no conversion is necessary for json formatting.

    * CSV formatting is handled using the library 'pandas'. A DataFrame object containing the dictionary entry in the database and is converted to csv using the pandas method to_csv().

    * The value arrays in the database are already sorted, getting the top 'k' times is a matter of getting the last 'n' elements in the open and close time arrays.

* In index.php (apiDataWebsite/index.php)
    * Requests are made to each of the following URI's above and displayed on one web page using php. The top 'k' times is just a demo (k = 3), a URI with a different number will give a different result.

* In docker-compose.yml
    * 4 seperate containers are created for each of the services described above (MongoDB, main web service, API, and consumer service).

## Aknowledgements
This project was for CIS 322, Introduction to Software Engineering at University of Oregon, Spring 2020.

Professor Michal Young created the inital version of the project (https://bitbucket.org/UOCIS322/proj4-brevets/src/master/) and Professor Michal Young and Professor Ram Durairajan created the project specifications (https://bitbucket.org/UOCIS322/proj4-brevets/src/master/, https://bitbucket.org/UOCIS322/proj5-mongo/src/master/, and https://bitbucket.org/UOCIS322/proj6-rest/src/master/ in other words, this project is 3 sequential term projects joined together).