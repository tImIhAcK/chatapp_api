# CHATAPP API

### Development stage

To run the ChatAPP Backend project in the development stage, you can use the following commands:

- Build and run the containers:
  `docker-compose up --build -d`

- view the logs
  `docker-compose logs`

- Perform migrations and create superuser
  ```
    docker-compose exec web python manage.py makemigrations --no-input
    docker-compose exec web python manage.py migrate --no-input
    docker-compose exec web python manage.py createsuperuser
  ```

### Production stage

To run the ChatAPP Backend project in the production stage, you can use the following commands:

- BUild and run containers:
  `docker-compose -f docker-compose.prod.yml up --build -d`

- View the logs
  `docker-compose -f docker-compose.prod.yml logs`

- Perform migrations, create superuser and collectstatic

```
   docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations --no-input
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```
