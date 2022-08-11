# This is a flask api which implements an in-memory empty key-value store

You can perform the following operations

/get/<key> → Returns value of the key
/set → Post call which sets the key/value pair
/search → Search for keys using the following filters
    Assume have keys: abc-1, abc-2, xyz-1, xyz-2
    /search?prefix=abc would return abc-1 and abc-2
    /search?suffix=-1 would return abc-1 and xyz-1

## To run it locally use the following commands
```
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python cache_app.py
```

## To run it in a docker container locally
1. Build the docker image first using the command
```
docker build -t cache-app .
```

2. Run the docker file
```
docker run -p 8090:8090 cache-app
```

## To check for tests run the following command
```
pytest -v
```

## To check for code coverage run the following commands
```
coverage run -m pytest
coverage report
```

## Current hosting
This API is currently hosted on a GCP VM deployed using the terraform script provided in 'terraform/main.tf'. However, the script will not run unless you provide your service account details.

To check the deployment of the API, please visit http://35.232.181.87:8090
You can use the description provided above to interact with the API