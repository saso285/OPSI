# Interface for accessing the portal Open data of Slovenia

*The following project is the product of a bachelor's thesis.*

The interface scraps the data from <a href="https://podatki.gov.si/">OPSI portal</a> and provides it to it's user via simple graphical user interface. The interface also provides basic statistical insight into available data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Project was developed using Python 3.6.3. 

The prerequisites are listed in file "root/requirements.txt" (and bellow) and are installed on with "root/setup.py" script.

### Installing

*Docker integration in development...*

Run "python3 setup.py" from terminal to install prerequistes and "python3 build.py" after for data pull.

## Deployment

Run "python3 server.py" and visit "localhost:3000" to access the data.

## Authors

Sašo Marić

## License

Copyright. The results of the diploma work are the intellectual property of the author and
Faculty of Computer and Information Science, University of Ljubljana. Publication and
use of the results of diploma paper require the written consent of the author,
Faculty of Computer and Information Science and Mentor.
