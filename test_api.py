import unittest
import json
from app import app
from connexion.resolver import RestyResolver

BASE_URL = "http://127.0.0.1:9090/v1.0/items/"

class TestItemApi(unittest.TestCase):
    
    def setUp(self):
        
        self.client = app.app.test_client()
        self.client.testing = True
        

    def test_all(self):

        item = { "id": 999999,
                 "name": "name"
                }

        updated_item = { "id": 999999,
                         "name": "a name"
                        }
        non_existing_item_id = 999456999678

        ## get all items        
        response = self.client.get(BASE_URL)
        data = json.loads(response.get_data())

        # store number of items
        counter = len(data)

        # expecting respose code 200
        self.assertEqual(response.status_code, 200)

        ## add new item
        response = self.client.post(BASE_URL, 
                                    headers = {"Content-Type": "application/json"}, 
                                    data = json.dumps(item))
        # expecting respose code 201
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))

        # check items data
        self.assertEqual(999999, data['id'])
        self.assertEqual("name", data['name'])

        ## get all items
        response = self.client.get(BASE_URL)
        
        # expecting respose code 200
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())

        # number of items in response shuld be incresead for one
        self.assertEqual((counter + 1), len(data))

        ## get item by id
        response = self.client.get(BASE_URL+'{}'.format(item['id']))
        
        # expecting respose code 200
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        
        # check items data
        self.assertEqual(999999, data['id'])
        self.assertEqual("name", data['name'])

        ## try to add same item again
        response = self.client.post(BASE_URL, 
                                    headers = {"Content-Type": "application/json"}, 
                                    data = json.dumps(item))

        # expecting respose code 409
        self.assertEqual(response.status_code, 409)

        ## update
        response = self.client.put(BASE_URL+'{}'.format(item['id']), 
                                   headers = {"Content-Type": "application/json"}, 
                                   data = json.dumps(updated_item))
        # expecting respose code 200
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        # check items data
        self.assertEqual(999999, data['id'])
        self.assertEqual("a name", data['name'])


        ## update item which does not exists
        response = self.client.put(BASE_URL+'{}'.format(non_existing_item_id), 
                                   headers = {"Content-Type": "application/json"}, 
                                   data = json.dumps(updated_item))

        ## delete
        response = self.client.delete(BASE_URL+'{}'.format(item['id']), 
                                      headers = {"Content-Type": "application/json"})

        # expecting response code 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Item ' + str(item['id']) + ' deleted', response.data.decode())

        ## get all items        
        response = self.client.get(BASE_URL)
        data = json.loads(response.get_data())

        self.assertEqual(counter, len(data))

        ## get item by id
        response = self.client.get(BASE_URL+'{}'.format(item['id']))
        # expecting respose code 404
        self.assertEqual(response.status_code, 404)

        ## delete item which does not exists
        response = self.client.delete(BASE_URL+'{}'.format(non_existing_item_id), 
                                      headers = {"Content-Type": "application/json"})

        # expecting response code 404
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()