# Python template for the Trends of AI semester project
This is a template for the Trends of AI semester project. It includes a basic structure for the project, as well as a conda environment file to install the necessary packages.

## Project structure
The project structure is as follows:
```
Trends-of-AI-Project-Template/
├── data/
│   ├── raw/
│   ├── processed/
├── models/
├── notebooks/
├── src/
├── environment.yml
├── README.md
```
The project structure includes several key folders and files:
- `data`: Stores raw and processed data
- `notebooks`: Contains Jupyter notebooks
- `src`: Holds the source code
- `models`: Stores trained models
- `environment.yml`: Creates a conda environment with necessary packages
- `README.md`: Provides project information

Depending on your project's needs, you may need to add extra folders or files, or remove existing ones (e.g., omit the `src` folder if you're working exclusively with Jupyter notebooks).

## Usage
The conda environment file includes the necessary packages for the project. If you need to install additional packages, please add them to the [environment file](environment.yml)
 and update the environment by reinstalling it (**make sure to update the environment file in the repository as well including version numbers!**).

When working on the project, make sure to use the provided project structure and follow the best practices for project organization. This includes using version control, writing clean and readable code, and documenting your work. Make sure to document your code and provide a README file with information about the project, including how to reproduce the results.

When you're done with the project, make sure to clean up the code, remove unnecessary files, and provide a clean version of the project.

**This is important to ensure that we can reproduce the results of the project and understand the work that has been done!**


## Installation
To install the necessary packages, use the provided conda environment file. First, make sure you have conda installed. If you don't have it installed, you can download it from [here](https://docs.conda.io/en/latest/miniconda.html).

To create a new conda environment from the environment file, use the following command:
```bash
conda env create -f environment.yml
```

To activate the environment, use:
```bash
conda activate trends-of-ai-semester-project
```
If you're using an IDE like PyCharm or VSCode, you have to select the environment in the IDE settings.

## Running Jupyter Lab
Instead of using Jupyter notebooks, we recommend using Jupyter Lab. To run Jupyter Lab, use the following command:
```bash
jupyter lab
```
The cell should then output a link that you can open in your browser to access Jupyter Lab. Check the output in the terminal for the link. It should look something like this:
```
http://localhost:8888/lab?token=aa7e97c2d09bae01632db508730ab48cbc4609fc92c7fc6e
```
The token can vary, so make sure to use the one provided in the output.


&copy; 2024 Lucas Schönhold