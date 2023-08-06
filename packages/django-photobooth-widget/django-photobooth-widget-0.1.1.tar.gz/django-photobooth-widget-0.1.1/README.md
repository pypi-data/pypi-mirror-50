Photobooth Widget
=================

Usage
-----
* Add 'django_photobooth_widget' to INSTALLED_APPS.
* Make sure `'APP_DIRS': True`, enabled in TEMPLATES.
* `STATIC_ROOT` needs to be ser to collect stati files with:
   > `$ python collectstatic`

Test Photobooth
---------------
1. Create the virtualenv:  
   > `$ virtualenv -p python3 venv`  
   `$ source venv/bin/activate`
2. Install the requirements:  
   > `$ pip install -r requirements.txt`
3. Update the database:  
   > `$ python manage.py migrate`
4. To be able to use the, it needs to be in a HTTPS connection.
Run the test server as this:  
   > `$ python manage.py runserver_plus 9000 --cert-file cert.crt`

