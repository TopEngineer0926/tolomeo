from app.repository import Repository
from app.repository.mongo import MongoRepository
import uuid

class Service(object):
  def __init__(self, repo_client=Repository(adapter=MongoRepository)):
    self.repo_client = repo_client

  def find_all_users(self, user_email):
    return self.repo_client.find_all_users({'email': user_email})
    

#   def find_kudo(self, repo_id):
#     kudo = self.repo_client.find({'user_id': self.user_id, 'repo_id': repo_id})
#     return self.dump(kudo)

  def create_user(self, new_user):
    return self.repo_client.create_user(self.prepare_user(new_user))

#   def update_kudo_with(self, repo_id, githubRepo):
#     records_affected = self.repo_client.update({'user_id': self.user_id, 'repo_id': repo_id}, self.prepare_kudo(githubRepo))
#     return records_affected > 0

  def delete_user_for(self, user_email):
    records_affected = self.repo_client.delete({'email': user_email})
    return records_affected > 0

  def prepare_user(self, new_user):
    data = new_user.data
    data['uuid'] = str(uuid.uuid4())
    return data
  
  def get_version(self):
    return {"data": self.repo_client.version()}