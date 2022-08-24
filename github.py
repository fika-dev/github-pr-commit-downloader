from decouple import config
class Github:
  def __init__(self):
      self.token = config('GH_TOKEN')
      
