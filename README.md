
# PEOPLE-ECCO EOAP Example Algorithm

This repository provides an example on how to integrate a Python based algorithm
into the EOAP framework which makes it also compatible with the PEOPLE-ECCO platform.

## Development

### Run locally

Running as CWL Workflow requires `docker` and [`cwltool` (Link)](https://github.com/common-workflow-language/cwltool).

#### Installing cwltool in Python virtual environment

1. `$ python3 -m venv env`
2. `$ source env/bin/activate`
3. `$ pip install cwltool`

#### Build the docker image

Note: all PEOPLE-ECCO algorithm docker images are based on the `ecco-algorithm-base` image. It is defined at
https://github.com/PEOPLE-ECCO/ecco-algorithm-base/blob/main/Dockerfile and is available via ghcr.io.

```sh
docker build -t ghcr.io/people-ecco/ecco-eoap-example:latest .
```

#### Execute the CWL

In order to run, the scripts requires several environment variables:

- `TEST_PATH` = path to folder where results are written
- `OPENEO_AUTH_CLIENT_ID` = openeo client id
- `OPENEO_AUTH_CLIENT_SECRET` = openeo client secret

You can use a `.env` file. See `example.env`, or:

```
TEST_PATH=./target
OPENEO_AUTH_CLIENT_ID=client-id
OPENEO_AUTH_CLIENT_SECRET=client-secret

```

Additionally a JSON File with the parameters for the algorithm run must be provided. An example of the available parameters is provided in `example_parameters.json`, or:

```json
{
  "rangestart": "2023-01-01",
  "rangeend": "2023-01-23",
  "spatial_extent": {
    "west": 118.545313,
    "south": 4.537418,
    "east": 118.568237,
    "north": 4.553655,
    "crs": "EPSG:4326"
  },
  "maxcloudcover": 40
}
```



```sh
export $(cat .env | xargs) && cwl-runner run.cwl --cdse_client_id=${OPENEO_AUTH_CLIENT_ID} --cdse_client_secret=${OPENEO_AUTH_CLIENT_SECRET} --parameters example_parameters.json --run_name ${TEST_PATH}
```
