# New Python repository


Template for Python-based repositories


![Packages](https://img.shields.io/badge/package%20manager-uv-blue) ![Style](https://img.shields.io/badge/style-google-black) ![Linter](https://img.shields.io/badge/linter-ruff-black) ![Type check](https://img.shields.io/badge/type%20checker-pytype-black)

## CI status

![coverage](assets/coverage.svg)
[![Lint](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/lint.yaml/badge.svg)](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/lint.yaml) [![Test](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/test.yaml/badge.svg)](https://github.com/ClementSicard/air-monitoring-etl/actions/workflows/test.yaml) 


## Setup up a cronjob


```bash
crontab -e

# Run the job every 15 minutes
*/15 * * * * PATH="/usr/bin:$PATH" cd ~/src/github.com/ClementSicard/air-monitoring-etl && make job
```
