# Orchestration

This module is about creating a training pipline based on what we did for Module 02. This will need some sort of orchestration library. For the purposes of this homework, we'll be using dagster.


# Setting up Dagster

Source: https://docs.dagster.io/getting-started/quickstart

## Step 1: Install dagster

```
$ uv add dagster
$ uv tree | grep dagster # see dagster versions
```

As of 2205-06-09, we see 
```
└── dagster v1.10.19
    ├── dagster-pipes v1.10.19
    ├── dagster-shared v1.10.19
```

