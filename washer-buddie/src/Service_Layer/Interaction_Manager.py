import Machine
import User
import Notification_Manager

class Interaction_Manager:
    def add_washer(self):
        """
        Adds a new washing machine

        Returns:
            boolean: whether or not the washer was added successfully
        """
        try:
            Machine('Washer')
            return True
        except:
            return False

    def add_dryer(self):
        """
        Adds a new drying machine

        Returns:
            boolean: whether or not the dryer was added successfully
        """
        try:
            Machine('Dryer')
            return True
        except:
            return False

    def send_notification(self, sending_user, receiving_user, message):
        """
        Sends a notification to another user from the current user

        Args:
            sending_user (User): user sending a message
            receiving_user (User): user receiving the message
            message (str): message being sent
        """
        Notification_Manager.send_ping(sending_user, receiving_user, message)

    def add_user(self, user_name, notification_preference, user_phone_number, user_email, phone_carrier, is_admin=False):
        try:
            User(user_name, user_email, phone_carrier, notification_preference, user_phone_number, is_admin)
            # put an addition request into CRUD
            # will add line in DB with user
            return True
        except:
            return False

    def remove_user(self, user_name):
        try:
            # put a delete request into CRUD to search by the user's name
            # will search up in DB and delete that line
            return True
        except:
            return False

    def authenticate_log_in(self):
        # send request to CRUD to validate that user's log in information
        # database will need to be decrypted
        return False

    def get_white_list(self):
        try:
            # put a request into CRUD to read all users
            # will search up all valid users in the DB to return
            return True
        except:
            return False

    def log_event(self):
        # log any events with their timestamps into our database
        return False
