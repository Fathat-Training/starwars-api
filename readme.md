# FatHat.org starwars-api-backend-skeleton Learning Project


---

#### Version 1.0
#### copyright (c) 2022 - Fathat.org
#### Released under the MIT sublicense

---

This codebase is free to use under the above mentioned MIT license. We encourage anyone who wishes to use it for self learning or teaching or any other usage, to do so without hindrance. 
Please leave the title, copyright and license information intact. 

>Notes for those starting to learn about Software Development. Sometimes it feels impossible, sometimes it feels that there is too much to learn. Don't let these feelings stop
you. You will have many breakthrough moments that will encourage you and provide a sense of achievement. Continue learning, it's what life is all about.

>Notes for all those existing Python gurus. If you have any constructive comments and recommendations we would love to hear about them. Feel free to contact us at info@fathat.org

---

The aim of this project is to teach the fundamentals of building a Python API with openApi. The API itself 
is a pipeline API that uses the Star Wars Data at https://swapi.py4e.com/api/ and pass that through this API to 
clients. The openAPI enables the use of a Swagger definition and User interface. The definition acting as the definitive 
APi specification. The minimal use of the Python framework Flask in conjunction with Connexion https://connexion.readthedocs.io/en/latest/
are used to provide the bridge to our python API endpoints.

### Before you start
Before you start the build process the fundamentals must be put in place. The project uses two databases, 'Redis' and 'MySQL'. The project should
ideally be run in a virtual environment and requires python 3.10.

The databases need to be setup prior to the build process and kept running. We have included instructions for creating the database code and any tables
in the build code at the appropriate place. Other setup details for both Mac OS and Ubuntu are provided in the root directory of the project
along with some accompanying bash scripts for the setup of 'Redis'. Please read the files properly before running any of the commands.
If you have an existing virtual environment manager and the databases already setup on your system these can be ignored.

>[Mac OS - Setup](mac_setup.md)

>[Installing Redis on Mac OS](mac-redis.sh)

>[Ubuntu - Setup](ubuntu_setup.md)
