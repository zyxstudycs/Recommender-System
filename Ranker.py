# Ranker

import logging
import numpy as np

# rank the items from each recommendation module
# highly influenced by business strategy and varies from system to system
from DatabaseInterface import DatabaseInterface


class Ranker(object):
    logging.basicConfig(level=logging.INFO)
    def __init__(self, numberToServe, database):
        self.number_to_serve = numberToServe
        self.db = database

    def getUsedItems(self, userId):

        if type(userId) == type(1):
            history = self.database.connTable[self.database.HISTORY_KEY]
            return history[history['user_id'] == userId]['item_id'].tolist()
        else:
            return []

    def rerank(self,recommendationsTuple):
        # recommendationTupe is a tuple of (userId, recommendations)
        # recommendations is a dictionary of lists {RecType: Items}, RecType can be "online", "offline", "popular"
        # return the ranked recommendation
        # here is the strategy:
        # if the userId is -1, it means it is from anonymous user.
        # else remove the watched item and
        userId = recommendationsTuple[0]
        recommendations = recommendationsTuple[1]
        used_items = self.getUsedItems(userId)

        total_items = []
        for rec_type, items in recommendations.iteritems():
            # np.random.choice(items, size=100)
            total_items.extend(items)

        choiced_items = np.random.choice(list(set(total_items) - set(used_items)), self.number_to_serve)
        # np.random.choice(list(set(total_items) - set(used_items)), self.number_to_serve)

        return choiced_items



