## Django project to set up annotation tool

Usage of annotation tool requires basic knowledge of Django.<br>

To initialize the project create an environment, install `requirements.txt`, execute `python manage.py makemigrations`, and then `python manage.py migrate`. This will create sqlite3 database for your annotator. In case you want to use another database type, edit settings according to django docs.<br>
To use the tool you need to [create superuser](https://docs.djangoproject.com/en/2.0/intro/tutorial02/#creating-an-admin-user) and add possible labels for texts with django admin.<br>
You can upload data for annotation via django shell or using [django migration](https://simpleisbetterthancomplex.com/tutorial/2017/09/26/how-to-create-django-data-migrations.html) (the proper way). In any case consider using [`bulk_create`](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#bulk-create) for speed. To download annotated data use `python manage.py dumpdata mydata.json`.<br>

### Models in django project

##### Article
The main object - article for annotation. It is required to have `html_id`, text or readability html - `ra_summary`, a title - `ra_title`, and be associated with particular annotator from `django.contrib.auth.models.User` - `bee`.

##### Classified
Types for article. This model has one-to-one relations with `Article` and many-to-many relations with `FakeType` (not the best model name). All annotated `Article`s are stored in `Classified`

##### FakeType
Model for types of manipulation or whatever else your annotation is about. Each one has label and long description

##### Feedback
Comments for articles. Each feedback has one-to-one relation with `Article`.