import unittest
from unittest.mock import Mock, patch
from src.Service_Layer.Interaction_Manager import Interaction_Manager
from src.Service_Layer.User import User
from src.Service_Layer.Machine import Machine
from mongoDB.CRUD_api import Database_Manager

class TestInteractionManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.interaction_manager = Interaction_Manager()
        self.test_user = User(
            user_name="Nikhil Jindal",
            user_email="nxj224@case.edu",
            phone_carrier="T-Mobile",
            notification_preference="Text",
            user_phone_number=9093309194,
            is_admin=False,
            password="testpassword123"
        )

    def tearDown(self):
        """Clean up after each test method."""
        self.interaction_manager.Machines.clear()
        self.interaction_manager.Users.clear()
        self.interaction_manager.machine_count = 0

    def test_add_washer(self):
        """Test adding a washer."""
        result = self.interaction_manager.add_washer()
        self.assertTrue(result)
        self.assertEqual(len(self.interaction_manager.Machines), 1)
        self.assertEqual(self.interaction_manager.Machines[0].machine_type, 'Washer')

    def test_add_dryer(self):
        """Test adding a dryer."""
        result = self.interaction_manager.add_dryer()
        self.assertTrue(result)
        self.assertEqual(len(self.interaction_manager.Machines), 1)
        self.assertEqual(self.interaction_manager.Machines[0].machine_type, 'Dryer')

    @patch('src.Service_Layer.Notification_Manager.Notification_Manager.send_ping')
    def test_send_notification(self, mock_send_ping):
        """Test sending notification between users."""
        receiving_user = User(
            "Jaydon Faal",
            "jaydonfaal@gmail.com",
            "Verizon",
            "Text",
            6269935329,
            False,
            "password123"
        )
        
        self.interaction_manager.send_notification(
            self.test_user,
            receiving_user,
            "Test message"
        )
        mock_send_ping.assert_called_once()

    @patch('mongoDB.CRUD_api.Database_Manager.insert_single_user')
    def test_add_user(self, mock_insert_user):
        """Test adding a user."""
        mock_insert_user.return_value = True
        result = self.interaction_manager.add_user(
            user_name="Nikhil Jindal",
            user_email="nxj224@case.edu",
            phone_carrier="T-Mobile",
            notification_preference="Text",
            user_phone_number=9093309194,
            is_admin=False,
            password="testpassword123"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.interaction_manager.Users), 1)

    def test_add_duplicate_user(self):
        """Test adding a duplicate user."""
        self.interaction_manager.Users["test_user"] = self.test_user
        result = self.interaction_manager.add_user(
            "test_user",
            "email",
            1234567890,
            "test@example.com",
            "Verizon"
        )
        self.assertFalse(result)

    @patch('mongoDB.CRUD_api.Database_Manager.delete_single_user')
    def test_remove_user(self, mock_delete_user):
        """Test removing a user."""
        mock_delete_user.return_value = True
        self.interaction_manager.Users["test_user"] = self.test_user
        result = self.interaction_manager.remove_user("test_user")
        self.assertTrue(result)
        self.assertEqual(len(self.interaction_manager.Users), 0)

    def test_remove_nonexistent_user(self):
        """Test removing a user that doesn't exist."""
        result = self.interaction_manager.remove_user("nonexistent_user")
        self.assertFalse(result)

    @patch('mongoDB.CRUD_api.Database_Manager.validate_user')
    def test_authenticate_log_in(self, mock_validate):
        """Test user authentication."""
        mock_validate.return_value = True
        result = self.interaction_manager.authenticate_log_in(
            "test@example.com",
            "testpassword123"
        )
        self.assertTrue(result)

    @patch('mongoDB.CRUD_api.Database_Manager.find_machine_by_id')
    def test_create_session(self, mock_find_machine):
        """Test creating a machine session."""
        mock_machine = Machine('Washer', 0)
        mock_find_machine.return_value = mock_machine
        
        result = self.interaction_manager.create_session(0, self.test_user)
        self.assertTrue(result)
        self.assertEqual(mock_machine.current_state, "In Use")

    def test_create_session_invalid_input(self):
        """Test creating a session with invalid input."""
        with self.assertRaises(TypeError):
            self.interaction_manager.create_session("invalid", "invalid")

    @patch('mongoDB.CRUD_api.Database_Manager.find_machine_by_id')
    def test_get_status(self, mock_find_machine):
        """Test getting machine status."""
        mock_machine = Machine('Washer', 0)
        mock_find_machine.return_value = mock_machine
        
        status = self.interaction_manager.get_status(0)
        self.assertEqual(status, "Available")

if __name__ == '__main__':
    unittest.main()
