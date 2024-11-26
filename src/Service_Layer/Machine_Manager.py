from Service_Layer.Machine import Machine
from Service_Layer.User import User
import datetime
import time
from Service_Layer.Notification_Manager import Notification_Manager
from mongoDB.CRUD_api import *

class Machine_Manager:
	"""
	Class that manages the machines and their status
	"""
 
	def create_session(self, machine, user):
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
		if type(machine) != Machine or type(user) != User:
			raise TypeError()
		
		machine.current_state = ("In Use", user)
		change_machine_state(machine.machine_id, "In Use")
		change_machine_user(machine.machine_id, user.user_name)
  
		now = datetime.datetime.now()
		change_machine_start_time(machine.machine_id, now)
  
		target_datetime = machine.end_time
		change_machine_end_time(machine.machine_id, target_datetime)
  
		time_to_wait = (target_datetime - now).total_seconds()
		if time_to_wait > 0:
			time.sleep(time_to_wait)
   
		Machine_Manager.end_session(self, machine, user)
		Machine_Manager.notify_user(self, machine, user)
  
		return True
		
	def end_session(self, machine, user):
		"""
		Sets the status for a machine to 'Available' and removes the user from the machine

		Args:
			machine (Machine): machine the user is using
			user (User): user using the machine
			machine_id (int): id of the machine

		Raises:
			TypeError: if the parameters are not of type Machine or User

		Returns:
			None: if the machine is successfully set to 'Available'
		"""
		if not (isinstance(machine, Machine) and isinstance(user, User)):
			raise TypeError()

		machine.current_state = ('Available', user)
		change_machine_state(machine.machine_id, "Available")
		change_machine_user(machine.machine_id, None)
		return True
		
	def set_out_of_order(self, machine, status, user):
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
		change_machine_state(machine.machine_id, status)
		return True

	def get_status(self, machine):
		"""
		Returns the current status of the machine

		Args:
			machine (Machine): machine to get the status of

		Returns:
			str: the current status of the machine

		Raises:
			TypeError: if the parameter is not of type Machine
		"""
		if type(machine) != Machine:
			raise TypeError()

		return machine._current_state
	
	def notify_user(self, machine, user):
		"""
		Notifies the user of the machine's completion

		Args:
			machine (Machine): machine to notify the user of
			user (User): user to notify

		Raises:
			TypeError: if the parameters are not of type Machine or User
		"""
		if type(machine) != Machine or type(user) != User:
			raise TypeError()

		Notification_Manager.send_user_notification(Notification_Manager(), user, machine)
		return True