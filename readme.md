### Clone this project
```
git clone https://github.com/<username>/<forked-repo>.git
```
### Change the project name
```
project name: ecom_project
```
### Create your own virtual environment, if no VM exists
```
python3 -m venv venv
source venv/bin/activate
```
### Install following dependencies
```
pip install django pillow
```
### Make your migrations
```
python manage.py makemigrations
python manage.py migrate
```
###  Create a new superuser
```
python manage.py createsuperuser
```
### Start the project
```
python manage.py runserver