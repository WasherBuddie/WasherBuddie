from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import threading
import datetime
import time
import traceback

# if TYPE_CHECKING:
from mongoDB.CRUD_api import Database_Manager
from src.Service_Layer.Machine import Machine
from src.Service_Layer.User import User
from src.Service_Layer.Notification_Manager import Notification_Manager

class Interaction_Manager:
	machine_count = 0
	Machines = {}
	Users = {}
	white_list = []
	
	def add_washer(self) -> bool:
		"""
		Adds a new washing machine
		
		Args:
			machine_id (int): machine id of the new washer

		Returns:
			boolean: whether or not the washer was added successfully
		"""
		try:
			washer = Machine('Washer', self.machine_count)
			self.Machines[self.machine_count] = washer
			self.machine_count+=1
			return True
		except Exception as e:
			print(f"Error adding user: {e}")
			print(traceback.format_exc())  # Print the stack trace for debugging
			return False

	def add_dryer(self) -> bool:
		"""
		Adds a new drying machine
		
		Args:
			machine_id (int): machine id of the new dryer

		Returns:
			boolean: whether or not the dryer was added successfully
		"""
		try:
			dryer = Machine('Dryer', self.machine_count)
			self.Machines[self.machine_count] = dryer
			self.machine_count+=1
			return True
		except Exception as e:
			print(f"Error adding user: {e}")
			print(traceback.format_exc())  # Print the stack trace for debugging
			return False

	def send_notification(self, sending_user: User, receiving_user: User, message: str):
		"""
		Sends a notification to another user from the current user

		Args:
			sending_user (User): user sending a message
			receiving_user (User): user receiving the message
			message (str): message being sent
		"""
		Notification_Manager().send_ping(sending_user, receiving_user, message)

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
			boolean: True is user added successfully. False otherwise
		"""
		try:
			#need to check if the user already exists first
			if user_name in self.Users:
				print(f"User with {user_name} already exists.")
				return False
			
			user =  User(user_name, user_email, phone_carrier, notification_preference, user_phone_number, is_admin, password)
			self.Users[user_name] = user
			return Database_Manager().insert_single_user(User(user_name, user_email, phone_carrier, notification_preference, user_phone_number, is_admin, password))
		except Exception as e:
			print(f"Error adding user: {e}")
			print(traceback.format_exc())  # Print the stack trace for debugging
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
			if user_name not in self.Users:
				print(f"User with {user_name} does not exist.")
				return False
			
			del self.Users[user_name]
			return Database_Manager().delete_single_user(user_name)
		except Exception as e:
			print(f"Error adding user: {e}")
			print(traceback.format_exc())  # Print the stack trace for debugging
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
		except Exception as e:
			print(f"Error adding user: {e}")
			print(traceback.format_exc())  # Print the stack trace for debugging
			return False
		
#below needs to be integrated into the class, may keep local vars, my go into the db, then get rid of machine manager      
	
	def create_session(self, machine_id: int, user: User) -> bool:
		"""
		Sets the status for a machine to 'In Use' and associates the user with the machine

		Args:
			machine_id (int): machine id of the machine being used
			user (User): specific user using the machine

		Raises:
			TypeError: if the parameters are not of type Machine or User

		Returns:
			None: if the machine is successfully set to 'In Use'
		"""
		if not isinstance(machine_id, int) and not isinstance(user, User):
			raise TypeError()
		
		# machine = self.Machines[machine_id]
		machine = Database_Manager().find_machine_by_id(machine_id)
		machine.current_state = ('In Use', user)
  
		def monitor_session():
			now = datetime.datetime.now()

			target_datetime = machine.end_time

			time_to_wait = (target_datetime - now).total_seconds()
			if time_to_wait > 0:
				time.sleep(time_to_wait)
	
			self.end_session(machine_id, user)
			self.notify_user(machine_id, user)

		thread = threading.Thread(target=monitor_session, daemon=True)
		thread.start()
  
		return True
		
	def end_session(self, machine_id: int):
		"""
		Sets the status for a machine to 'Available' and removes the user from the machine

		Args:
			machine_id (int): machine the user is using
			user (User): user using the machine
   
		Raises:
			TypeError: if the parameters are not of type Machine or User

		Returns:
			None: if the machine is successfully set to 'Available'
		"""
		if not (isinstance(machine_id, int)):
			raise TypeError()

		# machine = self.Machines[machine_id]
		return Database_Manager().change_machine_end_time(machine_id, None)
	
	def set_out_of_order(self, machine_id: int, user: User) -> bool:
		"""
		Sets the status of the machine to/from out of order

		Args:
			machine_id (int): machine to have its status changed
			user (User): user setting the status of the machine
   
		Raises:
			TypeError: if the parameters are not of type Machine or User
			PermissionError: if the user is not an admin
		"""
		if not (isinstance(machine_id, int) and isinstance(user, User)):
			raise TypeError()

		if not user.is_admin:
			raise PermissionError()

		# machine = self.Machines[machine_id]
		machine = Database_Manager().find_machine_by_id(machine_id)
  
		machine.current_state = ('Out of Order', user)
		return True

	def return_to_service(self, machine_id: int, user: User) -> bool:
		"""
		Sets the status of the machine to/from out of order

		Args:
			machine_id (int): machine to have its status changed
			user (User): user setting the status of the machine
   
		Raises:
			TypeError: if the parameters are not of type Machine or User
			PermissionError: if the user is not an admin
		"""
		if not (isinstance(machine_id, int) and isinstance(user, User)):
			raise TypeError()

		if not user.is_admin:
			raise PermissionError()

		# machine = self.Machines[machine_id]
		machine = Database_Manager().find_machine_by_id(machine_id)
  
		machine.current_state = ('return', user)
		return True


	def get_status(self, machine_id: int) -> str:
		"""
		Returns the current status of the machine

		Args:
			machine_id (int): machine to get the status of

		Returns:
			str: the current status of the machine

		Raises:
			TypeError: if the parameter is not of type Machine
		"""
		if not isinstance(machine_id, int):
			raise TypeError()

		# machine = self.Machines[machine_id]
		machine = Database_Manager().find_machine_by_id(machine_id)

		return machine._current_state
	
	def notify_user(self, machine_id: int, user: User) -> bool:
		"""
		Notifies the user of the machine's completion

		Args:
			machine_id (int): machine to notify the user of
			user (User): user to notify

		Raises:
			TypeError: if the parameters are not of type Machine or User
		"""
		if not (isinstance(machine_id, int) and isinstance(user, User)):
			raise TypeError()

		# machine = self.Machines[machine_id]
		machine = Database_Manager().find_machine_by_id(machine_id)

		Notification_Manager().send_user_notification(user, machine)
		return True
		

	
	def user_update(self, user_name, code, value):
		return Database_Manager().user_update(user_name, code, value)		

	def get_user(self, email):
		return Database_Manager().find_user_by_email(email)