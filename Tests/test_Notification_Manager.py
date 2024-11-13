import unittest
import pytest
from unittest.mock import MagicMock, patch
from Service_Layer.Notification_Manager import Notification_Manager
from Service_Layer.User import User
from Service_Layer.Machine import Machine
from Service_Layer.Notification_Sender import Notification_Sender

class TestNotificationManager(unittest.TestCase):

    def setUp(self):
        self.manager = Notification_Manager()
        self.admin_user = User("Jaydon Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329, True)
        self.non_admin_user = User("Steve Faal", "jaydonfaal@gmail.com", "Verizon", "Email", 6269935329,False)
        self.user1 = User("James Faal", "jaydonfaal@gmail.com", "Verizon", "Text", 6269935329, False)
        self.user2 = User("William Faal", "jaydonfaal@gmail.com", "Verizon", "Text", 6269935329, False)
        self.machine = Machine('Dryer')
        self.notifier = Notification_Sender.Notification_Sender()


    def test_send_notification_success(self):
        users = [self.user1, self.user2]
        message = "Your laundry is ready!"

        #Sending a notification without admin access
        with pytest.raises(PermissionError):
            assert self.manager.send_notification(users, self.user2, message)
        #Sending a notification with admin access
        assert self.manager.send_notification(users, self.admin_user, message) == True


    def test_send_notification_type_error_sender(self):
        with self.assertRaises(TypeError):
            self.manager.send_notification([self.user1], "NotAUser", "Message")

    def test_send_notification_type_error_message(self):
        with self.assertRaises(TypeError):
            self.manager.send_notification([self.user1], self.admin_user, 123)

    def test_send_notification_permission_error(self):
        with self.assertRaises(PermissionError):
            self.manager.send_notification([self.user1], self.non_admin_user, "Message")

    def test_send_user_notification_success_text(self):
        self.user1.notification_preference = 'Text'

        self.manager.send_user_notification(self.user1, self.machine) 


    def test_send_user_notification_success_email(self):
        self.non_admin_user.notification_preference = 'Email'
        
        self.manager.send_user_notification(self.non_admin_user, self.machine)

        # with patch('Notification_Sender.send_email_notification') as mock_send:
        #     self.manager.send_user_notification(self.user1, self.machine)
        #     mock_send.assert_called_once_with(self.user1, self.machine)

    def test_send_user_notification_type_error_user(self):
        with self.assertRaises(TypeError):
            self.manager.send_user_notification("NotAUser", self.machine)

    def test_send_user_notification_type_error_machine(self):
        with self.assertRaises(TypeError):
            self.manager.send_user_notification(self.user1, "NotAMachine")

    def test_send_follow_up_notification_success_text(self):
        self.user1.notification_preference = 'Text'
        
        self.manager.send_follow_up_notification(self.user1, self.machine)

        # with patch('Notification_Sender.send_follow_up_text_notification') as mock_send:
        #     self.manager.send_follow_up_notification(self.user1, self.machine)
        #     mock_send.assert_called_once_with(self.user1, self.machine)

    def test_send_follow_up_notification_success_email(self):
        self.non_admin_user.notification_preference = 'Email'
        
        self.manager.send_follow_up_notification(self.non_admin_user, self.machine)


        # with patch('Notification_Sender.send_follow_up_email_notification') as mock_send:
        #     self.manager.send_follow_up_notification(self.user1, self.machine)
        #     mock_send.assert_called_once_with(self.user1, self.machine)

    def test_send_follow_up_notification_type_error_user(self):
        with self.assertRaises(TypeError):
            self.manager.send_follow_up_notification("NotAUser", self.machine)

    def test_send_follow_up_notification_type_error_machine(self):
        with self.assertRaises(TypeError):
            self.manager.send_follow_up_notification(self.user1, "NotAMachine")

    def test_send_ping_success(self):
        message = "Hello!"
        
        self.manager.send_ping(self.user1, self.user2, message)

    #     with patch('Notification_Sender.send_custom_message') as mock_send:
    #         self.manager.send_ping(self.admin_user, self.user1, message)
    #         mock_send.assert_called_once_with(self.admin_user, self.user1, message)

    def test_send_ping_type_error_sending_user(self):
        with self.assertRaises(TypeError):
            self.manager.send_ping("NotAUser", self.user1, "Message")

    def test_send_ping_type_error_receiving_user(self):
        with self.assertRaises(TypeError):
            self.manager.send_ping(self.admin_user, "NotAUser", "Message")

    def test_send_ping_type_error_message(self):
        with self.assertRaises(TypeError):
            self.manager.send_ping(self.admin_user, self.user1, 123)

if __name__ == '__main__':
    unittest.main()
