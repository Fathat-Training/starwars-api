# Setting up the development environment on Ubuntu (Linux)

## Install Multipass

Follow instructions to install Multipass here: https://multipass.run/

## Create a virtual machine

```bash
multipass launch --name ubuntu
multipass shell ubuntu
```

The last command will open the command-line shell of your virtual machine.
In the shell update the packages by issuing the following commands:
```bash
sudo apt update
sudo apt upgrade
```

See the other usage info here: https://multipass.run/

## Install the core toolset

Open shell using `multipass shell ubuntu` and enter the following commands:

```bash
# Git
sudo apt install -y git

# Python
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.10 python3-pip build-essential libssl-dev libffi-dev python-dev python3-venv

# MySQL server
sudo apt install -y mysql-server
# Set the root password here.
sudo mysql_secure_installation
# This should say the service is active.
sudo systemctl status mysql.service
# This will print the MySQL version
sudo mysqladmin -p -u root version
# You should be able to login now (type "quit" to exit):
sudo mysql

# Redis server
sudo apt install -y redis
# This should print "PONG"
redis-cli ping
# Configure Redis
sudo nano /etc/redis/redis.conf
# UNCOMMENT the following line, change "foobared" to "redisrocker" and save file.
# requirepass foobared
# Should be --> requirepass redisrocker
# Restart Redis
sudo systemctl restart redis-server
# This should say the service is active.
sudo systemctl status redis-server
# This should print "OK"
redis-cli AUTH redisrocker
```

## Mount your Github root directory

```bash
$env:MULTIPASS_SERVER_ADDRESS = 'localhost:5001'

multipass set local.privileged-mounts=true

mount C:\Users\$USERNAME\Documents\GitHub\ ubuntu:/mnt/github
```

Go to your ubuntu terminal and see the files there:
```bash
multipass shell ubuntu
ls -al /mnt/github
```

## Testing: Connect to your server via browser

To test, start a web server in your home directory.
Open shell with `multipass shell ubuntu`.

```bash
# This will print the IP address of your virtual machine.
# Copy the IP address of the eth0 interface to clipboard.
# For example "172.18.206.97"
ip addr show label eth0 | grep "inet "
cd /mnt/github
python3 -m http.server 8080
```

Open browser (eg. Chrome, Firefox) on your host machine and enter this address: `http://<IP>:8080`

Replace `<IP>` with the IP address you copied to the clipboard.
You will see the directory listing of your GitHub directory.

## Set up environment for starwars-api

```bash
cd ~
python3 -m venv ./venv
cd ./venv
source bin/activate
cd /mnt/github/starwars-api-backend-skeleton
python3 -m pip install -r requirements.txt
```

Now go to the readme.md file or the readme.html file and follow the instructions
