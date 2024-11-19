from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
from Service_Layer.Machine_Manager import Machine_Manager
from Service_Layer.Machine import Machine
from Service_Layer.User import User
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://WasherBuddie:{password}@washerbuddie.2izth.mongodb.net/?retryWrites=true&w=majority&appName=WasherBuddie"
client = MongoClient(connection_string)

dbs = client.list_database_names()
washerbuddie_db = client.WasherBuddie
collections = washerbuddie_db.list_collection_names()

def insert_single_user(self, user):
	"""
	Inserts a single user into the database

	Args:
		user (User): user to be added to whitelist

	Raises:
		TypeError: if user is not an instance of the User class

	Returns:
		str: inserted_id of the field
	"""
 
	if not isinstance(user, User):
		raise TypeError("Input must be an instance of the User class")
	
	collection = washerbuddie_db.Users
	inserted_id = collection.insert_one(user.__dict__).inserted_id
	return inserted_id

def insert_multiple_users(self, users):
	"""
	Inserts multiple users into the database at once

	Args:
		users (User): list of users to be added to whitelist

	Raises:
		TypeError: if user is not an instance of the User class

	Returns:
		str: inserted_id of the field
	"""

	if not all(isinstance(user, User) for user in users):
		raise TypeError("All elements in the list must be instances of the User class")
	
	to_add = []
	for user in users:
		to_add.append(user.__dict__)
	
	collection = washerbuddie_db.Users
	inserted_ids = collection.insert_many(to_add).inserted_ids
	return inserted_ids

def insert_washer(self, washer):
	"""
    Inserts a single washer into the database

	Args:
		washer (Machine): washing machine to be added to inventory

	Raises:
		TypeError: raises error if washer is not an instance of the Machine class

	Returns:
		str: inserted_id of the field
	"""
	if not isinstance(washer, Machine):
		raise TypeError("Input must be an instance of the Machine class")

	collection = washerbuddie_db.Machines
	inserted_id = collection.insert_one(washer.__dict__).inserted_id
	return inserted_id

def insert_dryer(self, dryer):
	"""
	Adds a single dryer to the database

	Args:
		dryer (Machine): drying machine to be added to inventory

	Raises:
		TypeError: if dryer is not an instance of the Machine class

	Returns:
		str: inserted_id of the field
	"""
	if not isinstance(dryer, Machine):
		raise TypeError("Input must be an instance of the Machine class")

	collection = washerbuddie_db.Machines
	inserted_id = collection.insert_one(dryer.__dict__).inserted_id
	return inserted_id

def delete_single_user(self, user):
	"""
	Deletes a single user from the database

	Args:
		user (User): user to be deleted from whitelist

	Raises:
		TypeError: if user is not an instance of the User class

	Returns:
		str: deleted_count of the field
	"""
	if not isinstance(user, User):
		raise TypeError("Input must be an instance of the User class")

	collection = washerbuddie_db.Users
	collection.delete_one({"_user_name": user.user_name})

def delete_multiple_users(self, users):
	"""
	Deletes multiple users from the database at once

	Args:
		users (User): list of users to be deleted from whitelist

	Raises:
		TypeError: if user is not an instance of the User class

	Returns:
		str: deleted_count of the field
	"""
	if not all(isinstance(user, User) for user in users):
		raise TypeError("All elements in the list must be instances of the User class")

	collection = washerbuddie_db.Users
	deleted_count = collection.delete_many({"_user_name": {"$in": [user.user_name for user in users]}}).deleted_count
	return deleted_count

def get_valid_users(self):
	"""
	Retrieves all valid users from the database

	Returns:
		list: list of valid users
	"""
	collection = washerbuddie_db.Users
	valid_users = []
	for user in collection.find():
		valid_users.append(User(user['_user_name'], user['_user_email'], user['_phone_carrier'], user['_notification_preference'], user['_user_phone_number'], user['_is_admin']))
	return valid_users

def update_user(self, old_user, new_user):
	"""
	Updates a single user in the database

	Args:
		old_user (User): user to be updated
		new_user (User): user to be updated to

	Raises:
		TypeError: if user is not an instance of the User class

	Returns:
		str: modified_count of the field
	"""
	if not isinstance(old_user, User) and isinstance(new_user, User):
		raise TypeError("Input must be an instance of the User class")
 
	collection = washerbuddie_db.Users
	collection.find_one_and_replace({"_user_name": old_user.user_name}, new_user.__dict__)
	# collection.replace_one({"_user_name": old_user.user_name}, new_user.__dict__)

def find_user_by_id(self, user_id):
	"""
	Finds a user by their ID

	Args:
		user_id (str): ID of the user to be found

	Returns:
		User: user with the given ID
	"""
	collection = washerbuddie_db.Users
	user = collection.find_one({"_id": user_id})
	return User(user['_user_name'], user['_user_email'], user['_phone_carrier'], user['_notification_preference'], user['_user_phone_number'], user['_is_admin'])

# ----------------------------------------

# Testing

manager = Machine_Manager()
washer1 = Machine('Washer')
washer2 = Machine('Washer')
dryer1 = Machine('Dryer')
dryer2 = Machine('Dryer')
test_user = User('Nikhil Jindal', 'nxj224@case.edu', 'T-Mobile', 'Email', 9093309194, False)
test_admin_user = User('Jaydon Faal', 'nxj224@case.edu', 'T-Mobile', 'Email', 9093309194, True)
test_secondary_user = User('Jake Model', 'nxj224@case.edu', 'T-Mobile', 'Email', 9093309194, False)
replacement_user = User('Nikhil Jindal', 'njindal2004@gmail.com', 'Verizon', 'Email', 9095559195, False)

test_user_id = insert_single_user(washerbuddie_db, test_user)
print("Adding single user:")
pprint.pprint(find_user_by_id(washerbuddie_db, test_user_id).__dict__)

insert_multiple_users(washerbuddie_db, [test_admin_user, test_secondary_user])
all_users = get_valid_users(washerbuddie_db)
print("\nAll users after adding two more: ")
for user in all_users:
    pprint.pprint(user.__dict__)

update_user(washerbuddie_db, test_user, replacement_user)
print("\nAfter updating Nikhil Jindal:")
pprint.pprint(washerbuddie_db.Users.find_one({"_user_name": "Nikhil Jindal"}))

delete_single_user(washerbuddie_db, test_user)
print("\nAfter deleting Nikhil Jindal:")
print("Remaining Users: ", len(get_valid_users(washerbuddie_db)))

print("\nDeleting all remaining users: ")
delete_multiple_users(washerbuddie_db, [test_admin_user, test_secondary_user])
print("Remaining Users: ", len(get_valid_users(washerbuddie_db)))


insert_washer(washerbuddie_db, washer1)
insert_washer(washerbuddie_db, washer2)
insert_dryer(washerbuddie_db, dryer1)
insert_dryer(washerbuddie_db, dryer2)
pprint.pprint(list(washerbuddie_db.Machines.find()))