# CV Management System

A Django-based web application for managing CVs with skills, projects, and contacts. The system allows users to create, edit, and share CVs in both web and PDF formats.

## Features
- CV management (CRUD operations)
- PDF generation
- Email sharing
- REST API
- Request auditing
- OpenAPI documentation

## Local Setup

### Prerequisites
* Python 3.11+
* PostgreSQL
* Poetry
* pyenv (recommended for Python version management)

### Installation Steps

1. Clone the repository:
```shell
git clone https://github.com/sberdianskyi/DTEAM-django-test-task.git
cd DTEAM-django-test-task
```

2. Install and set Python version:
```shell
pyenv install 3.12.10
pyenv local 3.12.10
```

2. Install dependencies using Poetry:
```shell
poetry install
```

3. Create .env file in the root directory with:
* DEBUG=True
* DJANGO_SECRET_KEY=your-secret-key
* POSTGRES_DB=your-db-name
* POSTGRES_USER=your-db-user
* POSTGRES_PASSWORD=your-db-password
* POSTGRES_HOST=localhost
* POSTGRES_PORT=5432
* EMAIL_HOST=smtp.gmail.com
* EMAIL_PORT=587
* EMAIL_USE_TLS=True
* EMAIL_HOST_USER=your-email@gmail.com
* EMAIL_HOST_PASSWORD=your-app-password
* DEFAULT_FROM_EMAIL=your-email@gmail.com

4. Apply migrations and load sample data:
```shell
poetry run python manage.py migrate
poetry run python manage.py loaddata sample_data.json
```

5. Run the development server:
```shell
poetry run python manage.py runserver
```
6. Access the application at `http://localhost:8000`.

### Testing
The project uses Django's testing framework. To run tests:
1. Run all tests:
```shell
poetry run python manage.py test
```

2. Run tests with coverage:
```shell
poetry run coverage run manage.py test
poetry run coverage report
```

3. Run specific test file:
```shell
poetry run python manage.py test path.to.your.test_file
```

## Docker Setup

1. Build and start containers:
```shell
docker-compose up -d --build
```

2. Load sample data into the database:
```shell
docker-compose exec app python manage.py loaddata sample_data.json
```
3. Access the application at `http://localhost:8000`.

To run tests, you can use the following command:

```shell
poetry run python manage.py test
```

## Endpoints

### CV Management API

* GET /api/cv/ - List all CVs
* POST /api/cv/ - Create new CV
* GET /api/cv/{id}/ - Retrieve CV
* PUT /api/cv/{id}/ - Update CV
* DELETE /api/cv/{id}/ - Delete CV

### Web Interface

* GET /cv/ - List CVs
* GET /cv/{id}/ - View CV
* GET /cv/create/ - Create CV form
* GET /cv/{id}/edit/ - Edit CV form
* POST /cv/{id}/send_pdf/ - Generate and send CV as PDF

## Documentation

* GET /api/schema/ - OpenAPI schema
* GET /api/schema/swagger-ui/ - Swagger UI
* GET /api/schema/redoc/ - ReDoc UI

## Live Demo

The application is deployed at:
https://dteam-django-test-task.onrender.com/