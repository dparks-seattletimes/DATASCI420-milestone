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

        self.unique_user_ids = self.__remove_downloaded_ids(self.unique_user_ids, StackexApi.USER_INFO)
        self.unique_answer_ids = self.__remove_downloaded_ids(self.unique_answer_ids, StackexApi.ANSWER_INFO)

    def __remove_downloaded_ids(self, ids, file):
        try:
            stored_dict = pickle.load(open(file, 'rb'))
        except FileNotFoundError:
            stored_dict = {}

        return list(set(ids) - set(list(stored_dict.keys())))

    def __generate_id_batch(self, ids):
        if not ids:
            return ids
        return [";".join([str(id) for id in ids]) for ids in np.array_split(ids, StackexApi.BATCH_COUNT)]

    def __save_items(self, items, id_key, file):
        id_info_dict = dict([(item[id_key], item) for item in items])
        try:
            stored_dict = pickle.load(open(file, 'rb'))
        except FileNotFoundError:
            stored_dict = {}

        updated_dict = {**stored_dict, **id_info_dict}
        pickle.dump(updated_dict, open(file, "wb"))

    def __fetch(self, url, backoff=0):
        print(f'Downloading {url} with backoff {backoff}...')
        sleep(backoff) if backoff else None
        json = self.stackoverflow.fetch(url)

        return json['items'], json['backoff']

    def user_info(self):
        backoff = 0
        user_ids_batch = self.__generate_id_batch(self.unique_user_ids)

        for ids in user_ids_batch:
            items, backoff = self.__fetch(f'users/{ids}', backoff)
            self.__save_items(items, 'user_id', StackexApi.USER_INFO)
        else:
            print('No user ids to download.')

    def answer_info(self):
        backoff = 0
        answer_ids_batch = self.__generate_id_batch(self.unique_answer_ids)

        for ids in answer_ids_batch:
            items, backoff = self.__fetch(f'answers/{ids}', backoff)
            self.__save_items(items, 'answer_id', StackexApi.ANSWER_INFO)
        else:
            print('No answer ids to download.')


if __name__ == "__main__":
    s = StackexApi(
        unique_user_ids=[449139, 98537, 1764254, 3226814],
        unique_answer_ids=[41341285, 51268787, 46930381, 20861606]
    )
    s.user_info()
    s.answer_info()
