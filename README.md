Celeryproject website
=====================

The official Celery Project website 

#### Required Django apps ####
- sorl-thumbnail

### How to run celeryproject in local ###

The project contains a requirements.txt file, so it's enough that you create a virtual env and you install the requirements using pip

```
pip install -r requirements.txt
```

After that make sure to create a dev.py file in the settings folder, you can use as template the dev.py.sample, and just fill in your local database settings.
Once done you can run the Django syncdb command and feel free to create an admin user.

```
python manage.py syncdb
```

Once this is done the website is ready to run, but if you want some content coming from the celeryproject website you can load the sample data from the fixtures by running:

```
python manage.py loaddata sampledata.json
```

Feel free to contribute or propose new features/content for the website.

