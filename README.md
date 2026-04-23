
# PEOPLE-ECCO EOAP Example Algorithm

This repository stores a beta version of the flow to map Subaquatic vegetation and coral presence from openeo.

## Development

### Run locally

Running as CWL Workflow requires `docker` and [`cwltool` (Link)](https://github.com/common-workflow-language/cwltool).

#### Installing cwltool in Python virtual environment

1. `$ python3 -m venv env`
2. `$ source env/bin/activate`
3. `$ pip install cwltool`

#### Build the docker image

All PEOPLE-ECCO algorithm docker images are based on the `ecco-api-base` image. It is defined at
https://github.com/PEOPLE-ECCO/ecco-api/blob/main/eo/algorithms/base.Dockerfile
which must be built beforehand.

```sh
docker build -t ecco-eoap-example:latest .
```

#### Execute the CWL

In order to run, the scripts requires several environment variables:

- `TEST_PATH` = path to folder where results are written
- `OPENEO_AUTH_CLIENT_ID` = openeo client id
- `OPENEO_AUTH_CLIENT_SECRET` = openeo client secret

You can use a `.env` file. See `example.env`.

Additionally a JSON File with the parameters for the algorithm run must be provided. An example of the available parameters is provided in `example_parameters.json`.



```sh
export $(cat .env | xargs) && cwl-runner run.cwl --cdse_client_id=${OPENEO_AUTH_CLIENT_ID} --cdse_client_secret=${OPENEO_AUTH_CLIENT_SECRET} --parameters example_parameters.json --run_name ${TEST_PATH}
```
