import unittest
from src.Service_Layer.Notification import Notification
class TestNotification(unittest.TestCase):

    def setUp(self):
        self.notification = Notification()

    def test_get_text_notification(self):
        self.assertEqual(
            self.notification.get_text_notification("Washer"),
            "Your Washer cycle has finished. Please swap or pick up your laundry\n\nSincerely,\nWasherBuddie Team"
        )
        self.assertEqual(
            self.notification.get_text_notification("Dryer"),
            "Your Dryer cycle has finished. Please swap or pick up your laundry\n\nSincerely,\nWasherBuddie Team"
        )

    def test_get_email_notification(self):
        self.assertEqual(
            self.notification.get_email_notification("John Doe", "Washer"),
            "Hello John Doe,\n\nYour Washer cycle has finished. Please swap or pick up your laundry from the laundry room at your earliest convenience.\n\nSincerely,\nWasherBuddie Team"
        )
        self.assertEqual(
            self.notification.get_email_notification("Jane Smith", "Dryer"),
            "Hello Jane Smith,\n\nYour Dryer cycle has finished. Please swap or pick up your laundry from the laundry room at your earliest convenience.\n\nSincerely,\nWasherBuddie Team"
        )

    def test_get_follow_up_text_notification(self):
        self.assertEqual(
            self.notification.get_follow_up_text_notification("Washer"),
            "Your Washer cycle has been stagnant and other people would like to use this machine.\n\nPlease swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team"
        )
        self.assertEqual(
            self.notification.get_follow_up_text_notification("Dryer"),
            "Your Dryer cycle has been stagnant and other people would like to use this machine.\n\nPlease swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team"
        )

    def test_get_follow_up_email_notification(self):
        self.assertEqual(
            self.notification.get_follow_up_email_notification("John Doe", "Washer"),
            "Hello John Doe,\n\nYour Washer cycle has been stagnant and other people would like to use this machine. Please swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team"
        )
        self.assertEqual(
            self.notification.get_follow_up_email_notification("Jane Smith", "Dryer"),
            "Hello Jane Smith,\n\nYour Dryer cycle has been stagnant and other people would like to use this machine. Please swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team"
        )

if __name__ == '__main__':
    unittest.main()