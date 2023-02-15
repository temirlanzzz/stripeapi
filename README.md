Django + stripe

prerequisites:
Docker
Python
environmental variables in .env file

To run the app:
1. Clone this repo: git clone https://github.com/temirlanzzz/stripeapi.git
2. Build docker image: docker build -t stripeapi .
3. Start container from image: docker run --env-file=.env -p 8000:8000 stripeapi
4. Apply migrations: docker exec -it <container_id> python manage.py migrate (replace container_id with new container id, you can get it from docker ps)
5. Access app in web browser in:
 - http://localhost:8000/api/item/1 for item
 - http://localhost:8000/api/buy/1 - buy item
 - http://localhost:8000/admin/ - for admin panel 
 - To access admin panel create a super user: python manage.py createsuperuser



