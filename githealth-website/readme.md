# Githealth-website
Githealth-website is a full stack web dashboard for the githealth metrics using next.js for frontend and FastAPI for backend.

## Requirements
* npm
* Python 3

## Frontend
Githealth-website uses next.js for the frontend.\
For localdev:
~~~
npm run start
~~~
For deployment:
Make sure the environemnt variable NODE_ENV is set to be "production".

Build Command:
~~~
githealth/githealth-website/>$ npm install; npm run build
~~~

Start Commamnd:
~~~
githealth/githealth-website/>$ npm run start
~~~

To configure the api routes for development and production environments, in [next.config.js](https://nextjs.org/docs/pages/api-reference/next-config-js)  edit 
~~~
const PRODUCTION_API_DOMAIN = "your backend domain";
~~~

## Backend
Install pip packages
~~~
githealth/githealth-website/api>$ pip install -r requirements.txt
~~~
To Start the backend: 

For local dev:
~~~
githealth/githealth-website/api>$ python3 -m uvicorn index:app --reload
~~~

For production
~~~
githealth/githealth-website/api>$ python3 -m uvicorn index:app --host 0.0.0.0
~~~