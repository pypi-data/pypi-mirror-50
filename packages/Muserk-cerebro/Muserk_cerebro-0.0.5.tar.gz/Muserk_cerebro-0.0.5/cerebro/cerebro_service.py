""" Cerebro Service """
import logging
import requests

LOGGER = logging.getLogger(__name__)


class CerebroService:
    """ A service for interacting with Cerebro """

    def __init__(self, cerebro_url: str):
        self._cerebro_url = cerebro_url

    def finished(self, task_id: str, **kwargs):
        """ Tells Cerebro that a Task has finished """
        requests.post(
            url=f'{self._cerebro_url}/tasks/{task_id}/finished',
            data=kwargs
        )
