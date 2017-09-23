from sklearn.cluster import KMeans
from DatabaseInterface import DatabaseInterface


class ClusteringModel(object):
    def __init__(self, n_cluster=10):
        self.numb_cluster = n_cluster
        self.trained = False
        self.k_means = KMeans(self.numb_cluster)

    def train(self, itemFeatures):
        self.indexes = itemFeatures.index.tolist()
        self.model = self.k_means.fit_predict(itemFeatures.loc[:, "unknown":])
        self.trained = True
        return self.model


    def predict(self, itemFeatures):
        indices = []
        group = self.k_means.predict(itemFeatures.loc[:, "unknown":])
        satisfied_group = self.trained == group
        for i in range(len(self.indexes)):
            if satisfied_group[i]:
                indices.append(self.indexes[i])
        return indices


if __name__ == "__main__":
    connector = DatabaseInterface("../DATA")
    connector.startEngine()
    itemFeatures = connector.connTable["item_feature"]
    cluster_model = ClusteringModel()
    trained_cluster = cluster_model.train(itemFeatures)
    itemFeature = itemFeatures[0:1]
    print cluster_model.predict(itemFeature)
    print trained_cluster