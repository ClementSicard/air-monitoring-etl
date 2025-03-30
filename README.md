# Air monitoring pipeline for Ecco2 sensors

Quick pipeline to fetch air quality data from local air quality monitoring sensors by Ecco2 and store it in a PostgreSQL database.
The pipeline is designed to be run every 15 minutes using a cronjob.


![Packages](https://img.shields.io/badge/package%20manager-uv-blue) ![Style](https://img.shields.io/badge/style-google-black) ![Linter](https://img.shields.io/badge/linter-ruff-black) ![Type check](https://img.shields.io/badge/type%20checker-pytype-black)

## CI status

![coverage](assets/coverage.svg)
[![Lint](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/lint.yaml/badge.svg)](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/lint.yaml) [![Test](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/test.yaml/badge.svg)](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/test.yaml) 


## Set up the pipeline

[`uv`](https://docs.astral.sh/uv/getting-started/installation/) and [`docker`](https://docs.docker.com/engine/install/) need to be installed in order to run the pipeline.

Ecco2 URL is of the form `https://live.ecco2.ch/data?devId=<devId>&token=<token>` - you can get the `devId` and `token` from the QR code on the device.

You then need to setup the `.env` file with the following variables:

```bash
PG_PORT=5432
PG_HOST=localhost
PG_USER=postgres
PG_DATABASE=air_monitoring

ECCO2_TOKEN='<your token>'
ECCO2_DEV_ID='<your dev id>'
```

To start the docker compose stack, run:

```bash
make run
```

To manually launch the fetching job, run:

```bash
make job
```


## Setup up a cronjob


```bash
crontab -e

# Run the job every 15 minutes
*/15 * * * * PATH="/usr/bin:$PATH" cd <path to this repo> && make job
```

> [!NOTE]
> - `PATH="/usr/bin:$PATH"` adds `make` to the path, so that it can be found by cron


This has been tested on a Debian system (Raspberry Pi) with Postgres 16
