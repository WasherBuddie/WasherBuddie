import unittest
from unittest.mock import MagicMock, patch
from src.Service_Layer.Interaction_Manager import Interaction_Manager
from src.Service_Layer.Machine import Machine
from src.Service_Layer.User import User
import src.Service_Layer.Notification_Manager

class TestInteractionManager(unittest.TestCase):

    def setUp(self):
        self.manager = Interaction_Manager()

    @patch('src.Service_Layer.Machine')
    def test_add_washer_success(self, MockMachine):
        MockMachine.return_value = None  
        result = self.manager.add_washer()
        self.assertTrue(result)
        MockMachine.assert_called_once_with('Washer')

    @patch('src.Service_Layer.Machine')
    def test_add_washer_failure(self, MockMachine):
        MockMachine.side_effect = Exception("Failed to create washer")
        result = self.manager.add_washer()
        self.assertFalse(result)

    @patch('src.Service_Layer.Machine')
    def test_add_dryer_success(self, MockMachine):
        MockMachine.return_value = None  
        result = self.manager.add_dryer()
        self.assertTrue(result)
        MockMachine.assert_called_once_with('Dryer')

    @patch('src.Service_Layer.Machine')
    def test_add_dryer_failure(self, MockMachine):
        MockMachine.side_effect = Exception("Failed to create dryer")
        result = self.manager.add_dryer()
        self.assertFalse(result)

    @patch('src.Service_Layer.Notification_Manager.send_ping')
    def test_send_notification_success(self, mock_send_ping):
        sending_user = User()
        receiving_user = User()
        message = "Hello!"
        
        self.manager.send_notification(sending_user, receiving_user, message)
        mock_send_ping.assert_called_once_with(sending_user, receiving_user, message)

    @patch('src.Service_Layer.User')
    def test_add_user_success(self, MockUser):
        MockUser.return_value = None
        result = self.manager.add_user("John Doe", "Email", "1234567890", "johndoe@example.com", "Carrier")
        self.assertTrue(result)
        MockUser.assert_called_once_with("John Doe", "johndoe@example.com", "Carrier", "Email", "1234567890", False)

    @patch('src.Service_Layer.User')
    def test_add_user_failure(self, MockUser):
        MockUser.side_effect = Exception("Failed to create user")
        result = self.manager.add_user("John Doe", "Email", "1234567890", "johndoe@example.com", "Carrier")
        self.assertFalse(result)

    def test_remove_user_success(self):
        result = self.manager.remove_user("John Doe")
        self.assertTrue(result)

    def test_authenticate_log_in(self):
        result = self.manager.authenticate_log_in()
        self.assertFalse(result)

    def test_get_white_list_success(self):
        result = self.manager.get_white_list()
        self.assertTrue(result)

    def test_log_event(self):
        result = self.manager.log_event()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
