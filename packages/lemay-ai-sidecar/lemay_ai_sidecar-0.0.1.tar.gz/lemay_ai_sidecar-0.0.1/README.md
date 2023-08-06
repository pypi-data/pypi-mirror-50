# Sidecar: Augmenting Word Embedding Models With Expert Knowledge

The sidecar project provides a mechanism for customizing a pre-trained word embedding model, for application in a domain with plenty of jargon (e.g., *index* means one thing in a book, and another thing in a SQL database) and out-of-vacabulary words (e.g., *BigInteger* is not in the dictionary but encodes meaning in the context of the Java programming language).

This library takes in a dataset and a pre-trained model, and it returns back an LSTM neural network model for classifying text using the new custom model ("model"), the filename where the neural network model is saved on disk ("fname_sidecar"), and the filename where a new custom fasttext model is located on disk ("fname_custom"). The LSTM model makes a prediction on the concatenation of the a pre-trained model vector with the custom vector for the same text.

The **CSV dataset** input is processed as a pandas dataframe, where the column with text samples is named **"body"** and the column with the taget labels is named **"tags"**. To use this project for your own purposes, change the dataset passed to the framework, and feel free to try other pre-trained models as well.

The following is one key finding from this work:

![Results High Level Summary](https://github.com/lemay-ai/sidecar/blob/master/images/accuracy.png)

This repository was released by Lemay.ai as open source software under the license specified in this repository (GPLv3), and represents the work product described in the research paper "Sidecar: Augmenting Word Embedding Models With Expert Knowledge"

# Installation

First off, the current version of fasttext is not playing nicely with pip, and so you must, before installing this package, install fasttext via the command line. All other dependencies will auto-install. And so please begin by installing fasttext as follows:
```
pip3 install fasttext
```
Now, the following commands should get you the rest of the software:

```
git clone https://github.com/lemay-ai/sidecar.git
cd sidecar/
python3 setup.py install
```

# Testing

## WARNING: THIS TEST TAKES A LONG TIME TO RUN, AND GOBBLES RAM, SO ALLOCATE 16GB+ FOR THIS TEST

Test the library using the test data supplied in the repository as follows. It takes about 10 to 25 minutes to run the test:

```
python3 test.py
```

## NOTE: THIS TEST SHOULD WORK ON CPU, GPU, AND EVEN TPU... WE HAVE TESTED IT

# Testing Data Origin
The data for the paper was pulled from https://cloud.google.com/bigquery/public-data/stackoverflow

Example queries: 
```SQL
SELECT title, tags  FROM [bigquery-public-data:stackoverflow.posts_questions] where tags = 'php' LIMIT 10000
SELECT body, tags  FROM [bigquery-public-data:stackoverflow.posts_questions] where tags = 'c++' LIMIT 1000
```
