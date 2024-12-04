from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Service_Layer.User import User
    from src.Service_Layer.Notification_Sender import Notification_Sender
    from src.Service_Layer.Machine import Machine

class Notification_Manager:
    """
    Class that manages the sending of notifications by calling the Notification_Sender class
    """
    
    def send_notification(self, users: list, sender: User, message: str) -> bool:
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
        from src.Service_Layer.User import User
        from src.Service_Layer.Notification_Sender import Notification_Sender
        
        if not isinstance(sender, User) or type(message) != str:
            raise TypeError()
        
        if not sender.is_admin:
            raise PermissionError()
        
        for user in users:
            if type(user) != User:
                raise TypeError()
            Notification_Sender().send_custom_message = (sender, user, message)
        return True
        
    def send_user_notification(self, user: User, machine: Machine):
        """
        Sends a notification to a specific user (i.e. when a person’s laundry finishes)

        Args:
            user (User): user using machine
            machine (Machine): machine being used

        Raises:
            TypeError: if the parameters are not the correct type
            Exception: if the user has an invalid notification preference
        """
        from src.Service_Layer.User import User
        from src.Service_Layer.Machine import Machine
        from src.Service_Layer.Notification_Sender import Notification_Sender
        
        if not isinstance(user, User)  or not isinstance(machine, Machine):
            raise TypeError()
        
        sender = Notification_Sender()
        
        if user.notification_preference == 'Text':
            sender.send_text_notification(user=user, machine=machine)
        elif user.notification_preference == 'Email':
            sender.send_email_notification(user=user, machine=machine)
        else:
            raise Exception()
        
    def send_follow_up_notification(self, user: User, machine: Machine):
        """
        Sends a follow-up notification to a user after a machine has been used for a long time

        Args:
            user (User): user using machine
            machine (Machine): machine being used

        Raises:
            TypeError: if the parameters are not the correct type
            Exception: if the user has an invalid notification preference
        """
        from src.Service_Layer.User import User
        from src.Service_Layer.Machine import Machine
        from src.Service_Layer.Notification_Sender import Notification_Sender
        
        if type(user) != User or type(machine) != Machine:
            raise TypeError()
        
        if user.notification_preference == 'Text':
            Notification_Sender().send_follow_up_text_notification(user, machine)
        elif user.notification_preference == 'Email':
            Notification_Sender().send_follow_up_email_notification(user, machine)
        else:
            raise Exception()
    
    def send_ping(self, sending_user: User, receiving_user: User, message: str):
        """
        Sends a custom message to a specific user from another user

        Args:
            sending_user (User): user sending a message
            receiving_user (User): user receiving the message using a machine
            message (str): custom message from the user

        Raises:
            TypeError: if the parameters are not the correct type
        """
        from src.Service_Layer.User import User
        from src.Service_Layer.Notification_Sender import Notification_Sender
        
        if type(sending_user) != User or type(receiving_user) != User or type(message) != str:
            raise TypeError()

        Notification_Sender().send_custom_message(sending_user, receiving_user, message)