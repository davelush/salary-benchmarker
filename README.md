# Salary Benchmarker

## Introduction

This is a small Python script that grabs a set of salary benchmark data from ITJobsWatch. I've provided an example input
file in [jobs.csv](https://github.com/davelush/salary-benchmarker/blob/main/jobs.csv) that is used to decide which job 
roles to scrape and how they map to the role names you have. The only thing that's really used here is the `link` column. 
The rest is passed through to the output spreadsheet unchanged. Selfishly, I just want to be able to include everything I 
use to manage job specs.

## Pre-requisites

```
Python 3.9+
pipenv
```

## How to run

```shell
pipenv update
python main.py
```
