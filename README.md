Django + stripe

prerequisites:
Docker
Python

To run the app:
1. Clone this repo: git clone https://github.com/temirlanzzz/stripeapi.git
2. Build docker image: docker build -t stripeapi .
3. Start container from image: docker run --env-file=.env -p 8000:8000 stripeapi
4. Access app in web browser in:
 - http://localhost:8000/api/item/1 for item
 - http://localhost:8000/api/buy/1 - buy item
 - http://localhost:8000/admin/ - for admin panel



