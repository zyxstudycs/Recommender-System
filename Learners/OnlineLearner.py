# Online Learner
# take in the user action, serve models

from ModelStore import ModelStore
from DatabaseInterface import DatabaseInterface
# from Webserver import Action
import Webserver
from Models.SimilarItemModel import SimilarItemModel
import logging

class OnlineLearner(object):
    logging.basicConfig(level=logging.INFO)

    def __init__(self, database, modelStore):
        self.db = database
        self.model_store = modelStore

    def trainModel(self, action):
        assert(isinstance(action, Webserver.Action))
        clustering_model = self.model_store.persistModels[ModelStore.CL_MODEL_KEY]
        similarity_model = SimilarItemModel(clustering_model)

        userId = action.userId
        itemId = action.itemId
        rating = action.rating

        item_feature_table = self.db.connTable[DatabaseInterface.ITEM_FEATURE_KEY]
        item_feature = item_feature_table.loc[[itemId]]

        #here I still add the training part of similarity_model
        similarity_model.train(item_feature, rating)

        self.pushModel(similarity_model, userId)

    def pushModel(self, model, userId):
        self.model_store.transientModels[ModelStore.SI_MODEL_KEY][userId] = model
