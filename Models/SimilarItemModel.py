# similar item model
# underneath it is to use a clustering model
# for simplicity, return all in the same cluster if rating is higher or equal to 3; return empty cluster otherwise

from DatabaseInterface import DatabaseInterface
from ClusteringModel import ClusteringModel

class SimilarItemModel(object):
    THRESHOLD = 3.0 # if ratings are below threshold, it will not be used

    def __init__(self,clusteringModel):
        self.clustering_model = clusteringModel
        self.recommendations = []

    def train(self, itemFeature, rating):
        # only single record
        # each model learns one person's current interest
        # itemFeature = itemFeature.values.reshape(1, -1)
        indices = self.clustering_model.predict(itemFeature)

        if rating >= self.THRESHOLD:
            self.recommendations = indices
        else:
            self.recommendations = []

    def predict(self, itemFeature):
        # X should be item's category feature, only single record
        # return the similar items
        # itemFeature = itemFeature.values.reshape(1, -1)
        indices = self.clustering_model.predict(itemFeature)
        return indices

    def provideRec(self):
        return self.recommendations


if __name__ == "__main__":
    connector = DatabaseInterface("../DATA")
    connector.startEngine()
    itemFeatures = connector.connTable["item_feature"]

    cluster_model = ClusteringModel()
    cluster_model.train(itemFeatures)
    simularity_item_model = SimilarItemModel(cluster_model)

    item_feature = itemFeatures[0:1]
    simularity_item_model.train(item_feature, 3)
    print simularity_item_model.provideRec()


