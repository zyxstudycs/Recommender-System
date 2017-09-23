# Recommendation Engine

from ModelStore import ModelStore
import logging

class RecEngine(object):
    logging.basicConfig(level=logging.INFO)

    def __init__(self, userAnalyzer, modelStore, userActivityTable):
        self.user_analyzer = userAnalyzer
        self.model_store = modelStore
        self.user_activity_table = userActivityTable
        self.log = logging.getLogger(__name__)

    def provideRecommendation(self, request):
        user_type = self.user_analyzer.analyze(request, self.user_activity_table)
        recommendation = {}
        #first dealing with anonymous user, this time only use clustering
        if user_type[0] == "anonymous":
            online_model = self.model_store.getModel(ModelStore.SI_MODEL_KEY, request.userId)
            recs_online = online_model.provideRec()
            recommendation['online'] = recs_online
            self.log.info('online recs made')

            most_popular_model = self.model_store.getModel(ModelStore.MP_MODEL_KEY)
            recs_most_popular = most_popular_model.provideRec()
            recommendation['most_popular'] = recs_most_popular
            self.log.info('offline recs made')

            recommendationsTuple = (request.userId, recommendation)
        return recommendationsTuple



