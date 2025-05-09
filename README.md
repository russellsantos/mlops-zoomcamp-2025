# MLOps Zoomcamp 2025 
My repository containing homework answers for MLOps Zoomcamp 2025 (https://github.com/DataTalksClub/mlops-zoomcamp)


# Environment Setup

I am setting up my enironment slightly differently because of my setup. Here's how I'm setting things up
  1. Running on Ubuntu 22.04 LTS on WSL2 inside Windows 11 - this is just how I'm setup on Windows at the moment. Might upgrade Ubuntu at some point
  2. Using miniconda instead of Anaconda - Anaconda feels bloated to me. Following instructions here: https://www.atlantic.net/dedicated-server-hosting/how-to-install-miniconda-on-ubuntu-22-04/
  3. Docker usage is through Docker Desktop and WSL2 Integration: https://docs.docker.com/desktop/features/wsl/
  4. For python package management, I chose to use `uv` instead of fully using conda. (https://medium.com/codefile/. uv-or-conda-for-virtual-environments-7372a258c7d5). I will still be using conda for making sure system dependencies are met, but for python dependencies, I will  be using uv.

# VS Code Setup
I am also using VSCode as my editor. Using these plugins specifically for this project:
  1. Jupyter