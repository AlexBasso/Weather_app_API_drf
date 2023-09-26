# Django Weather App

Django Weather App is an API that provides weather forcast for up 7 days based on specified city/zip code. Has 3 main API:
   - current weather based on IP address.
   - current weather based on provided City name or Zip code.
   - weather forcast from "Meteomatics API" for the next 7 days, based on provided City name or Zip code.

## Installation

1. Download project.
2. Install and configure PostreSQL and Docker on your OS.
3. Configure .env based on .env.template:
    - example:
        - DB_NAME=postgres
        - DB_USER=postgres
        - DB_PASSWORD=1234
        - DB_HOST=db
        - DB_PORT=5432
        - SECRET_KEY='django-insecure-50shyx*p%t#+3fo@4dt^zf#t=k*uvhn)%sbl@tk%rh*oaa^klk'
        - DEBUG=1
        - DJANGO_ALLOWED_HOSTS=''
4. In case of running:
    - on local host, activate venv and use the package manager [pip](https://pip.pypa.io/en/stable/) to install
      requirements.txt ```"pip install -r requirements.txt" ``` as in the usual django projct configure and
      run ```"python manage.py migrate"```.
    - via docker container commands:

        - ```"docker-compose build" ```
        - ```"docker-compose up" ```
        - use a separate console while container is running: ```"docker-compose exec web python manage.py migrate" ```

You are all set to go!

## Usage, how it looks and what can be expected:

1. You need to register, use: "http://localhost:8000/api/register/", via POST send "username" and "password". You will
   receive your token, that will allow to use Weather API from "Meteomatics API".

![Test image](screenshots/img_1.jpg)

2. In case you already registered, but forgot your token you can just log in and receive your token,
   use: "http://localhost:8000/api/login/", via POST send "username" and "password". You will receive your token,
   that will allow to use Weather API from "Meteomatics API".

![Test image](screenshots/img_2.jpg)

3. Make sure to send your token that you got during registration or log in, then
   use: "http://localhost:8000/api/weather/current/", via GET. You will receive current weather based on your IP
   address.

![Test image](screenshots/img_3.jpg)

4. Make sure to send your token that you got during registration or log in, then
   use: "http://localhost:8000/api/weather/search/", via POST. You will receive current weather based on City name or
   Zip code you have provided. You can also use "query string" with GET method to receive same response.

![Test image](screenshots/img_4.jpg)

5. Make sure to send your token that you got during registration or log in, then
   use: "http://localhost:8000/api/weather/forcast/", via POST. You will receive weather forcast for 7 days based on
   City name or Zip code you have provided. You can also use "query string" with GET method to receive same response, if
   no "query string" is used with GET method, you will receive weather forcast for 7 days for location based on your IP
   address.

![Test image](screenshots/img_5.jpg)

6. You can find more detailed documentaiton via: "http://localhost:8000/swagger/"

![Test image](screenshots/img_6.jpg)

## Contributing

Pull requests are welcome, have fun.

## License

[MIT](LICENSE.txt)