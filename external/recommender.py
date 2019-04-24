# [Introduction To Recommendation system In Javascript](https://becominghuman.ai/introduction-to-recommendation-system-in-javascript-74209c7ff2f7)
# [Recommender Systems in Python: Beginner Tutorial](https://www.datacamp.com/community/tutorials/recommender-systems-python)
# [An Introductory Recommender Systems Tutorial](https://medium.com/ai-society/a-concise-recommender-systems-tutorial-fa40d5a9c0fa)

import copy
import pandas as pd
import numpy as np

"""
What tp recommend?
1. Recommend meal events to attend
2. Recommend users to follow

How to recommend?
1. Recommend based on user profile (preferences)
  - recommend meal events that offer cuisine to the user's liking
  - sorted by host avg rating / distance / event date
2. Recommend based on meal history
  - recommend users that have participated the most common meal events
  - sorted by # of meal events participated together
3. Recommend based on meal event rating
  - recommend meal events based on user similarty determined by rating
  - recommend meal events that similar user hosts / is going to attend
4. Random Recommendation
  - recommend random meal events
  - sorted by host avg rating / distance / event date

Inputs:
user_df = pd.DataFrame(
    columns=['_id', 'username', 'address.zip', 'fav_cuisine'])
review_df = pd.DataFrame(
    columns=['_id', 'author', 'event_id', 'recipient', 'rating', 'comment', 'tipping'])
event_df = pd.DataFrame(columns=['_id', 'host_id', 'guest_list', 'num_guests',
                        'cuisine_type', 'event_datetime', 'address.zip', 'status'])
meal_history_df = pd.DataFrame(
    columns=['host_id', 'guest_id', 'event_id', 'status'])

Output:
a list of event id's
"""


class UCookRecommender(object):

    def __init__(self, user_id, event_df, user_profile=None, num_rec=10):
        self.user_id = user_id
        self.event_df = event_df
        self.user_profile = user_profile
        self.num_rec = num_rec
        self.recs = list()

    def get_rand_recs(self, exclude=None):
        """
        Get random recommendations for a NEW user
        """
        rand_indices = np.random.randint(
            low=0, high=self.event_df.shape[0], size=2*self.num_rec)
        rand_event_ids = list(self.event_df.iloc[rand_indices, 0].values)
        if exclude:
            rand_event_ids = list(
                filter(lambda id: id not in exclude, rand_event_ids))
        return list(set(rand_event_ids[:self.num_rec]))

    def get_profile_recs(self, exclude=None):
        """
        Get recommendations based on user profile settings
        """
        if not self.user_profile:
            return
        fav_cuisine = list(self.user_profile['fav_cuisine'])
        rec_event_ids = list(self.event_df[self.event_df['cuisine_type'].isin(
            fav_cuisine), '_id'])  # sort by what
        if exclude:
            rec_event_ids = list(
                filter(lambda id: id not in exclude, rec_event_ids))
        return rec_event_ids[:self.num_rec]

    @staticmethod
    def normalize(df, exclude_col):
        normalize_cols = copy.copy(list(df.columns))
        normalize_cols.remove(exclude_col)
        max_df = pd.DataFrame(
            np.tile(df[normalize_cols].max(axis=0), (df.shape[0], 1)))
        min_df = pd.DataFrame(
            np.tile(df[normalize_cols].min(axis=0), (df.shape[0], 1)))
        max_df.columns = normalize_cols
        min_df.columns = normalize_cols
        max_df.index = df[normalize_cols].index
        min_df.index = df[normalize_cols].index
        df[normalize_cols] = (max_df - df[normalize_cols]) / \
            (max_df - min_df + .000000001)
        return df

    @staticmethod
    def aggregate_scores(df, exclude_col):
        res = pd.DataFrame()
        res[exclude_col] = df[exclude_col]
        res['score'] = 0
        for i in range(1, df.shape[1]):
            res['score'] += df[df.columns[i]]
        return res

    def compute_sim(self, user_ids, review_df):
        """
        Finding similar users
        euclid = math.sqrt((x1-y1)**2 + (x2-y2)**2 + ...), the smaller, the more similar
        reuclid = 1 / (1 + euclid), the larger, the more similar
        """
        user_reviews = review_df[review_df['author.id'] == self.user_id][[
            'event_id', 'rating', 'comment', 'tipping']]
        user_reviews = UCookRecommender.normalize(
            user_reviews, exclude_col='event_id')

        reuclids = []
        for other_userid in user_ids:
            other_user_reviews = review_df[review_df['author'] == other_userid][[
                'event_id', 'rating', 'comment', 'tipping']]
            other_user_reviews = UCookRecommender.normalize(
                other_user_reviews, exclude_col='event_id')

            sum_sq = 0
            for j in range(user_reviews.shape[0]):
                user_event = user_reviews.iloc[[j], :]
                event = user_reviews.iloc[j, 0]
                # common events
                if event in list(other_user_reviews['event_id']):
                    other_user_event = other_user_reviews[other_user_reviews['event_id'] == event]
                    for col in user_event.columns[1:]:
                        sum_sq += (user_event[col].values[0] -
                                   other_user_event[col].values[0]) ** 2
            euclid = np.sqrt(sum_sq)
            reuclid = 1 / (1 + euclid)
            reuclids.append(reuclid)

        similarity_df = pd.DataFrame()
        similarity_df['userid'] = user_ids
        similarity_df['similarity'] = reuclids

        # Ranking users
        similarity_df = similarity_df[similarity_df['userid'] != self.user_id]
        similarity_df[similarity_df['userid'] != self.user_id].sort_values(
            by='similarity', axis=0, ascending=False, inplace=True)

        return similarity_df

    def recommend(self, user_ids, review_df):
        """
        Recommendation based on rating system
        """
        # better cache the results
        user_reviews = review_df[review_df['author.id'] == self.user_id][[
            'event_id', 'rating', 'comment', 'tipping']]
        user_reviews = UCookRecommender.normalize(
            user_reviews, exclude_col='event_id')

        similarity_df = self.compute_sim(user_ids, review_df)

        candidates = []
        for other_userid in user_ids:
            other_user_reviews = review_df[review_df['author'] == other_userid][[
                'event_id', 'rating', 'comment', 'tipping']]
            for j in range(other_user_reviews.shape[0]):
                event = other_user_reviews.iloc[j, 0]
                if event not in list(user_reviews['event_id']) and event not in candidates:
                    candidates.append(event)

        for i in similarity_df.index:
            other_userid = similarity_df['userid'][i]
            other_user_reviews = review_df[review_df['author'] == other_userid][[
                'event_id', 'rating', 'comment', 'tipping']]
            other_user_reviews = UCookRecommender.normalize(
                other_user_reviews, 'event_id')
            other_user_reviews = UCookRecommender.aggregate_scores(
                other_user_reviews, 'event_id')
            for event in candidates:
                if event in list(other_user_reviews['event_id']):
                    similarity_df.loc[i, event = (
                        other_user_reviews.loc[other_user_reviews['event_id'] == event,
                                              'score'] * similarity_df.loc[i, 'similarity']).values[0]
                else:
                    similarity_df.loc[i, event] = 0

        ranking_pool = pd.DataFrame(similarity_df.sum(axis=0, skipna=True))
        ranking_pool.columns = ['total']
        ranking_pool['total / sim.sum']= ranking_pool['total'] /
            ranking_pool.loc['similarity', :].values[0]
        ranking_pool.drop('similarity', axis=0, inplace=True)
        ranking_pool.sort_values(by='total / sim.sum',
                                 ascending=False, inplace=True)

        recs = list(ranking_pool.index[:self.num_rec])
        return recs
