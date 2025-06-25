# Overview

This document serves as my notes as I go through the videos in this module. This will be a bit disorganized, as I will just note down what I need to.

I will be watching each video, and try to code along, so that I can get the practice. I will also be adding any issues I went through ,and how I resolved them. 

After I go through each video, I will be going through the homework, and taking notes as well.

# Relevant Links
 - [Module Folder](https://courses.datatalks.club/mlops-zoomcamp-2025/homework/hw6) on Github
 - [Homework Link](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2025/06-best-practices/homework.md)
 - [Homework Submission](https://courses.datatalks.club/mlops-zoomcamp-2025/homework/hw6)


# Video Notes
## MLOps Zoomcamp 6.1 - Testing Python code with pytest
Video: [Testing Python code with pytest](https://www.youtube.com/watch?v=CJp1eFQP5nk&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK) on Youtube.

 - Copied the initial streaming code from  Module 04 folder in the original github repository. Putting it in the streaming folder in this repo under `06-best-practices`.
 - I'll be following along to add unit tests to the project.
 - Since the streaming project use pipenv, I will use pipenv, instead of using uv for this. Howevever, it seems i have to install pipenv through pipx. 
 - running `pipenv install` is running into an issue. Since I already have an active venv because of uv, pipenv just wants to reuse the same evironment created by uv. I am asking it to create its own by setting ` PIPENV_IGNORE_VIRTUALENVS=1` and then `export PIPENV_IGNORE_VIRTUALENVS`. This seems to have worked.
 - also need to to install pyenv separately.
 - note that i set things up so that each module has separated environments. it was becomeing untenable to use the workspaces feature in uv. 
 - also, I think i need to recreate a model file since downloading it from s3 isn't workable. I'll work on that next.