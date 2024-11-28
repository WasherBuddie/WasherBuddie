import unittest
from unittest.mock import Mock, patch
from src.Service_Layer.Machine_Manager import Machine_Manager
from src.Service_Layer.Machine import Machine
from src.Service_Layer.User import User
import pytest

class TestMachineManager(unittest.TestCase):

	def setUp(self):
		self.manager = Machine_Manager()
		self.washer1 = Machine('Washer', 111)
		self.washer2 = Machine('Washer', 112)
		self.dryer1 = Machine('Dryer', 121)
		self.dryer2 = Machine('Dryer', 122)
		self.test_user = User('Nikhil Jindal', 'nxj224@case.edu', 'T-Mobile', 'Email', 9093309194, False)
		self.test_admin_user = User('Nikhil Jindal', 'nxj224@case.edu', 'T-Mobile', 'Email', 9093309194, True, 'newpswdt3st!ng')
		
	def test_create_session_and_end_session_success(self):
		# create a user session
		assert self.manager.create_session(self.washer1, self.test_user) == True
		assert self.washer1.current_state == 'Available'
		assert self.washer1.who_is_using == None
		assert self.washer1.end_time == None
		assert self.washer1.start_time == None

	def test_create_session_failure(self):
		# failure to pass a user object
		with pytest.raises(TypeError):
			self.manager.create_session(self.washer1, self.washer2)

	def test_end_session_failure(self):
		self.washer1._current_state = 'Available'
		with pytest.raises(ValueError, match="Invalid state transition"):
			self.manager.end_session(self.washer1, self.test_user)

	def test_set_out_of_order_success(self):
		assert self.manager.set_out_of_order(self.washer1, 'Out of Order', self.test_admin_user) == True

	def test_set_out_of_order_fail(self):
		with pytest.raises(PermissionError):
			self.manager.set_out_of_order(self.washer1, 'Out of Order', self.test_user)
   
	def test_get_status_success(self):
		self.washer1._current_state = 'Available'
		assert self.manager.get_status(self.washer1) == 'Available'
  
	def test_get_status_fail(self):
		with pytest.raises(TypeError):
			self.manager.get_status(self.test_admin_user)
   
	def test_notify_user_success(self):
		assert self.manager.notify_user(machine=self.washer1, user=self.test_user) == True

	def test_notify_user_fail(self):
		with pytest.raises(TypeError):
			self.manager.notify_user(machine=self.washer1, user=self.washer2)

if __name__ == '__main__':
	unittest.main()
