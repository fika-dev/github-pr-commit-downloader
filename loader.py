import json

class Loader:
  def __init__(self, repo_json_path):
    with open(repo_json_path, 'r') as fp:
      searched = json.load(fp)
      self.repos = searched['items']
      self.repo_length = searched['count']
      self.meta = searched['parameters']

  def get(self, index:int):
      return self.repos[index]