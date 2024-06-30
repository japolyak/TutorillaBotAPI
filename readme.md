# TutorillaBotAPI

This application is part of the [TutotillaBot](https://github.com/users/japolyak/projects/2/views/4) project.
It connects [TutotillaBot](https://github.com/japolyak/TutorillaBot) and [TutorillaBotWebApp](https://github.com/japolyak/TutorillaBotWebApp) with `PostgreSQL` database.

## API

The API is built using FastAPI for creating endpoints, Pydantic for data validation and settings management, and SQLAlchemy for ORM  and database operations.

## Database

The application uses a PostgreSQL database hosted on a Google Cloud virtual machine located in the North America region.
This choice was based on financial considerations. Due to the database's location, requests to the database may take slightly longer than usual.
To mitigate this, some requests are made (and others will be rewritten) as transactions or functions to reduce the number of database requests.

## Deployment

The app runs on Docker containers and uses Google Cloud Platform for reliability and scalability.
It requires the following environment variables for service configuration:

Main variables:
* `ALLOWED_ORIGINS` - list of divided by `&` allowed origins for CORS.
* `IS_DEVELOPMENT` - determines development or production environment - `True` or `False`.

Telegram related variables:

* `BOT_TOKEN` - bot token
* `ADMIN_TG_ID` - bot admin telegram id
* `MY_TG_ID` - developer telegram id for debugging - not required in production

Database related variables:
* `DB_USER` - db user
* `DB_PASSWORD` - db password
* `DB_HOST` - db host
* `DB_NAME` - db name
* `DB_PORT` - db port