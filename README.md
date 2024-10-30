Project 10 - SoftDeskAPI
-
As part of the OpenClassroom "Python Application Developer" training program, this project is an Restful API for sharing issues and comments about projects developped with Django Rest Framework

Prerequisites :
-
Ensure to have the following installed on your system :

* Python 3.10 or higher
* Pipenv

Installation (windows)
-
In a terminal, clone this repository using :

    git clone https://github.com/Chillihache/Projet10.git

Open the directory :

    cd Projet10

Install dependencies :

    pipenv install

Activate the virtual environment :

    pipenv shell

To set up the data base :

    python manage.py migrate

Create a superuser :

    python manage.py shell
    from authentication.models import User
    user = User.objects.create_superuser(username="your_username", password="your_password", age=your_age)
    user.save()
    exit()

Then, run the server :

    python manage.py runserver

The API is now available at http://localhost:8000/
