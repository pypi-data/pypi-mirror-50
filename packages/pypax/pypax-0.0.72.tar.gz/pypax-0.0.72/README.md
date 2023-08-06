# pypax
CLI tool to organise, version, and automate work on repositories.



![pypax_deps](images/pypax_deps.svg)

#### Configuration and Responsibilities

> PyPax will need to be configured at three different levels. The **project configuration** is unique to the project. The **system configuration** is for the user's instance of PyPax installed in a particular machine. The **server configuration** is shared between multiple users and machines.

| Project      | System          | Server                      |
| ------------ | --------------- | --------------------------- |
| Dependencies | Server Logins   | Version Control Credentials |
| Workflow     | Encryption Keys | 3rd Party Credentials       |
|              |                 | Dependency Graph            |
|              |                 | CICD                        |

## Core Functionality

* **Automatic Directed Updates**: If a change is pushed into production for a module, all of its dependant modules should receive the update process as well.
* **Channel Creation**: Easy to define and edit the channel and relationship of data-flow between modules without needing to deal with the helm charts.
* **Testing and Coverage**: Testing and coverage is built into the system.



TO DO: 

* Create a server and a database to store this information.
* Create a front-end for the server.
* Dockerize and deploy to the cloud.
* Create API to add nodes.
* Create API to trigger node updates.
* Create API to scan for node tests and such.