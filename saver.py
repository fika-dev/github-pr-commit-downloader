import lm_dataformat as lmd

class Saver:
  def __init__(self, out_dir):
    self.ar = lmd.Archive(out_dir)

  def __str__(self):
      return self.crawler_id

  def save(self):
      self.ar.commit()
  
  def add(self, data):
    self.ar.add_data(data)

  def close(self):
      self.ar.commit()
  