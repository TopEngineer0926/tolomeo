class Repository(object):
  def __init__(self, adapter=None):
    self.client = adapter()

  def find_all(self, selector):
    return self.client.find_all(selector)

  def find_all_users(self, selector):
    return self.client.find_all_users(selector)
 
  def find(self, selector):
    return self.client.find(selector)
 
  def create_user(self, new_user):
    return self.client.create_user(new_user)
  
  def update(self, selector, kudo):
    return self.client.update(selector, kudo)
  
  def delete(self, selector):
    return self.client.delete(selector)
  
  def version(self):
    return self.client.version()
  
  def save_evidence(self, evidence):
    return self.client.save_evidence(evidence)
  
  def find_evidence(self, uuid):
    return self.client.find_evidence(uuid)
  
  def find_evidence_by_url(self, url):
    return self.client.find_evidence_by_url(url)
  
  def get_evidences(self):
    return self.client.get_evidences()