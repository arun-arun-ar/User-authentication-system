This web app has been developed using the popular Django framework for backend and bootstrap, HTML  for the frontend. 

Basic Features of The blog web app prototype.
User Registration – Users can register and create their own new profile
Login - Registered user can login using username and password.
Dashboard - After loging in user are redirected to a dashboard which contains features like change password, edit profile, delete profile etc.
Update Profile  and change password– register user can update theri profile details by clicing on edit profile.
Forgot Password – Users can easily retrieve their password if they forget it by using their email address
(as it is a prototype i havent add a mail server but it send mail to backend for verifying)
django bildin user administration 


To start the project
To get this project up and running locally on your computer follow the following steps.
open the user authentication system then follwo the following steps

Set up a python virtual environment

Run the following commands

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Open a browser and go to http://localhost:8000/ or http://127.0.0.1:8000/




