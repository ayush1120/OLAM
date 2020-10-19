import os
import pandas as pd
import logging
import random

from logger import log


log.setLevel(logging.DEBUG)

class TextGenerator:

    def __init__(self,
            filePath=os.path.join(os.getcwd(), 'hindi_corpus_2012_12_19', 'Hi_Newspapers.txt'),
            dbType='HC Corpora',
            log=log):

        self.filePath = filePath
        self.dBType = dbType
        self.log = log
        self.loadDatabase()

    def getRandomText(self):
        size = len(self.data)
        index  = random.randint(1, size)
        return self.data.text.loc[index]
        


    def loadDatabase(self):
        if self.dBType == 'HC Corpora':
            self.loadHCDatabase()


    def loadHCDatabase(self):
        data = pd.read_csv(self.filePath, delimiter='\t', 
            names=['source', 'date', 'unnamed_1', 'unnamed_2', 'text'])
        self.data = data.loc[:,['source', 'date', 'text']]
        return self.data
    
    


class TextProcess:
    def __init__(self, log=log):
        self.log = log

    def preprocess(self, dataframe):
        self.log.info("In preprocess function.")
        dataframe1 = self.remove_nan(dataframe)
        # dataframe2 = self.lowercase(dataframe1)
        dataframe3 = self.remove_whitespace(dataframe1)
        dataframe4 = self.remove_emails(self, dataframe3)
        dataframe5 = self.remove_website_links(self, dataframe4)
        dataframe6 = self.remove_special_characters(dataframe5)
        # dataframe7 - self.remove_numbers(dataframe6)
        # self.remove_stop_words(dataframe8) # Doesn't return anything for now
        # dataframe7 = self.tokenize(dataframe6)

        self.log.info(f"Sample of preprocessed data: {dataframe4.head()}")

        return dataframe6

    def remove_nan(self, dataframe):
        """Pass in a dataframe to remove NAN from those columns."""
        return dataframe.dropna()

    def lowercase(self, dataframe):
        logging.info("Converting dataframe to lowercase")
        lowercase_dataframe = dataframe.apply(lambda x: x.lower())
        return lowercase_dataframe


    def remove_special_characters(self, dataframe):
        self.log.info("Removing special characters from dataframe")
        no_special_characters = dataframe.replace(r'[^A-Za-z0-9 ]+', '', regex=True)
        return no_special_characters

    def remove_numbers(self, dataframe):
        self.log.info("Removing numbers from dataframe")
        removed_numbers = dataframe.str.replace(r'\d+','')
        return removed_numbers

    def remove_whitespace(self, dataframe):
        self.log.info("Removing whitespace from dataframe")
        # replace more than 1 space with 1 space
        merged_spaces = dataframe.str.replace(r"\s\s+",' ')
        # delete beginning and trailing spaces
        trimmed_spaces = merged_spaces.apply(lambda x: x.str.strip())
        return trimmed_spaces

    def remove_stop_words(self, dataframe):
        # TODO: An option to pass in a custom list of stopwords would be cool.
        set(stopwords.words('english'))

    def remove_website_links(self, dataframe):
        self.log.info("Removing website links from dataframe")
        no_website_links = dataframe.str.replace(r"http\S+", "")
        return no_website_links


    def remove_emails(self, dataframe):
        no_emails = dataframe.str.replace(r"\S*@\S*\s?")
        return no_emails

    def expand_contractions(self, dataframe):
        # TODO: Not a priority right now. Come back to it later.
        return dataframe