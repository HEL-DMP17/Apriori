# University of Helsinki - Data mining project 2017
Ege Can Özer/Agustin Zuñiga
See the project's main page for full documentation at: https://hel-dmp17.github.io/Apriori/

## About project
### Summary
The project deals with the student-level data (ICPSR 4275) to find
frequent itemsets and extract associaton rules. We are hoping to find
social, educational, and cognitive relations. For instance, the students' performance, 
gender, family income, parents' education level may correlate with each other.
In order to do that we are using Apriori algorithm to mine frequent itemsets. We also
have provided some visualization methods, which are feasible to analyze the results.

### Dataset
We are using student-level data to study the classic data mining algorithm (Apriori). Briefly,
the dataset approximately consists of 15000 records and 1600 features. However, we are focused
only on 16 features. List of selected features could be seen in preprocessor.py file.

The dataset can be downloaded from the following link: http://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/4275

## How to install
### Prerequisites
Arules is implemented in python 3.5.2 and depends on lxml library

### Installation
You can install and run the program from scratch as follows
~~~shell
git clone https://github.com/HEL-DMP17/Apriori.git
cd Apriori
pip install -r requirements.txt
python arules.py
~~~

You can check the all optional arguments using:
~~~shell
python arules.py -h
~~~

All optional arguments are as follows:
~~~shell
usage: arules.py [-h] [-f FILE] [-s SUPPORT] [-c CONFIDENCE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The dataset pathdata/samples.txt
  -s SUPPORT, --support SUPPORT
                        The minimum support count, DEFAULT: 2.0
  -c CONFIDENCE, --confidence CONFIDENCE
                        The minimum confidence, DEFAULT: 0.374
~~~






