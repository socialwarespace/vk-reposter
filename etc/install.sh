#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
cd ../
PROJECT_ROOT=`pwd`

LOG_DIR="$PROJECT_ROOT/../log"
ENV_DIR="$PROJECT_ROOT/../env"
PROJECT_SRC="$PROJECT_ROOT/src"
PYTHON_VERSION='python3'

sudo apt-get install -y nginx
sudo apt-get install -y supervisor
sudo apt-get install -y git
sudo apt-get install -y python-pip
sudo pip install -y virtualenv

mkdir -p $LOG_DIR
mkdir -p $ENV_DIR

# create env and install requirements
cd $PROJECT_ROOT
virtualenv -p $PYTHON_VERSION $ENV_DIR
source $ENV_DIR/bin/activate
pip install -r requirements.txt

# init project
cd $PROJECT_SRC
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
