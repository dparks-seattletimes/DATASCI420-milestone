from time import sleep

from stackapi import StackAPI
import pickle
import numpy as np


class StackexApi(object):
    BATCH_COUNT = 2
    USER_INFO = 'user_info.p'
    ANSWER_INFO = 'answer_info.p'
    
    def __init__(self, unique_user_ids=[], unique_answer_ids=[]):
        self.unique_user_ids = unique_user_ids
        self.unique_answer_ids = unique_answer_ids
        self.stackoverflow = StackAPI('stackoverflow')
        self.__remove_downloaded_ids()

    def __remove_downloaded_ids(self):
        try:
            stored_user_dict = pickle.load(open(StackexApi.USER_INFO, 'rb'))
        except FileNotFoundError:
            stored_user_dict = {}

        self.unique_user_ids = list(set(self.unique_user_ids) - set(list(stored_user_dict.keys())))

    def __generate_id_batch(self, ids):
        if not ids:
            return ids
        return [";".join([str(id) for id in ids]) for ids in np.array_split(ids, StackexApi.BATCH_COUNT)]

    def __save_user_items(self, items):
        id_info_dict = dict([(item["user_id"], item) for item in items])
        try:
            stored_dict = pickle.load(open(StackexApi.USER_INFO, 'rb'))
        except FileNotFoundError:
            stored_dict = {}

        updated_dict = {**stored_dict, **id_info_dict}
        pickle.dump(updated_dict, open(StackexApi.USER_INFO, "wb"))

    def __fetch(self, url, backoff = 0):
        print(f'Downloading ${url} with backoff ${backoff}...')
        sleep(backoff) if backoff else None
        json = self.stackoverflow.fetch(url)

        return json['items'], json['backoff']

    def user_info(self):
        backoff = 0
        user_ids_batch = self.__generate_id_batch(self.unique_user_ids)
        print(user_ids_batch)
        for ids in user_ids_batch:
            items, backoff = self.__fetch(f'users/{ids}', backoff)
            self.__save_user_items(items)


if __name__ == "__main__":
    s = StackexApi([449139, 98537, 1764254, 3226814])
    s.user_info()