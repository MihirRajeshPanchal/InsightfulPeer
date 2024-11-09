# InsightfulPeer-CoT: Not All Peer Reviews Are Significant

This repository contains code, datasets, visualizations, and analysis for the research project, *InsightfulPeer-CoT: Not All Peer Reviews Are Significant*. The study investigates the use of large language models (LLMs) to evaluate peer review quality using Chain of Thought (CoT) reasoning. We categorize reviews as "good" (exhaustive) or "bad" (trivial) based on their depth in covering sections and aspects of the reviewed paper, aiming to automate the evaluation of peer review quality.

## Folder Structure

```plaintext
├── .gitattributes
├── README.md
├── data
│   ├── Cot-dataset.csv
│   ├── qualitative-analysis-aspect.csv
│   └── qualitative-analysis-section.csv
├── notebooks
│   ├── Cot-GPT.ipynb
│   ├── Cot-Gemma.ipynb
│   ├── Cot-Llama.ipynb
│   ├── Cot-Mistral.ipynb
│   └── results-analysis.ipynb
├── plots
│   ├── COT_DatasetOverview.png
│   ├── COT_Pipeline.png
│   └── Process Flow.png
└── streamlit
    ├── .env.example
    ├── .gitignore
    ├── app.py
    ├── g1.py
    └── requirements.txt
```

## Overview

### Project Objective
The goal of this project is to automate peer review evaluation by training LLMs on a dataset of annotated peer reviews. We employ CoT reasoning models like GPT-4, Llama-3.1-70b-versatile, Gemma2-9b-it, and Mixtral-8x7b-32768 to classify reviews as either "Exhaustive" or "Trivial," based on section and aspect coverage. This automated process allows for more efficient, transparent, and objective assessment of peer review quality.

### Dataset

The dataset includes manually annotated peer reviews:
- **Section Coverage**: Indicates specific sections covered in the review, such as Abstract, Introduction, Methodology, Results, and Conclusion.
- **Aspect Coverage**: Specifies aspects addressed in the review, such as clarity, originality, empirical soundness, and comparisons to related works.

The labels are as follows:
- **Exhaustive**: The review provides comprehensive feedback across multiple sections and aspects of the paper, offering detailed insight into key areas such as methodology, results, experiments, and more. A review should be classified as ’Exhaustive’ if it covers a wide range of sections and aspects (e.g., Abstract, Introduction, Methodology, etc.) with depth, leaving no significant sections or questions unaddressed
- **Trivial**: The review lacks depth and does not sufficiently cover critical sections or aspects. It might focus only on one or two areas (e.g., comments on Abstract or Introduction) and fails to address significant sections or aspects in detail. A ’Trivial’ review might provide shallow or vague comments that do not contribute much to improving the paper.”

## Notebooks

The `notebooks` directory contains Jupyter notebooks for model training and analysis:

- [**Cot-GPT.ipynb**](notebooks/Cot-GPT.ipynb): Experimentation with GPT-4.
- [**Cot-Gemma.ipynb**](notebooks/Cot-Gemma.ipynb): Experimentation with Gemma2-9b-it.
- [**Cot-Llama.ipynb**](notebooks/Cot-Llama.ipynb): Experimentation with Llama-3.1-70b-versatile.
- [**Cot-Mistral.ipynb**](notebooks/Cot-Mistral.ipynb): Experimentation with Mixtral-8x7b-32768.
- [**results-analysis.ipynb**](notebooks/results-analysis.ipynb): Analysis of model performance and alignment with human-labeled review quality.


Visualizations and data tables from the paper are provided to facilitate a better understanding of the results and methodology. Click the links to view each visualization or table.

- [COT Dataset Overview](plots/COT_DatasetOverview.png): Overview of the dataset with section and aspect coverage statistics.
- [COT Pipeline Diagram](plots/COT_Pipeline.png): Workflow for model training and evaluation.
- [Process Flow Diagram](plots/Process%20Flow.png): Chain of Thought (CoT) reasoning approach.

## Streamlit App

The `streamlit` directory contains code to deploy a web app for interactive analysis and model demonstration:
- **app.py**: Main script for launching the Streamlit app.
- **g1.py**: Helper functions and components for the app.
- **requirements.txt**: List of required packages.
- **.env.example**: Example configuration file for environment variables.

### Launching the Streamlit App

Run the following command to start the Streamlit app:
```bash
streamlit run streamlit/app.py
```

## Installation

To set up the repository, install the dependencies using the requirements file:

```bash
pip install -r streamlit/requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

For inquiries, please reach out here:
- dept.csprabhat@gmail.com
- mihirpanchal5400@gmail.com
- viraldalal04@gmail.com
- mayank265@iitp.ac.in
- asif@iitp.ac.in
