import smtplib
from email.mime.text import MIMEText
from src.Service_Layer.User import User
from src.Service_Layer.Notification import Notification
from src.Service_Layer.Machine import Machine

class Notification_Sender:
	
	_mobile_carriers = 	{'AT&T': '@mms.att.net',
	 					'Verizon': '@vzwpix.com', 
						'Boost Mobile': '@myboostmobile.com', 
					 	'Cricket': '@mms.mycricket.com', 
					  	'MetroPCS': '@mymetropcs.com',
					   	'Sprint': '@pm.sprint.com',
						'T-Mobile': '@tmomail.net',
						'U.S. Cellular': '@mms.uscc.net',
						}
 
	_password = 'smbd ipal qysl zxxw'
	
	@property
	def mobile_carriers(self):
		"""
		Returns a list of mobile carriers and their gateway addresses

		Returns:
			dict: list of mobile carriers and their gateway addresses
		"""
		return self._mobile_carriers

	@property
	def password(self):
		"""
		Returns the password for the email account

		Returns:
			str: password for the email account
		"""
		return self._password

	def	send_text_notification(self, user, machine):
		"""
		Sends a text notification to the user's phone number

		Args:
			user (User): user using the machine
			machine (Machine): machine being used

		Raises:
			TypeError: if the parameters are not the correct types
		"""	
		if not isinstance(user, User)  or not isinstance(machine, Machine):
			raise TypeError()

		msg = MIMEText(Notification.get_text_notification(self=Notification(), machineType=machine.machine_type))
		msg['Subject'] = 'WasherBuddie - Your Laundry Cycle Has Finished'
		msg['From'] = 'WasherBuddie'
		msg['To'] = str(user.user_phone_number) + self.mobile_carriers[user.phone_carrier]

		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.starttls()
			smtp.login("washerbuddie@gmail.com", self.password)
			smtp.send_message(msg)
			smtp.quit()
   
	def send_email_notification(self, user, machine):
		"""
		Sends an email notification to the user's email address

		Args:
			user (User): user using the machine
			machine (Machine): machine being used

		Raises:
			TypeError: if the parameters are not the correct types
		"""	
		if type(user) != User or type(machine) != Machine:
			raise TypeError()

		msg = MIMEText(Notification.get_email_notification(Notification(), user.user_name, machine.machine_type))
		msg['Subject'] = 'WasherBuddie - Your Laundry Cycle Has Finished'
		msg['From'] = 'WasherBuddie'
		msg['To'] = user.user_email

		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.starttls()
			smtp.login("washerbuddie@gmail.com", self.password)
			smtp.send_message(msg)
			smtp.quit()
  
	def send_follow_up_text_notification(self, user, machine):
		"""
		Sends a follow-up text notification to the user's phone number

		Args:
			user (User): user using machine
			machine (Machine): machine being used

		Raises:
			TypeError: if the parameters are not the correct types
		"""	
		if type(user) != User or type(machine) != Machine:
			raise TypeError()

		msg = MIMEText(Notification.get_follow_up_text_notification(self=Notification(), machineType=machine.machine_type))
		msg['Subject'] = 'WasherBuddie - Your Laundry Cycle Has Been Stagnant'
		msg['From'] = 'WasherBuddie'
		msg['To'] = str(user.user_phone_number) + self.mobile_carriers[user.phone_carrier]
  
		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.starttls()
			smtp.login("washerbuddie@gmail.com", self.password)
			smtp.send_message(msg)
			smtp.quit()
   
	def send_follow_up_email_notification(self, user, machine):
		"""
		Sends a follow-up email notification to the user's email address

		Args:
			user (User): user using machine
			machine (Machine): machine being used

		Raises:
			TypeError: if the parameters are not the correct types
		"""
		if type(user) != User or type(machine) != Machine:
			raise TypeError()

		msg = MIMEText(Notification.get_follow_up_email_notification(Notification(), user.user_name, machine.machine_type))
		msg['Subject'] = 'WasherBuddie - Your Laundry Cycle Has Been Stagnant'
		msg['From'] = 'WasherBuddie'
		msg['To'] = user.user_email

		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.starttls()
			smtp.login("washerbuddie@gmail.com", self.password)
			smtp.send_message(msg)
			smtp.quit()
   
	def send_custom_message(self, sending_user, receiving_user, message):
		"""
		Sends a custom message to the receiving user using their preferred method of communication from another user

		Args:
			sending_user (User): user sending a message
			receiving_user (User): user using machine and receiving the message
			message (str): message contents

		Raises:
			TypeError: if the parameters are not the correct types
		"""
		if type(sending_user) != User or type(receiving_user) != User:
			raise TypeError()

		if receiving_user.notification_preference == 'Text':
			msg = MIMEText(message)
			msg['Subject'] = 'WasherBuddie - Message from ' + sending_user.user_name
			msg['From'] = sending_user.user_name
			msg['To'] = str(receiving_user.user_phone_number) + self.mobile_carriers[receiving_user.phone_carrier]
		elif receiving_user.notification_preference == 'Email':
			msg = MIMEText(message)
			msg['Subject'] = 'WasherBuddie - Message from ' + sending_user.user_name
			msg['From'] = sending_user.user_name
			msg['To'] = receiving_user.user_email

		with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
			smtp.starttls()
			smtp.login("washerbuddie@gmail.com", self.password)
			smtp.send_message(msg)
			smtp.quit()