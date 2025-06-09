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
$ uv add pandas fastparquet scikit-learn 
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

Then to run the asset pipeline
`$ dagster dev -f dagster-pipeline/assets.py ` 

Go to the UI and materialize the `raw_data` asset.
Alternatively, run the following command:

`$ dagster asset materialize -f dagster-pipeline/assets.py --select raw_data`

## Step 3: Preprocessing

Before running the code, create the necessary directories.

```
$ mkdir -p data/processed 
$ touch data/processed/.gitkeep
```

Then Go to the UI and materialize `preprocesed_data`, or run:
`$ dagster asset materialize -f dagster-pipeliune/assets.py --select preprocessed_data`

## Step 4: Train model
Source: https://docs.dagster.io/guides/build/ml-pipelines/ml-pipeline

Run in UI or run:
`$ dagster asset materialize -f dagster-pipeline/assets.py --select dict_vectorizer,X_train,Y_train,trained_model`

## Step 5: Register model in MLFLow