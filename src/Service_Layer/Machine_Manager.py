from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
import time
from src.Service_Layer.Machine import Machine
from src.Service_Layer.User import User
from src.Service_Layer.Notification_Manager import Notification_Manager

# if TYPE_CHECKING:
    
class Machine_Manager:
	"""
	Class that manages the machines and their status
	"""
 
	def create_session(self, machine: Machine, user: User) -> bool:
		"""
		Sets the status for a machine to 'In Use' and associates the user with the machine

		Args:
			machine (Machine): machine the user is using
			user (User): specific user using the machine

		Raises:
			TypeError: if the parameters are not of type Machine or User

		Returns:
			None: if the machine is successfully set to 'In Use'
		"""
		if not isinstance(machine, Machine) and not isinstance(user, User):
			raise TypeError()
		
		machine.current_state = ("In Use", user)
  
		now = datetime.datetime.now()
  
		target_datetime = machine.end_time
  
		time_to_wait = (target_datetime - now).total_seconds()
		if time_to_wait > 0:
			time.sleep(time_to_wait)
   
		Machine_Manager.end_session(self, machine, user)
		Machine_Manager.notify_user(self, machine, user)
  
		return True
		
	def end_session(self, machine: Machine, user: User) -> bool:
		"""
		Sets the status for a machine to 'Available' and removes the user from the machine

		Args:
			machine (Machine): machine the user is using
			user (User): user using the machine
   
		Raises:
			TypeError: if the parameters are not of type Machine or User

		Returns:
			None: if the machine is successfully set to 'Available'
		"""
		if not (isinstance(machine, Machine) and isinstance(user, User)):
			raise TypeError()

		machine.current_state = ('Available', user)
		return True
		
	def set_out_of_order(self, machine: Machine, status: str, user: User) -> bool:
		"""
		Sets the status of the machine to/from out of order

		Args:
			machine (Machine): machine to have its status changed
			status (str): new status of the machine
			user (User): user setting the status of the machine
   
		Raises:
			TypeError: if the parameters are not of type Machine or User
			PermissionError: if the user is not an admin
		"""
		if not (isinstance(machine, Machine) and isinstance(user, User) and isinstance(status, str)):
			raise TypeError()

		if not user.is_admin:
			raise PermissionError()

		machine.current_state = (status, user)
		return True

	def get_status(self, machine: Machine) -> str:
		"""
		Returns the current status of the machine

		Args:
			machine (Machine): machine to get the status of

		Returns:
			str: the current status of the machine

		Raises:
			TypeError: if the parameter is not of type Machine
		"""
		if not isinstance(machine, Machine):
			raise TypeError()

		return machine._current_state
	
	def notify_user(self, machine: Machine, user: User) -> bool:
		"""
		Notifies the user of the machine's completion

		Args:
			machine (Machine): machine to notify the user of
			user (User): user to notify

		Raises:
			TypeError: if the parameters are not of type Machine or User
		"""
		if not (isinstance(machine, Machine) and isinstance(user, User)):
			raise TypeError()

		Notification_Manager.send_user_notification(Notification_Manager(), user, machine)
		return True