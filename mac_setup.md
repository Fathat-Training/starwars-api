# Setting up the development environment on the Mac (OSX)

## Installing Python 3.

This project uses Python 3.10 -

If you already have python 3 on your machine please update to at least 3.10.

You can check your python version via the following command from the terminal.

```bash
python --version
```

To upgrade your python version from an earlier version of python 3:

>Instructions for Installing and Upgrading Python
her [Install/Upgrade Python](https://pyquestions.com/updating-python-on-mac) and here [Install/Upgrade Python](https://docs.python-guide.org/starting/install3/osx/)

## Installing a virtual environment.

If you do not have a virtual Environment Manager Installed you will need install one.

Instructions for installing VirtualEnv can be found

here [VirtualEnv](https://python-guide-cn.readthedocs.io/en/latest/starting/install/osx.html) or here [VirtualEnv](https://virtualenv.pypa.io/en/latest/installation.html)
or numerous other websites by searching 'Installing virtualenv mac OS'


## Create a virtual environment

If you did not create a virtual environment with one of the examples above. Now is the time to do so.
Make sure that you enable python 3.10 for this environment.

## Create a project directory or 

>Create a directory for this project - you can call it something like starwars-api

>Copy this repository into directory either by cloning it to your git account and installing from there or downloading the zip package and unpacking it. 

>If you are using an IDE that has git integration enabled, like Pycharm, you can import the repository directly and set the virtual environment
you wish to use for the project.

>Once you have got the project in place - Inside the virtual environment install all required packages run the requirements.txt using pip or your IDE

```bash
pip install -r requirements.txt
```

## Installing Redis

This project uses [Redis](https://redis.io)

To install Redis on the Mac follow the instructions here [Installing Redis](https://phoenixnap.com/kb/install-redis-on-mac) or by running the 
script mac-redis.sh in the root of this project.

To use redis you will need to set a password. There is a default password of 'redisrocker' assigned in our project configuration file
config/v1/app_config.py

```python
REDIS = {
    "host": "localhost",
    'port': "6379",
    'db': "0",
    'password': "redisrocker"}
```

If you do not wish to use this password, you can change it here. 

## Installing MySQL

The project also uses [MySQL](https://www.mysql.com)

To install MySQL on the Mac follow the instructions here 

```bash 
To install MySQL enter :

brew install mysql
brew services start mysql
```

>then run mysql_secure_installation and follow the instructions

If you want to install a MySql manager to manage databases, you can install 

###MySQL Workbench

install via HomeBrew Cask: 

```base
brew cask install mysqlworkbench
```

If you do not want to because your IDE can manage Databases, then you can start, stop and create databases from setting or via the command line.

When you installed MySQL it generated a password for the root user.

>Type the command '/usr/local/mysql/bin/mysql -u root -p' in the terminal
and type in the generated password.

For all Mysql commands see the link above and read the docs.


That's it for the setup, once all these components are in place and running as they should be you can start learning and building the project
here using 
> [Build the project- markdown instructions](training-docs/intro.md) or running the html files starting with the introduction at training-docs/html-docs/intro.html
