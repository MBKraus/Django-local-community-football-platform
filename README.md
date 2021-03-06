# Web-based local community football platform built on the Django web framework

A simple responsive online platform built on Django which allows people to get together and organise football matches in their own neighbourhood.

Notable features:

- Allows one to organise and browse football matches in the neighbourhood
- Enables users to create their own user profile along an extended user model
- Users are able to communicate with each other through a messaging platform linked to each match
- Through GeoPy and the Google Maps API match locations are pinpointed for each event
- Built using the Django authentication system (using custom password reset templates)
- Includes mail templates (from MailChimp) for sign up confirmation and password resets

#### Screenshot - Homepage
![alt text](https://raw.githubusercontent.com/Weesper1985/Django-local-community-football-platform/master/gitpics/Home.jpg)

#### Screenshot - Event Detail
![alt text](https://raw.githubusercontent.com/Weesper1985/Django-local-community-football-platform/master/gitpics/Event_detail.jpg)

#### Screenshot - Event List
![alt text](https://raw.githubusercontent.com/Weesper1985/Django-local-community-football-platform/master/gitpics/Event_list.jpg)

## Built With

* [Python 3.5.1](https://www.python.org/downloads/release/python-351/) - The python version used
* [Django 2.0](https://docs.djangoproject.com/en/2.0/releases/2.0/) - The web framework used
* [GeoPy 1.11](https://pypi.python.org/pypi/geopy) - The geocoding web service used
* [Django-Bootstrap3 9.1](https://django-bootstrap3.readthedocs.io/en/latest/) - For Bootstrap3 integration
* [Django-Braces 1.11](https://django-braces.readthedocs.io/en/latest/) - For Mixins
* [Pip 9.01](https://pip.pypa.io/en/stable/installing/) - Recommended tool for installing Python packages

## Install instructions for use on your local server [assuming 0.0.0.0:8000]

- Install the packages above by means of Pip
- In your terminal go into the project's root folder and type in the below to collect all static assets:

```
python manage.py collectstatic
```

- Link to your own SQL database in settings.py (or skip this step if you would like to proceed along Django's standard SQLite database)

- Get a Google Maps API key and insert it in the following templates:

    - events/event_form.html
    - events/event_detail.html
    - event/event_update_form.html
    
- make migrations and migrate
- create a superuser ("python manage.py createsuperuser")
- create a site in the admin panel (and put the corresponding site_id in your settings.py file)
- hit 'python manage.py runserver 0.0.0.0:8000' and enjoy!
