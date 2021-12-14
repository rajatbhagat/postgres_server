# PostgreSQL as a service

## Vision and Goals Of The Project:

PostgreSQL is an object-relational database system that is robust and reliable. The vision of this
project is to build a fault-tolerant PostgreSQL as a service solution.

The key goals of this project include:

* Building various APIs that can create, delete and modify PostgreSQL databases that are stored on
  various containers.
* Developing websites for the users to easily monitor and manage their databases through the APIs we
  built.

## Users/Personas Of The Project:

Database Users

1. As a database user, I want to store my data on a remote server that is fault tolerant, so that it
   is easy to scale up and down, and if one server is down, my data will not be lost.

2. As a database user, I want to be able to conveniently manage my database through a website,
   including: create a new database, requesting access to existing database and deleting a database
   etc.

3. As a database user, I want to be able to monitor my database usage and conveniently have a report
   generated for me about the various metrics of my databases.

## Scope and Features Of The Project:

The project covers the build and deployment of a Web Application with an API implementation using
which the user will be able to create PostgreSQL instances on different VMs and spin-up new
databases as required. The below features can be considered as in scope for the project
implementation:

- Create a Web-Application that the user will be able to interact with and perform various
  operations.
- Creation of various APIs for the purpose of :
- Creation of new databases on the existing PostgreSQL instances. This should also create a backup
  database that shadows the primary database on another PostgreSQL instance.
- Delete existing PostgreSQL database.
- Get information about a PostgreSQL database.
- Change settings of an existing database.
- Generate reporting metrics regarding the database health and database usage.

Stretch Goals:

* Provide Client Authentication over SSL.
* Expand the API service to function across multiple clouds (e.g. a private OpenStack cloud and
  Google Cloud).

## Solution Concept:

The system will consist of a Web Application that will be used by the user and the corresponding API
logic layer will be responsible for creating the database instances as well as getting the data
requested by the user. Initially, the entire project will be done on an OpenStack based Cloud and
then later can be expanded to accommodate other private clouds.

### Technology Used

The technology stack that we used for implementation are as follows:

* Frontend: React.js
* Backend: Flask
* PostgreSQL Database Adapter: Psycopg
* Auto Postgres Fail Over Management Tool: Repmgr, Keepalived
* API Testing: Swagger API

### Design

We envision the final structure to be as given below.

![alt text][figure 1]

[figure 1]: https://github.com/libing-milly/cs6620_postgresql/blob/main/final_diagram.png "Logo Title Text 2"

The above diagram presents the conceptual design we have for PGSQL as a Service (PGSQLaaS) system.
There are mainly 4 componenets:

* the React web application;
* the Backend Server that handles database CRUD operation;
* the Central Lookup Repository that maintains information needed to connect to a Postgres Server;
* the Postgres Servers along with a poller script for updating server information to the Central
  Lookup Server.

The user can either calls the APIs directly or through the web application we developed. When a user
trigger an API call through the web application, the web application will call the backend server
through API.

The Backend Server and Central Lookup Repository are are hosted on one VM. This VM is used only for
the purpose of hosting this server. When the backend server receives a request, it will check the
central lookup repository for information needed to connect to the correct postgres server,
including the ip address, whether the postgres server is primary or sandby, and its availability.
When the backend server found the information needed, it will then connect to the appropriate
postgres server and sends appropriate commmands as requested.

The Postgres Servers are always created in pairs on 2 separate VMs, with one being parimary and the
other being the standby. When a postgres server receives a command from the backend server, the
command will be automatically replicated to its standby server. On every VM that runs a postgres
server, there is also a poller script that will call the Central Lookup API on a schedule to update
the postgres server's inforamtion to the Central Lookup Repository. In the scenario when the primary
postgres server fails, the standby postgres server will automatically become the primary, and the
poller script will update this information to the Central Lookup Repository.

## Acceptance criteria:

* Our web application supports basic functions such as creating, deleting and updating a Postgres
  database, in a fault-tolerent mannner.

## Release Planning:

We will attempt to deliver our project in the following stages:

1. A simple website and the corresponding APIs for the user to create and delete a PostgreSQL
   database on a container.
2. A more comprehensive website with functions including viewing the meta information on current
   databases, updating the parameters of databases. The stretch goals if time permits.

## Developer Guide:

In the following sections we will explain the steps needed to set up each of the 4 main components
of this project in order:

1. the configuration of postgres server (for auto replication and failover)
2. the backend server
3. the central repository and the poller script
4. the web interface

## API Setup

### Python and Virtual-Environment Setup

Follow the below mentioned steps : 

1. Install Python

`sudo yum install python3`

2. Install Virtual Environment

`pip3 install virtualenv`

3. Install git-cli and setup code

`yum install git`

`mkdir app`

`cd app`

``git clone https://github.com/amadgi/postgres_server.git``

4. Create Virtual environment

`virtualenv cloudenv`

`source cloudenv/bin/activate`

`cd postgres_server`

`nohup python application.py &`

5. Update the VMs setup as database instances in the central repository manually.

### Setup of Poller Script On Database VM

