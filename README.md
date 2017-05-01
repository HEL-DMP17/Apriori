# University of Helsinki - Data mining project 2017
Ege Can Özer/Agustin Zuñiga
Project main repository: https://github.com/HEL-DMP17/Apriori

## About project
### Overview
Our project is related with the student-level data, our goal is to find interesting
frequent patterns that could be related with things like the students performance,
social and educational frameworks, depending on the frequent patterns. i.e. the relation
between scores and gender, family income or parents education level. In order to do that
we will implement Apriori Algorithm as well as different approaches to handle the different
kind of attributes of the sample.

### Dataset
The data matrix has 9,679 rows and 17 columns, it does not contain missing values.
A detailed description of the data set could be find
in the following link: https://vincentarelbundock.github.io/Rdatasets/doc/mediation/student.html

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






