# Docker Setup

This guide provides step-by-step instructions to set up and run the Docker container for the project. The container uses Ubuntu 22.04 and includes a Miniconda installation to manage Python environments.

## Prerequisites

- Docker installed on your machine. You can download and install Docker from [here](https://docs.docker.com/get-docker/).
- Git installed on your machine. You can download and install Git from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Make sure you have enough space on your local machine (~30GB+) for development.
- Clone the Repository: `git clone git@github.com:ShvetankPrakash/GenAI4HW.git`. Make sure you've [generated and added an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to your github account.

## Step-by-Step Setup


### 1. Change Directory and Switch to Cohort Branch

Assuming you've cloned the project repository to your local machine, switch the docker directory:
```
cd GenAI4HW/docker
```
Switch to your cohort's development branch. All dev work needs to be done here. For example, for data curation cohort members:
```
git checkout data_curation_dev
```
See branches [here](https://github.com/ShvetankPrakash/GenAI4HW/branches).

### 2. Build the Docker Image

Once navigated to the `docker/` directory, build the Docker image using the following command:

```bash
docker build --platform linux/amd64 -t genai4hw .
```

### 3. Create a Docker Volume for Conda Environments

Create a Docker volume to store the Conda environments:

```bash
docker volume create conda_envs
```

### 4. Run the Docker Container

Run the container with an interactive bash shell, mounting the project directory and the Conda environments volume:

```bash
docker run -it --platform linux/amd64 --rm -v $(pwd)/../:/GenAI4HW -v conda_envs:/opt/conda/envs -p 8888:8888 genai4hw
```

This command mounts the project directory into the container, allowing you to access your files, and mounts the Conda environments volume to `/opt/conda/envs`.

### 5. Create Conda Environment

Inside the container, navigate to your respective cohort directory and create a Conda environment using an `environment.yml` file. For example, for the dataset curation cohort:

```bash
cd GenAI4HW/src/data/text/quarch/01_curation  # Replace 'data/text/quarch/01_curation' with path to your cohort directory
conda env create -f environment.yml
conda activate data_curation  # Replace 'data_curation' with your cohort's env name declared in environment.yml
```

### 6. Update Conda Environment (Optional)

At some point during development, you will most likely need to add more packages to you environment. To update your Conda environment with new packages, modify the `environment.yml` file and then run:

```bash
conda env update -f environment.yml
```

### 7. Commit and Push Changes

Whenever you are done with any development work, exit the container and commit and push your changes from your local machine to your cohort's dev branch:

```bash
# Exit the container
exit

# Commit and push changes from your local machine
git add [FILES CHANGED HERE]
git commit -m "YOUR DESCRIPTIVE COMMIT MESSAGE HERE"
git push origin [YOUR COHORT'S DEV BRANCH HERE]
```

### 8. Running Jupyter Notebook (Optional)

If you need to run a Jupyter Notebook inside the container for interactive development, start the Jupyter Notebook server inside the container like this:

```bash
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

Access the notebook from your browser using the URL provided in the terminal output.

## Additional Notes

- Each team should maintain their own `environment.yml` file within their respective directories (e.g., `dataset_curation/environment.yml`).
- Ensure the `environment.yml` files are kept up-to-date and pushed to the Git repository to allow others to replicate the environment easily.

This setup ensures a consistent development environment for all team members, minimizing issues related to dependencies and package versions.
