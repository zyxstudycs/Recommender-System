# most popular model
# here it is a simple design: find the one with highest score with most of the users
import pandas as pd
import logging
from DatabaseInterface import DatabaseInterface

class MostPopularModel(object):
    N_Freq_limit = 0.001

    def __init__(self):
        self.recs = []
        self.log = logging.getLogger(__name__)


    def train(self, history):
        # X must be a dataframe, with the second key as itemID, and third key as ratings
        self.rating_mean = history.groupby(['item_id'])['rating'].mean()
        count = history.groupby(['item_id'])['user_id'].count().rename('count')
        result = pd.concat([self.rating_mean, count], axis=1)
        self.recs = result[result['rating']>4][result[result['rating']>4]['count']>100].index.tolist()
        self.log.info("the most popular model is trained")

    def predict(self,X):
        # X can only be a list of itemID's
        # note: this method return dataframe with index of item_id, and first column mean rating
        return None

    def provideRec(self):
        return self.recs


if __name__ == "__main__":
    connector = DatabaseInterface("../DATA")
    connector.startEngine()
    history = connector.connTable["history"]
    most_popular_model = MostPopularModel()
    most_popular_model.train(history)
    print most_popular_model.provideRec()