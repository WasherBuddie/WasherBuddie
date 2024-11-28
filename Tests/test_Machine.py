
import unittest
from datetime import datetime, timedelta
from src.Service_Layer.Machine import Machine
from src.Service_Layer.User import User  



class TestMachine(unittest.TestCase):

    def setUp(self):
        """Create a Machine instance, admin, and user before each test."""
        self.user = User("Steve Wozniak", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329, True)
        self.user2 =  User("Steve Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329, False)
        self.washer = Machine("Washer", 101)
        self.dryer = Machine("Dryer", 111)


    def test_initial_state(self):
        """Test the initial state of the machine."""
        self.assertEqual(self.washer.current_state, "Available")
        self.assertEqual(self.dryer.current_state, "Available")

    def test_invalid_machine_type(self):
        """Test creating a Machine with an invalid type."""
        with self.assertRaises(ValueError):
            Machine("Oven", 000)

    def test_set_state_in_use(self):
        """Test setting the machine state to 'In Use'."""
        self.washer.current_state = ("In Use", self.user2) 
        self.assertEqual(self.washer.current_state, "In Use")
        self.assertIsNotNone(self.washer.start_time)
        self.assertIsNotNone(self.washer.end_time)


    def test_set_state_available(self):
        """Test setting the machine state back to 'Available'."""
        self.washer.current_state = ("In Use", self.user)
        self.washer.current_state = ("Available", self.user)
        self.assertEqual(self.washer.current_state, "Available")
        self.assertIsNone(self.washer.start_time)
        self.assertIsNone(self.washer.end_time)

    def test_set_state_out_of_order_as_admin(self):
        """Test an admin can set the machine to 'Out of Order'."""
        self.washer.current_state = ("Out of Order", self.user)
        self.assertEqual(self.washer.current_state, "Out of Order")

    def test_set_state_out_of_order_as_user(self):
        """Test a regular user cannot set the machine to 'Out of Order'."""
        with self.assertRaises(ValueError):
            self.washer.current_state = ("Out of Order", self.user2)

    def test_invalid_user_type(self):
        """Test setting state with an invalid user type."""
        with self.assertRaises(TypeError):
            self.washer.current_state = ("In Use", "Not a User")

    def test_start_time_is_set_correctly(self):
        """Test the start time is set correctly when machine is in use."""
        self.washer.current_state = ("In Use", self.user)
        self.assertAlmostEqual(self.washer.start_time, datetime.now(), delta=timedelta(seconds=5))

if __name__ == "__main__":
    unittest.main()
