"# DTEAM-django-test-task" 

To load the sample data into your Django application, you can use the following command:

```shell
poetry run python manage.py loaddata sample_data.json
```

To run tests, you can use the following command:

```shell
poetry run python manage.py test
```

To load fixture into app running in docker container, you can use the following command:

```shell
docker-compose exec app python manage.py loaddata sample_data.json
```