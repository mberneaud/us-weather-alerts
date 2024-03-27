# U.S. Weather Alerts Pipeline
Repo for the Le Wagon Data Engineering bootcamp final project

# General project guidelines

* We use [Github Flow](https://docs.github.com/en/get-started/using-github/github-flow) for managing code contributions. For this reason, the main branch is protected from pushes. Create feature branches with the following naming convention: name-yyyymmdd-feature when for features you work on and create pull requests.
* Stand up each Tuesday and Thursday at 18:45 CET.

# MVP Features
Screenshot from Slack
![MVP features](meeting_notes/MVP.png)

# Architecture sketch
![architecture sketch](architecture_sketch.png)

# Local env Airflow and DBT conf :

### Prerequisites :

Add the gcp keys to your VM  (In the same location as the one your VM uses for the bootcamp) and name it as us_weather_alerts.json
the path should be like the following
```
.gcp_keys/us_weather_alerts.json
```

Once the project is cloned in your local machine.

```
docker compose up --build
```

# Useful Links
## US National Weather Service API
* [US National Weather Service API page](https://www.weather.gov/documentation/services-web-api#/)
* [National Weather Service API Python package](https://nwsapy.readthedocs.io/en/latest/index.html)
* [US National Weather Service Glossary](https://forecast.weather.gov/glossary.php?letter=u)

## Pandas-GBQ Package
* [Writing Data to BigQuery](https://pandas-gbq.readthedocs.io/en/latest/intro.html#writing-data-to-bigquery)
* [Writing to an existing table](https://pandas-gbq.readthedocs.io/en/latest/writing.html)
* [Authenticating with a service account JSON](https://pandas-gbq.readthedocs.io/en/latest/howto/authentication.html#id3)
