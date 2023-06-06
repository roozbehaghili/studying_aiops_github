# Characteristics of AIOps Projects - Replication Package

This repository contains the replication package for the paper "Studying the Characteristics of AIOps Projects on GitHub".

## Introduction

We organize the replication package into three file folders.

1. Experiments: this folder contains code for our main experiments (i.e., extracting GitHub metrics for projects (RQ1) and analyze projects in terms of code quality (RQ3));
2. Results: this folder contains the results CSV files for all of our research questions;
3. Results analysis: this folder contains code for analyzing the dataset and experiment results.

The needed libraries and versions can be found on `requirements.txt` file.

## Install
```bash
git clone https://github.com/AIOpsstudy/understanding_aiops
pip install -r requirements.txt
```

## Experiments

This part contains code for our main experiments for RQ1 and RQ3. All code could be found under the `experiments` folder.
We have the following experiment code available:
- `github_aiops.ipynb` contains code for extracting GitHub metrics for our set of AIOps projects.
- `github_ml.ipynb` randomly selects repositories with the keywords `machine-learning` and `deep-learning`, and then extract their GitHub metrics.
- `github_general.ipynb` randomly selects repositories all over GitHub and then extract their GitHub metrics.
- `sonarqube` contains code for cloning projects, sending the codes to SonarQube server, analyzing the source codes, and extracting the results from SonarQube. To download and install a SonarQube instance, please refer to [their documentations](https://docs.sonarqube.org/latest/setup/install-server/).

## Results
This part contains the output data from our main experiments. All output CSV files could be found under the `results` folder.

## Result Analysis
This part contains code for the analysis of our experiment results. All code could be found under the `analysis` folder. 
