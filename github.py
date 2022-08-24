from decouple import config
import requests
from requests import Response
class Github:
  def __init__(self):
      self.token = config('GH_TOKEN')
  
  def request(self, endpoint: str, params: dict = None)->Response:
    return requests.get(endpoint, params=params, headers={
      "Authorization": f'token {self.token}',
      "Accept": "application/vnd.github+json",
    })