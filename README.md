# Survista, a light weught CMS 📄 and Search Engine 🔍 for you Survey Data

The Canada School of public service is a federal department responsible for teaching and identifying valuable and essential skills for the Government of Canada.
As such we conduct a wide array of surveys to identify learning satisfaction and where to improve in order to optomize learning delivery in our events and courses.
The current tools used to fulfill this requirement are inefficient and make it very difficult to extract value from qualitative textual data where most of it is.
As such the Digital Innovation Services as part of the Digital Academy identified a need for an end to end survey solution that would allow analysts to quickly design
and implement an effective surveys with an automated data pipeline and API. Rudementary NLP such as POS, Sentiment Analysis and Keyword Extraction is built in to allow 
quick filtering and extraction of useful insights from qualitative data. The API allows access to clean machine readable data in the form of JSON allowing the delivery of
data to third party services, such as Power BI in an automated fashion almost live. This will allow our organization to be data driven and quickly able to action extract 
insight and action from our learners in order to be able to substantially improve our offerings.

This repo encompasses the CMS, pipeline and API side of things. To take a look at the actual survey design tool please have a look at this [repo](https://github.com/DIS-SIN/Evalhalla) 

<b> Please note this tool is still in development and has not been released yet </b>

# Technical Overview 🛠️

Roll credits 📽️

## Main technical Stack 

* [Flask](http://flask.pocoo.org/docs/1.0/): Flask is a python micoframwork for building extandable and malluable web services. Since we are prodominently building a data pipeline
it is perfect for our needs allowing for great flexibility.

* [SQLAlchemy](https://www.sqlalchemy.org/): We depend heavy on SQLAlchemy for the effecient abstraction of our database layer. It is an ORM in essence. Instead of having to manage SQL files and the translation of that
to data objects in python we instead can create class definitions which in turn define our database schema and the relationships between them

* [Postgres](https://www.postgresql.org/): The worlds most beloved open source database engine and server


## Use of third party tools


* [Sentry](https://sentry.io/welcome/) : An all purpose logging tool with an emphesis on error logging. We are using this in production to help inform us
of any errors that occur with a rich amount of debugging information to help us mitigate issues not caught in development

* [Google Natural Language API](https://cloud.google.com/natural-language/) : What we are using for Sentiment Analysis. While building our own Sentiment Analysis 
models with domain specific data would probably be better. Our current priority is to build a modular data pipeline and as such are currently outsourcing this step 
to Google's Natural Language API. What's more Google's API supprts 6 languages. This removes the hassle of having to manage a the life cycle and deployment of multiple Sentiment Analysis
models until it needs to be addressed

* [spaCy](https://spacy.io): Industrial grade natural language processing. spaCy built is built with Cython and contains pretrained neural nets that allow for Part of Speech tagging and
normalization of text for keyword extraction with incredible speed.

* [Celery](http://www.celeryproject.org): We are using celery as a task queue to allow us to ansychronously schedule and execute tasks such as munging of data and running textual data through our 
NLP pipeline

## Tools we are looking at 

* [ElasticSearch](https://www.elastic.co/products/elasticsearch): We are looking to see if we can incorporate ElasticSearch as an engine and inteface for natural language search on textual data

* [Apache Kafka](https://kafka.apache.org/): Since we are looking to enable live streaming of data we are looking for a platform to do this at scale. Apache Kafka is an optimal solution for this

* [Neo4J](https://neo4j.com/): Neo4j is a NoSQL Graph Database. It allows for a more natural way of modeling data and is able to scale to millions upon millions of records and relationships with ease. We are evaluating this as a way to escape the bottleneck of relational databases and for our data pipeline.

## Testing 🧪

This is an area that is currently lacking in this project but are working to address this as the project matures. Testing solutions we are looking at

* [PyTest](https://docs.pytest.org/en/latest/) Simple and highly effective framwork and package for building automated tests in python

* [PostMan](https://www.getpostman.com/) Highly advanced and visual friendly API development platform which allows you to build your API suite and create automated tests on them. We are looking at using PostMan to created automated client side tests

* [BDD](https://github.com/DIS-SIN/bdd-test-runner) Behavior Driven Test Development allows us to write the technical specification of a system in simple and plain language and the build tests in an automated fashion. The system must meet these tests in order to be deployed. This ensuress we meet the requirements of our clients and users

# Deployment

This tool is still in development and is currently not in a deployable state. We are however planning to dockerize all components of this system such that it can be deployed in most cloud environments.

# Setup ⚙️

We will walk you through on how to get the app up and running 

## prequesites 

* [python3](https://www.python.org/downloads/)

* pip3 (Usually this comes with the python download)

* [Postgres](https://www.postgresql.org/) of minimum version 10.x

## Get your environment set up

The fisrt thing you will need to do is get your environment setup

First clone the repo into your directory. If you are windows I recommend you set up WSL or if that is too much, download and use git bash. If you are darwin this should be pretty much be the same 

```sh 
cd ~/
git clone https://github.com/DIS-SIN/Evaluations.git
```

The next step is to setup the virtual environment 

```sh
cd Evaluations
python -m venv venv
```

Install the packages in the requirements.txt

```sh
pip install -r requirements.txt
```

to activate your environment 

```sh
source venv/bin/activate
```

This should then show something like this 

```sh
(venv)user@user:~/Evaluations$
```

## Environment Variables 🌲

There is a couple of environment variables to take note of. I will split the description in terms of behavior in the development environment and the production environment

*  ```APP_SECRET_KEY```: This is the secret key used to sign cookies
    * ```DEVELOPMENT```: This environment variable is ignored and an dummy key is set as can be seen in the application factory ```src/__init__.py```
    * ```PRODUCTION```: This environment variable needs to be set in production. The application will fail to run in production without this environment variable. It is recommended that you set this to a random 32 character length string. As the name implies this environment variable needs to be a secret. It is preferable you do not store this environment variable in plain text but if you are for whatever reason ensure that it is stored securely and is not exposed (i.e. by accidently uploading it to github)
* ```APP_SQLALCHEMY_DATABASE_URI```: The URI of the postgres database
    * ```DEVELOPMENT```: This environment variable will be ignored the default uri is set to the following ```postgresql+psycopg2://postgres:password@localhost:5432/evaluations```. You can change this default in the application factory ```src/__init__.py```
    * ```PRODUCTION```: This environment variable variable needs to be set in production. The application will fail to run in production without this environment variable. It is recommended that you do not store this environment variable in plain text. If for whatever reason you need too then ensure it's stored securely. If the value of this environment variable has been exposed for whatever reason, you should consider that the public has access to your production database. Proceed to panic and frantically change your password or find your database wiped clean. 
* ```APP_SENTRY_URL```: The URL of your sentry endpoint
   * ```DEVELOPMENT```: This environment variable will be ignored. Sentry is not set up in the development environment
   * ```PRODUCTION```: Sentry is an optional feature. If you do not set this environment variable sentry services will simply be turned off. A warning will be emitted to inform you of such 
* ```GOOGLE_APPLICATION_CREDENTIALS```: The path to the JSON credentials to your google services
   * ```DEVELOPMENT```: This is an optional feature. If you do not set this environment variable in development a flag will be set in the config to not use the Google Natural Language API for Sentiment Analysis
   * ```PRODUCTION```: Same behavior as development

<b> A fair warning. We can only encorage you to follow best practices regarding security. We are not responsible for the draining of your credits on GCP, The flooding of your sentry inbox with fake events or the loss of your data </b>


## Setting up your database 

We have incorporated a couple of cli utilities for your convenience. To initialise your data base simply issue the following command

```sh
flask init-db
```

If you wish to wipe your database 
```sh
flask delete-db
```

## Testing Sentry and Google Natural Language API 

If you would like to ensure that your sentry and google natural language configuration works. You can use ```/debug-sentry``` to send a dummy event to your sentry instance and ```/debug-nlp``` to send some dummy data to the Google Natural Language API and see the response.

## Running the development environment

Set the environment variable ```FLASK_ENV``` to ```development``` then 
```sh
flask run
```
### Running the production environment
Set the environment variable ```FLASK_ENV``` to ```production``` or clear this environment variable entirely then

```sh 
flask run
```

# Other Resources 

This application is under heavy development. We are working to provide documentation on the API as soon as possible. If you have any questions please feel free to open an issue on this repo or contact me at omar.nasr@canada.ca