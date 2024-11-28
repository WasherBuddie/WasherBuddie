from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from mongoDB.CRUD_api import Database_Manager
    from src.Service_Layer.Machine import Machine
    from src.Service_Layer.User import User
    from src.Service_Layer.Notification_Manager import Notification_Manager

class Interaction_Manager:
    def add_washer(self, machine_id: int) -> bool:
        """
        Adds a new washing machine
        
        Args:
            machine_id (int): machine id of the new washer

        Returns:
            boolean: whether or not the washer was added successfully
        """
        try:
            Machine('Washer', machine_id)
            return True
        except:
            return False

    def add_dryer(self, machine_id: int) -> bool:
        """
        Adds a new drying machine
        
        Args:
            machine_id (int): machine id of the new dryer

        Returns:
            boolean: whether or not the dryer was added successfully
        """
        try:
            return Database_Manager().insert_dryer(Machine('Dryer', machine_id))
        except:
            return False

    def send_notification(self, sending_user: User, receiving_user: User, message: str):
        """
        Sends a notification to another user from the current user

        Args:
            sending_user (User): user sending a message
            receiving_user (User): user receiving the message
            message (str): message being sent
        """
        Notification_Manager.send_ping(sending_user, receiving_user, message)

    def add_user(self, user_name: str, notification_preference: str, user_phone_number: int, user_email: str, phone_carrier: str, is_admin:Optional[bool]=False, password:Optional[str]='defaultpassword123') -> bool:
        """
        Adds a user to the database

        Args:
            user_name (str): user's name
            notification_preference (str): user's notification preferences
            user_phone_number (int): user's 10-digit phone number
            user_email (str): user's valid email
            phone_carrier (str): user's phone carrier
            is_admin (bool, optional): whether the user is an admin of the program. Defaults to False.
            password (str, optional): user's password. Defaults to 'defaultpassword123'.

        Returns:
            _type_: _description_
        """
        try:
            return Database_Manager().insert_single_user(User(user_name, user_email, phone_carrier, notification_preference, user_phone_number, is_admin, password))
        except:
            return False

    def remove_user(self, user_name: str) -> bool:
        """
        Removes a user from the database

        Args:
            user_name (str): user's namee to be deleted from whitelist

        Returns:
            boolean: True if the user was removed successfully, False otherwise
        """
        try:
            return Database_Manager().delete_single_user(user_name)
        except:
            return False

    def authenticate_log_in(self, email_address: str, password: str) -> bool:
        """
        Authenticates a user's log in using their email and password

        Args:
            email_address (str): user's email address
            password (str): user's password input

        Returns:
            boolean: True if the user is authenticated, False otherwise
        """
        try:
            return Database_Manager().validate_user(email_address, password)
        except:
            return False

    def get_white_list(self):
        """
        Returns a list of all valid users

        Returns:
            list: list of all valid users as Users, False otherwise
        """
        try:
            return Database_Manager().get_valid_users()
        except:
            return False