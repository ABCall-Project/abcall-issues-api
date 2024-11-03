import unittest
import json
from flaskr.utils.json_custom_encoder import JSONCustomEncoder

class MockObject:
    def to_dict(self):
        return {"key": "value"}

class TestJSONCustomEncoder(unittest.TestCase):
    def test_encode_object_with_to_dict(self):

        obj = MockObject()
        

        encoded_json = json.dumps(obj, cls=JSONCustomEncoder)
        

        self.assertEqual(encoded_json, '{"key": "value"}')

   
