import cognitive_face as CF
import uuid
import json
import time

class MsFace:
  def __init__(self, person_group_id, force_create=False):
    self.person_group_id = person_group_id
    self.fetch_set_creds()
    current_groups = CF.person_group.lists()
    
    if len([x for x in current_groups if x['name'] == person_group_id]) == 0:
      print('group doesn\'t exist:', person_group_id)
      if force_create:
        print('creating person group:',person_group_id)
        res = CF.person_group.create(person_group_id)
        print(res)
      else:
        raise NameError('try force_create to force this group to be created')
    else:
      print('group already exists. ready to go.')
      
  def fetch_set_creds(self):
    creds = json.loads(open("creds/ms-face.json","r").read())
    self.key1 = creds['key1']
    self.key2 = creds['key2']
    CF.Key.set(self.key1)

  def get_people(self):
    return CF.person.lists(self.person_group_id)
  
  def get_person_for_id(self,person_id):
    return CF.person.get(self.person_group_id,person_id)
  
  def get_person_for_name(self,full_name):
    all_current_people = CF.person.lists(self.person_group_id)
    these_current_people = [x for x in all_current_people if x['name'] == full_name]
  
    if len(these_current_people) > 0:
      print('person ', full_name, 'exists')
      print(these_current_people[0])
      return these_current_people[0]
    else:
      return None
    
  def find_or_create_person(self,first_name,last_name):
    full_name = "%s %s" % (first_name, last_name)
    existing_person = self.get_person_id_for_name(full_name)
    if existing_person:
      print("person ", full_name, "already exists: id=", existing_person)
      return existing_person
    else:
      print("person ", full_name, "doesn't exist.  creating...")  
      res = CF.person.create(self.person_group_id, full_name, json.dumps({'first_name': first_name, 'last_name': last_name}))
      return res

  def add_face(self,person_id,img_url):
    try:
      resFace = CF.person.add_face(img_url,self.person_group_id, person_id)
      print(resFace)
    except CF.util.CognitiveFaceException as err:
      print("invalid image!")
      print(err)
      
  def face_detect(self,img_url):
    result = CF.face.detect(img_url)
    print(result)
    return result[0]['faceId']
    
  def face_identify(self,img_url):
    face_id = self.face_detect(img_url)
    res = CF.face.identify([face_id],self.person_group_id)
    return {
      'response': res,
      'candidates_detail': map(lambda x: self.get_person_for_id(x['personId']),res[0]['candidates'])
    }
    
  def add_face_for_name(self,first_name,last_name,img_url):
    person = self.find_or_create_person(first_name,last_name)
    person_id = person['personId']
    self.add_face(person_id,img_url)

# msface = MsFace('facebook-friends-small')
# print msface.get_people()
# print msface.get_person_for_name(full_name)
# print msface.face_identify(img_url)
# print msface.get_person_for_id(person_id)
# msface.add_face(person_id,img_url)