# Weather app exercise.

This small application gets the weather info from
[open weather map](https://openweathermap.org/)
api, and shows the current weather for the specified city an - country.


## run on docker.

1. configure the .env file, see "example.env". Set your appId and ports. Set the host is optional.
2. Run "docker-compose up".
3. The app should run, if you're in a local environment, you can access to the endpoint, for example:

http://localhost:8080/weather?city=bogota&country=co

## How to run locally?

1. Install python, this was tried with python 3.11.
2. Open the console, and Create a virtual environment: "python -m venv {your_folder}"
3. Go to the new environment and run: Scripts/activate
4. Go to the folder of this project and install the modules: "pip install -r r_dev.txt"
5. set the environment variables in the ".env" file. See the "example.env" file.
6. run "python run.py"

### (Optional) running with flask.

this was added to be executed in pythonanywhere, seems that pythonanywhere sopports wsgi based frameworks only and have templates for flask.

Do the previous steps, except the last step. Do the following instead:
1. "pip install flask". Flask is not included in the requirement files.
2. "python run_flask.py"

## endpoints

### GET /weather?city=$City&country

Get the current weather for the specified city and country.

- City: is a string. Example: Valledupar
- Country: is a country code of two characters. Example: co

For example:

GET /weather?city=Bogota&country=co

You should get a result like this:

{
    "location_name": "Bogota, CO",
    "pressure": "1028 hpa",
    "humidity": "100%",
    "geo_coordinates": "[4.6097, -74.0817]",
    "temperature": "11.73 °C, 53.11 °F",
    "wind": "Light air, 1.03 m/s, North",
    "cloudiness": "broken clouds",
    "sunrise": "05:42",
    "sunset": "17:44",
    "requested_time": "2023-10-10 06:06:52"
}

Notes:

* sunrise and sunset are set to the provided timezone from the query in the weather api service.
* requested_time is based on the current server time, in UTC.

