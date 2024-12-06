from flask import Flask, session, request, jsonify, send_from_directory
from src.Service_Layer.Interaction_Manager import Interaction_Manager
from mongoDB.CRUD_api import Database_Manager
import bcrypt
from src.Service_Layer.User import User
import os
from flask_cors import CORS
import secrets

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = secrets.token_hex(16)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "supports_credentials": True
    }
})

# Initialize the interaction manager
interaction_manager = Interaction_Manager()

# API routes
@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.json
        user_name = session.get('user_name') or data.get('user_name')
        code = data.get("code")
        value = data.get("value")

        if not user_name or code is None or not value:
            return jsonify({"success": False, "error": "Invalid input"}), 400

        result = interaction_manager.user_update(user_name, code, value)

        if result:
            return jsonify({"success": True, "message": "Update successful"}), 200
        else:
            return jsonify({"success": False, "error": "Update failed"}), 500
    except Exception as e:
        app.logger.error(f"Error in update endpoint: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400

    try:
        is_authenticated = interaction_manager.authenticate_log_in(email, password)
        if is_authenticated:
            user_data = interaction_manager.get_user(email)
            session['user_name'] = user_data.get('user_name')
            session['email'] = user_data.get('email')
            session['phone_carrier'] = user_data.get('phone_carrier')
            session['notification_preferenece'] = user_data.get('notification_preferenece')
            session['phone_number'] = user_data.get('phone_number')
            session['is_admin'] = user_data.get('is_admin')
            return jsonify({'success': True, 'message': 'Authentication successful'}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/profile', methods=['GET'])
def profile():
    user_email = session.get('email')
    if not user_email:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401
   
    user = interaction_manager.get_user(user_email)
    return jsonify({'success': True, 'user': user})

@app.route('/get_by_email', methods=['GET'])
def get_user_by_email():
    data = request.json
    email = data.get('email')
    return interaction_manager.get_user(email)

@app.route('/add_washer', methods=['POST'])
def add_washer():
    try:
        success = interaction_manager.add_washer()
        return jsonify({'success': success, 'message': 'Washer added successfully' if success else 'Failed to add washer'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/add_dryer', methods=['POST'])
def add_dryer():
    try:
        success = interaction_manager.add_dryer()
        return jsonify({'success': success, 'message': 'Dryer added successfully' if success else 'Failed to add dryer'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_machines', methods=['GET'])
def get_machines():
    try:
        rv = []
        for machine in Database_Manager().get_all_machines():
            rv.append(machine.__dict__)
        return jsonify({'DB_machines': rv})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        rv = []
        for user in Database_Manager().get_all_users():
            rv.append(user.__dict__)
        return jsonify({'DB_users': rv})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/send_notification', methods=['POST'])
def send_notification():
    try:
        data = request.json
        sending_user_name = data.get('sending_user_name')
        receiving_user_name = data.get('receiving_user_name')
        sending_user = Database_Manager().get_specific_user(sending_user_name)
        receiving_user = Database_Manager().get_specific_user(receiving_user_name)
        message = data.get('message')
       
        interaction_manager.send_notification(sending_user, receiving_user, message)
        return jsonify({'success': True, 'message': 'Notification sent successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        user_name = data.get('user_name')
        notification_preference = data.get('notification_preference')
        user_phone_number = int(data.get('user_phone_number'))
        user_email = data.get('user_email')
        phone_carrier = data.get('phone_carrier')
        is_admin = data.get('is_admin', False)
        password = data.get('password', 'defaultpassword123')

        if not user_name:
            return jsonify({'success': False, 'error': 'No username was provided'}), 400
       
        if len(user_email) <= 0 or '@' not in user_email or '.' not in user_email:
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400

        success = interaction_manager.add_user(user_name, notification_preference, user_phone_number, user_email, phone_carrier, is_admin, password)
        return jsonify({'success': success, 'message': 'User added successfully' if success else 'Failed to add user'})
    except Exception as e:
        print(f"Error adding user: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/remove_user', methods=['DELETE'])
def remove_user():
    try:
        data = request.json
        user_name = data.get('user_name')
        success = interaction_manager.remove_user(user_name)
        return jsonify({'success': success, 'message': 'User removed successfully' if success else 'Failed to remove user'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200

@app.route('/get_admin', methods=['GET'])
def get_admin():
    return jsonify({"admin": session.get('is_admin', False)}), 200

@app.route('/reset_password', methods=['GET'])
def reset_password():
    try:
        data = request.json
        email = data.get('email')
        user_data = interaction_manager.get_user(email)
        user = User(
            user_data['user_name'],
            user_data['email'],
            user_data['phone_carrier'],
            user_data['notification_preference'],
            user_data['phone_number'],
            user_data['is_admin'],
            "fakepass"
        )
        interaction_manager.reset_password(user)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/authenticate_log_in', methods=['POST'])
def authenticate_log_in():
    try:
        data = request.json
        email_address = data.get('email_address')
        password = data.get('password')
        success = interaction_manager.authenticate_log_in(email_address, password)
        return jsonify({'success': success, 'message': 'Authentication successful' if success else 'Authentication failed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/create_session', methods=['POST'])
def create_session():
    try:
        data = request.json
        machine_id = data.get('machine_id')
        user_name = session.get('user_name')
       
        if not user_name:
            return jsonify({'success': False, 'error': 'User not logged in'}), 401

        machines = Database_Manager().get_all_machines()
        users = Database_Manager().get_valid_users()
       
        if machine_id not in [machine.machine_id for machine in machines] or user_name not in [user.user_name for user in users]:
            return jsonify({'success': False, 'error': 'Machine or User not found'}), 404

        user = Database_Manager().get_specific_user(user_name)
        success = interaction_manager.create_session(machine_id, user)
        return jsonify({'success': success, 'message': 'Session created successfully' if success else 'Failed to create session'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/end_session', methods=['POST'])
def end_session():
    try:
        data = request.json
        machine_id = data.get('machine_id')
        success = interaction_manager.end_session(machine_id)
        return jsonify({'success': success, 'message': 'Session ended successfully' if success else 'Failed to end session'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/set_out_of_order', methods=['POST'])
def set_out_of_order():
    try:
        data = request.json
        machine_id = data.get('machine_id')
        user_name = session.get('user_name')

        if not user_name:
            return jsonify({'success': False, 'error': 'User not logged in'}), 401

        machines = Database_Manager().get_all_machines()
        users = Database_Manager().get_valid_users()
       
        if machine_id not in [machine.machine_id for machine in machines] or user_name not in [user.user_name for user in users]:
            return jsonify({'success': False, 'error': 'Machine or User not found'}), 404

        user = Database_Manager().get_specific_user(user_name)
        success = interaction_manager.set_out_of_order(machine_id, user)
        return jsonify({'success': success, 'message': 'Machine status updated successfully' if success else 'Failed to update machine status'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/return_to_service', methods=['POST'])
def return_to_service():
    try:
        data = request.json
        machine_id = data.get('machine_id')
        user_name = session.get('user_name')

        if not user_name:
            return jsonify({'success': False, 'error': 'User not logged in'}), 401

        machines = Database_Manager().get_all_machines()
        users = Database_Manager().get_valid_users()
       
        if machine_id not in [machine.machine_id for machine in machines] or user_name not in [user.user_name for user in users]:
            return jsonify({'success': False, 'error': 'Machine or User not found'}), 404

        user = Database_Manager().get_specific_user(user_name)
        success = interaction_manager.return_to_service(machine_id, user)
        return jsonify({'success': success, 'message': 'Machine status updated successfully' if success else 'Failed to update machine status'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_status', methods=['GET'])
def get_status():
    try:
        machine_id = request.args.get('machine_id')  # Changed from request.json to request.args for GET request
       
        if not machine_id:
            return jsonify({'success': False, 'error': 'Machine ID is required'}), 400
           
        machines = Database_Manager().get_all_machines()
        if machine_id not in [machine.machine_id for machine in machines]:
            return jsonify({'success': False, 'error': 'Machine not found'}), 404
       
        status = interaction_manager.get_status(machine_id)
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/notify_user', methods=['POST'])
def notify_user():
    try:
        data = request.json
        machine_id = data.get('machine_id')
        user_name = data.get('user_name')

        user = Database_Manager().get_specific_user(user_name)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
       
        success = interaction_manager.notify_user(machine_id, user)
        return jsonify({'success': success, 'message': 'Notification sent successfully' if success else 'Failed to send notification'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Serve static files and handle client-side routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f'Server error: {e}')
    return jsonify(error=str(e)), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)