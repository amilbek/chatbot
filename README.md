# StudentDesk

StudentDesk is a virtual assistant designed to support students with common university-related tasks. It simplifies access to important information and services, helping students manage their academic activities efficiently.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Running Jupyter Lab](#running-jupyter-lab)
4. [Downloading additional package](#downloading-additional-package)
5. [Running Chatbot (User Interface)](#running-chatbot)
9. [StudentDesk User Interface](#studentdesk-user-interface)
6. [Testing](#testing)
7. [Chatbot Functionalities](#chatbot-functionalities)
8. [Supported Queries](#supported-queries)
9. [StudentDesk Block Diagram](#studentdesk-block-diagram)
10. [Technologies Used](#technologies-used)
11. [Data](#data)
12. [Models](#models)
13. [Database](#database)
14. [Efficiency Metrics](#efficiency-metrics)
    - [NER Model](#ner-model)
    - [Intent Classifier Model](#intent-classifier)
   
## Project Structure
The project structure is as follows:
```
Chatbot/
├── data/
│   ├── raw/
│   ├── processed/
├── diagrams/
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
- `diagrams`: Contains diagrams and user interface
- `models`: Stores trained models
- `environment.yml`: Creates a conda environment with necessary packages
- `README.md`: Provides project information

## Installation
To install the necessary packages, use the provided conda environment file. First, make sure you have conda installed. If you don't have it installed, you can download it from [here](https://docs.conda.io/en/latest/miniconda.html).

To create a new conda environment from the environment file, use the following command:
```bash
conda env create -f environment.yml
```

To activate the environment, use:
```bash
conda activate student-desk
```
If you're using an IDE like PyCharm or VSCode, you have to select the environment in the IDE settings.

## Running Jupyter Lab
```bash
jupyter lab
```
The cell should then output a link that you can open in your browser to access Jupyter Lab. Check the output in the terminal for the link. It should look something like this:
```
http://localhost:8888/lab?token=aa7e97c2d09bae01632db508730ab48cbc4609fc92c7fc6e
```
The token can vary, so make sure to use the one provided in the output.

## Downloading additional package

To donwload - de_core_news_lg - spaCy language model (if it is already downloaded, there is no need to run this command.)
```bash
python -m spacy download de_core_news_lg
```

## Running Chatbot (User Interface)

Enter following commands in terminal

```bash
conda activate student-desk
```

```bash
cd src
```

```bash
python app.py
```

Following this go to the link
```bash
127.0.0.1:5000
```

## StudentDesk User Interface
![StudentDesk Architecture](https://github.com/amilbek/chatbot/blob/main/diagrams/StudentDesk%20User%20Interface.png)

## Testing
**test_requests.txt** contains possible requests to chatbot.

## Chatbot Functionalities
* Intent classification using **rule-based** and **machine learning** approaches.
* **Named Entity Recognition (NER)** for extracting student details.
* Database integration for retrieving and updating student records.

## Supported Queries
1. Update personal information (first name, last name, address)
2. Register for exams
3. Deregister from exams
4. Query exam status
5. Query exam grades
6. Query student profile

## StudentDesk Block Diagram
![StudentDesk Architecture](https://github.com/amilbek/chatbot/blob/main/diagrams/StudentDesk%20Architecture.png?raw=true)

## Technologies Used
* **spaCy (de_core_news_lg)**: Named Entity Recognition (NER)
* **TensorFlow (Bidirectional LSTM)**: Intent classification
* **sqlite3**: Database management
* **Flask API**: API integration

## Data
The chatbot uses three datasets:
* **tokens.csv**: Training data for NER, containing text and labeled entities.
* **test_tokens.csv**: Testing data for NER.
* **chatbot_dataset.csv**: Training data for intent classification.
* **rule_based_intents.json**: Predefined intents for rule-based responses.

## Models
The models are stored in **[amilbek/univerisy-chatbot](https://huggingface.co/amilbek/univerisy-chatbot/tree/main)**

* **custom_ner_model** - trained NER model to define entities
* **intetn_lstm_model.keras** - trained Intent Classifier Model
* **label_encoder.pkl** - Intent encoder
* **tokenizer.pkl** - Text tokenizer

## Database
To get the completed database, run a cell in **notebooks/database.ipynb**

* **shared_database.db** contains the database of the chatbot (users, courses, exams, exam grades).

## Efficiency Metrics

### NER Model

|  Metric  | Value |
|----------| ------|
| Precision| 98.96%|
| Recall   | 98.45%|
| F1-Score | 98.70%|

### Intent Classifier Model

|  Metric  | Value |
|----------| ------|
| Accuracy| 99.50%|
| Precision| 99.51%|
| Recall   | 99.50%|
| F1-Score | 99.50%|

📝 **Detailed Documentation:** See the **[StudentDesk Report](https://github.com/amilbek/chatbot/blob/main/StudentDesk%20Report.pdf)** for in-depth insights.
