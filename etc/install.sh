#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
cd ../
PROJECT_ROOT=`pwd`

LOG_DIR="$PROJECT_ROOT/../log"
ENV_DIR="$PROJECT_ROOT/../env"
PROJECT_SRC="$PROJECT_ROOT/src"
PYTHON_VERSION='python3'

echo "PREPARE PROJECT DIRECTORY"
rm -rf $LOG_DIR
rm -rf $ENV_DIR
mkdir -p $LOG_DIR
mkdir -p $ENV_DIR

echo "CREATE ENVIRONMENT"
cd $PROJECT_ROOT
virtualenv -p $PYTHON_VERSION $ENV_DIR
source $ENV_DIR/bin/activate

echo "INSTALL REQUIREMENTS"
pip install -r requirements.txt

echo "INITIAL PROJECT"
cd $PROJECT_SRC
rm db.sqlite3
python manage.py migrate
echo "yes" | python manage.py collectstatic

echo "CREATE ADMIN USER"
python manage.py createsuperuser

echo "INSTALLATION SUCCESSFULLY COMPLETED"
