from abc import abstractmethod


class BaseJob:
    def __init__(self, *args, **kwargs):
        self.ie_prediction_api = 'https://api.insights.cropwise.com/v2.0/predictions'
        self.data = None
        self.context = kwargs.get('context')
        self.seed = kwargs.get('seed')

    @abstractmethod
    def prepare(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError