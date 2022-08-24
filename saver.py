import lm_dataformat as lmd

class Saver:
  def __init__(self, out_dir):
    self.ar = lmd.Archive(out_dir)

  def save(self):
      self.ar.commit()
  
  def add(self, data):
    self.ar.add_data(data)

  def add_all(self, data: list):
    [self.ar.add_data(d) for d in data]

  def close(self):
      self.ar.commit()
  