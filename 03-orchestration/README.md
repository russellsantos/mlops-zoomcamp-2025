# Orchestration

This module is about creating a training pipline based on what we did for Module 02. This will need some sort of orchestration library. For the purposes of this homework, we'll be using dagster.


# Setting up Dagster

Source: https://docs.dagster.io/getting-started/quickstart

## Step 1: Install dagster
We will want to use dagster, and the dagster web ui
```
$ uv add dagster dagster-webserver
$ uv tree | grep dagster # see dagster versions
```

As of 2205-06-09, we see 
```
├── dagster v1.10.19
│   ├── dagster-pipes v1.10.19
│   ├── dagster-shared v1.10.19
└── dagster-webserver v1.10.19
    ├── dagster v1.10.19 (*)
    ├── dagster-graphql v1.10.19
    │   ├── dagster v1.10.19 (*)
```
We'll also want to use the following packages
```
$ uv add pandas fastparquet
```
## Step 2: Setup Initial data load
Source: https://dagster.io/blog/thinking-in-assets

Dagster files will be n the `dagster-pipeline` folder. We've created 2 files there:
 - `assets.py` - will contain asset data
 - `__init__.py` - will be empty for now.

In addition, we'll be creating a folder for storing data named `data`. We''ll store downloaded data in `data/raw`
You'll need to run the following steps to create these folders (assuming you're in 03-orchestration directory)
```
$ mkdir -p data/raw 
$ touch data/raw/.gitkeep
$ touch data/.gitkeep 
```
This will create the `data` and the `raw` directory, and make usre that these are kept by git even if they are empty

## Step 3: Preprocessing

Before running the code
 - Created the `raw_data` assets
