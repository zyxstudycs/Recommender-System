# RecommenderSystem
This is a general-purpose recommender system, using feature-based modeling, content-based filtering, collaborative filtering (matrix factorization) and clustering method. This system is able to provide hybrid online/offline recommendations for anonymous users, new users (cold-start) and old users.

# Architecture of the system.
![alt text](https://github.com/zyxstudycs/Recommender-System/blob/master/DATA/architecture.png)

# Details of the system.
1. Web server is the main class. All other classes should be instantiated in it. Web server can take two types of inputs: 
   (a). userId, (b) userAction.
2. If the web server receives a userId, it will send the request to an object called userTypeAnalyzer, which will determine the user type (see figure above).
3. For different user types the recommendation engine will pull different models from the model store and score over all items to provide recommendation.
4. The ranker will organize the recommendations from different models. Here only make sure there are no overlapped and visited items. The final recommendation will randomly pick K of them.
5. Model store contains the model object trained in the online learner and offline learner. Here simply use a hashmap of model name and model objects.
6. The offline learner trains the following models(Not finish): (a) a KNN model for feature- based model. (b) a collaborative filtering model with a content-based model on items with few ratings (c) a KMean model on item-feature. (d) A simple most popular item computation.
7. The online learner here do one thing(finished): if a user, no matter what type, pick an item (userAction), there should be T similar items randomly picked from the KMean cluster model.
8. For anonymous user, only most popular and online items will be served; For new user, most popular, online items and feature-based model prediction will be used; For old user, most popular, online items and collaborative filtering prediction will be used.
9. Besides feeding to online learner, the userAction data will also be saved into the database for registered user.
10. There is a function in web server called increment(), this function will trigger the offline model learning on the current data and online model cleaning up. This is to simulate the actual situations for online and offline training.
