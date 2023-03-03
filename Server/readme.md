# For installation:

## Dependencies

To install the dependencies for this server, it is neecessary to create a conda environment with the following `yaml` environment file:

`conda env create -f path/to/TFG-DatasetGenerator/Server/environment.yaml`

Download and install the mysql comunity installer to choose the mysql username and password.

https://dev.mysql.com/downloads/mysql/

## Database

To start up the database, it is necessary to have a file in this `Server` folder named `.envDDBB`. The file will have to contain the following structure:

`MYSQL_USERNAME=<your_user>`

`MYSQL_PASSWORD=<your_password>`

## Mail Sender

In order to start the mail server, it is necessary to have a file in this `Server` folder named `.env`. The file will have to contain the following structure:

`MAIL_USERNAME=<your_username>`

`MAIL_PASSWORD=<your_password>`

`MAIL_FROM=<your_email@gmail.com>`