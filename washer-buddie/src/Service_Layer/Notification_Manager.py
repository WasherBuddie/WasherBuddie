from User import User
from Notification_Sender import Notification_Sender
from Machine import Machine

class Notification_Manager:
    """
    Class that manages the sending of notifications by calling the Notification_Sender class
    """
    
    def send_notification(self, users, sender, message):
        """
        Sends a custom message to every user of the application from an administrative user

        Args:
            users (List): list of Users that use the application
            sender (User): user with admin rights
            message (str): message for all users

        Raises:
            TypeError: if parameters or users are not the correct types
            PermissionError: sender doesn't have the right permissions to send a message to all users
        """

        
        if not isinstance(sender, User) or type(message) != str:
            raise TypeError()
        
        if not sender.is_admin:
            raise PermissionError()
        
        for user in users:
            if type(user) != User:
                raise TypeError()
            Notification_Sender.send_custom_message = (sender, user, message)
        return True
        
    def send_user_notification(self, user, machine):
        """
        Sends a notification to a specific user (i.e. when a person’s laundry finishes)

        Args:
            user (User): user using machine
            machine (Machine): machine being used

        Raises:
            TypeError: if the parameters are not the correct type
            Exception: if the user has an invalid notification preference
        """
        if not isinstance(user, User)  or not isinstance(machine, Machine):
            raise TypeError()
        
        if user.notification_preference == 'Text':
            Notification_Sender.send_text_notification(self=Notification_Sender(), user=user, machine=machine)
        elif user.notification_preference == 'Email':
            Notification_Sender.send_email_notification(self=Notification_Sender(), user=user, machine=machine)
        else:
            raise Exception()
        
    def send_follow_up_notification(self, user, machine):
        """
        Sends a follow-up notification to a user after a machine has been used for a long time

        Args:
            user (User): user using machine
            machine (Machine): machine being used

        Raises:
            TypeError: if the parameters are not the correct type
            Exception: if the user has an invalid notification preference
        """
        if type(user) != User or type(machine) != Machine:
            raise TypeError()
        
        if user.notification_preference == 'Text':
            Notification_Sender.send_follow_up_text_notification(Notification_Sender(), user, machine)
        elif user.notification_preference == 'Email':
            Notification_Sender.send_follow_up_email_notification(Notification_Sender(), user, machine)
        else:
            raise Exception()
    
    def send_ping(self, sending_user, receiving_user, message):
        """
        Sends a custom message to a specific user from another user

        Args:
            sending_user (User): user sending a message
            receiving_user (User): user receiving the message using a machine
            message (str): custom message from the user

        Raises:
            TypeError: if the parameters are not the correct type
        """
        if type(sending_user) != User or type(receiving_user) != User or type(message) != str:
            raise TypeError()

        Notification_Sender.send_custom_message(Notification_Sender(), sending_user, receiving_user, message)
    
    def log_event(self, user_event):
        # log any events with their timestamps into our database
        pass