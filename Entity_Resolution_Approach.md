# Entity Resolution
Let us first consider what an entity is. Much as the key step in machine learning is to determine what an instance is, the key step in entity resolution is to determine what an entity is. Let’s define an entity as a unique thing (a person, a business, a product) with a set of attributes that describe it (a name, an address, a shape, a title, a price, etc.). That single entity may have multiple references across data sources, such as a person with two different email addresses, a company with two different phone numbers, or a product listed on two different websites. If we want to ask questions about all the unique people, or businesses, or products in a dataset, we must find a method for producing an annotated version of that dataset that contains unique entities.

# Approach
We have created an interface to take input of the entity (First Name + LastName, Location, Organization) from the user through argparse.
We have found various mentions of the entity in the web using two approaches
- [Using Google APP Engine API](https://cloud.google.com/appengine/training/fts_intro/)
- [Using Google Scrapper](https://pypi.org/project/GoogleScraper)
- Using Dedupe library to deduplicate , link and canonicalise data.

# [Using Google APP Engine API] (https://github.com/chandramoulirajagopalan/Entity_Resolution/blob/master/search_queries_using_google_api_engine.py)
We have used the query string from the input and made queries using the search method in the library. The output results are stored until we get to the end of the results. We use the library os, argparse and google.app.engine package for this job. Results are stored in a document file.

# [Using Google Scrapper] (https://github.com/chandramoulirajagopalan/Entity_Resolution/blob/master/search_queries_google_scrapper.py)

We have used the command line interface for the input from user using argparse. After securing the input we input it in a file and then use Google Scraper package to search for the queries and results are stored in a json file. Finally the json file is converted into csv file. The csv file is fed as an input for the deduplication process.
Libraries used json, csv, os and argparse

# [Deduplicate , linking and canonicalise data](https://github.com/chandramoulirajagopalan/Entity_Resolution/blob/master/Entity_Resolution_Using_Dedupe.py)
Dedupe works by engaging the user in labeling the data via a command line interface, and using machine learning on the resulting training data to predict similar or matching records within unseen data.
When comparing records, rather than treating each record as a single long string, Dedupe cleverly exploits the structure of the input data to instead compare the records field by field. The advantage of this approach is more pronounced when certain feature vectors of records are much more likely to assist in identifying matches than other attributes. Dedupe lets the user nominate the features they believe will be most useful.
Libraries used - future, dedupe, os, csv, re, collections, argparse, numpy and unidecode.
