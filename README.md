# Project 6: Brevet time calculator service

Simple listing service from project 5 stored in MongoDB database.

# Contact info/Class
Michael O'Connell
moconnel@uoregon.edu
CIS 322 at the University of Oregon, Spring 2020
5/30/2020

## What is in this repository

docker-compose file and docker files for containment and interaction between services.

3 main services were implemented for this project:
1. A main web service: brevet calculator
This service handles the logic for calculating the brevet open and close times, sending (form) data to a database (MongoDB), and creation of the brevet calculator web page. For more information see project 5.

2. A "producer" (API) service found in the directory titled 'api'
This service handles retrieving data from a database, formatting the data (JSON and CSV), and making requested data avaliable.

3. A "Consumer" service found in the directory titled 'apiDataWebsite'
This service makes all the requests detailed in the 'functionality' section and displays them on one web page. Note: The top 'n' open and close times are demoed for n=3, but the api service allows n to be any number.

## Functionality added

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
(1) In api.py (api/api.py)
The DB only holds one entry at a time containing a key for each of the fields and their values in an array. Because of this, the MongoDB method find_one() is used over find().

The DB stores JSON objects by default. Therefore no conversion is necessary for json formatting.

CSV formatting is handled using the library 'pandas'. A DataFrame object containing the dictionary entry in the database and is converted to csv using the pandas method to_csv().

The value arrays in the database are already sorted, getting the top 'k' times is a matter of getting the last 'n' elements in the open and close time arrays.

(2) In index.php (apiDataWebsite/index.php)
Requests are made to each of the following URI's above and displayed on one web page using php. The top 'k' times is just a demo (k = 3), a URI with a different number will give a different result.

(3) In docker-compose.yml
4 containers are created for each of the services described above.

Issues installing solved:
https://computingforgeeks.com/install-docker-and-docker-compose-on-linux-mint-19/