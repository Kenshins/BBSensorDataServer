import unittest
import sensor_receiver
from unittest.mock import MagicMock

class TestSum(unittest.TestCase):
    def test_request_sensors_return_None_on_bad_status_code(self):
        print("hej")
    #    response.status_code = MagicMock(return_value=400)
    #    print(response.status_code)
        
if __name__ == '__main__':
    unittest.main()