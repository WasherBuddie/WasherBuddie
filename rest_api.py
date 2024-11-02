from flask import Flask, request, jsonify
from Interaction_Manager import Interaction_Manager as im

washerbuddie = Flask(__name__)



@washerbuddie.route("/get-user", methods=["GET"])
def get_user():
    user_data = request.get_json
    user_name = request.get_json
    #needs to return the user from the db 
    return True
    
@washerbuddie.route("/create-user", methods=["PUT"])
def create_user():
    user_data = request.get_json
    user_name = user_data.get("name")
    user_password = user_data.get("password")
    user_email = user_data.get("email")
    user_phone = user_data.get("phone")
    user_contact_method = user_data.get("preferred")
    user_provider = user_data.get("provider")
    user_admin = user_data.get("admin", False)
    result = im.add_user(user_name, user_contact_method, user_phone, user_email,user_provider, user_admin)
    if result:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 500
    

@washerbuddie.route("/update-user", methods=["POST"])
def update_user():
    user_data = request.get_json
    update_type = user_data.get("type")
    def switch(update_type):
        if update_type == "0":
            #update user password
            return jsonify({"message": "User password updated successfully"}), 201
        elif update_type == "1":
            #update communication preference
            return jsonify({"message": "User password updated successfully"}), 201
        elif update_type == "2":
            #update email field
            return jsonify({"message": "User password updated successfully"}), 201
        elif update_type == "3":
            #update phone field
            return jsonify({"message": "User password updated successfully"}), 201


@washerbuddie.route("/get-machines", methods=["GET"])
def get_machines():
    #call from db the machine table
    #jsonify it, and push the data
    return True

@washerbuddie.route("/create-machine", methods=["PUT"])
def create_machine():
    machine_data = request.get_json
    machine_type = machine_data.get("type")
    if machine_type == "Washer":
        im.add_washer()
    else:
        im.add_dryer()
    
@washerbuddie.route("/update-machine", methods=["POST"])
def update_machine():
    machine_data = request.get_json
    update_type = machine_data.get("type")
    def switch(update_type):
        if update_type == "0":
            state = machine_data.get("state")
            machine_id = machine_data.get("id")
            #update the state of the machine with given id with state
            return jsonify({"message": "Machine state has been updated successfully"}), 201
        elif update_type == "1":
            state = machine_data.get("state")
            machine_id = machine_data.get("id")
            user = machine_data.get("user")
            start = machine_data.get("start")
            end = machine_data.get("end")
            #update machine with new session using user, state,start,end and id
            return jsonify({"message": "New machine session has been created"}), 201
        







if __name__ == "__main__":
    washerbuddie.run(debug=True)

