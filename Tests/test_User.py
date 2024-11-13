import pytest
import unittest
from src.Service_Layer.User import User

class TestUser(unittest.TestCase):

    def test_user_initialization(self):
        # Test with valid input
        user = User("Jaydon Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329, True)
        assert user.is_admin == True
        assert user.user_name == "Jaydon Faal"
        assert user.user_email == "jaydonfaal@gmail.com"
        assert user.phone_carrier == "Verizon"
        assert user.user_phone_number == 6269935329

    def test_user_invalid_name(self):
        # Test invalid name without first and last
        with pytest.raises(ValueError, match="No username was provided"):
            User("Jaydon", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329)

    def test_user_invalid_email(self):
        # Test invalid email format
        with pytest.raises(ValueError, match="Invalid email address was given"):
            User("Jaydon Faal", "invalidemail", "Verizon", "Email", 626935329)

    def test_user_phone_number_setterself(self):
        user = User("Jaydon Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329)

        # Valid phone number
        user.user_phone_number = 1234567890
        assert user.user_phone_number == 1234567890

        # Invalid phone number (too short)
        with pytest.raises(ValueError, match="Invalid phone number was given"):
            user.user_phone_number = 123 

        # Invalid phone number (too long)
        with pytest.raises(ValueError, match="Invalid phone number was given"):
            user.user_phone_number = 123456789012345  



    def test_user_invalid_notification_preference(self):
        # Test invalid notification preference
        with pytest.raises(ValueError, match="Invalid communication preference was provided"):
            User("Jaydon Faal", "jaydonfaal@gmail.com", "Verizon", "InvalidPreference", 6269935329)

    def test_user_setters(self):
        user = User("Jaydon Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329, True)
        # Test name setter
        user.user_name = "New Name"
        assert user.user_name == "New Name"
        
        # Test email setter with valid email
        user.user_email = "newemail@example.com"
        assert user.user_email == "newemail@example.com"

        # Test invalid email setter
        with pytest.raises(ValueError, match="Invalid email address was given"):
            user.user_email = "invalid-email"

        # Test phone number setter with valid number
        user.user_phone_number = 1234567890
        assert user.user_phone_number == 1234567890

        # Test invalid phone number setter
        with pytest.raises(ValueError, match="Invalid phone number was given"):
            user.user_phone_number = 123  

        # Test notification preference setter with valid input
        user.notification_preference = "Text"
        assert user.notification_preference == "Text"

        # Test invalid notification preference setter
        with pytest.raises(ValueError, match="Invalid communication method was provided"):
            user.notification_preference = "InvalidPreference"

if __name__ == '__main__':
    unittest.main() 