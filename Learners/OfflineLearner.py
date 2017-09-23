# Offline Learner
# Read in user history data, make models

from ModelStore import ModelStore
from DatabaseInterface import DatabaseInterface
import logging
import numpy as np

class OfflineLearner(object):
    logging.basicConfig(level=logging.INFO)
    THRESHOLD_FOR_LR = 3.

    def __init__(self, database, modelStore):
        self.database = database
        self.modelStore = modelStore
        self.log = logging.getLogger(__name__)
        self.modelRegistry = [(ModelStore.KNN_MODEL_KEY, "k nearest neighbor most popular model"),
                                (ModelStore.MP_MODEL_KEY, "most popular item model"),
                                (ModelStore.CL_MODEL_KEY, "item feature clustering model"),
                                (ModelStore.CF_MODEL_KEY, "collaborative filtering model")]

    def trainModel(self):
        self.log.info('offline learning start to learn')
        #first dealing with clustering model, cause it could be used online
        clustering_model = self.modelStore.persistModels[self.modelStore.CL_MODEL_KEY]
        item_features = self.database.connTable[DatabaseInterface.ITEM_FEATURE_KEY]
        clustering_model.train(item_features)

        #then dealing with most popular model.
        most_popular_model = self.modelStore.persistModels[self.modelStore.MP_MODEL_KEY]
        history = self.database.connTable[DatabaseInterface.HISTORY_KEY]
        most_popular_model.train(history)

        #push all the trained models to the model store
        self.pushModel(clustering_model,self.modelStore.CL_MODEL_KEY)
        self.pushModel(most_popular_model, self.modelStore.MP_MODEL_KEY)
        self.log.info('offline learner end learning')

    def pushModel(self, model, key):
        self.modelStore.setModel(model, key)
        self.log.info('the trained model is pushed into model store')

