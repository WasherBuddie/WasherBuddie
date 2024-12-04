import unittest
from app import app, interaction_manager
from flask import Flask, json, jsonify, session
from unittest.mock import patch, MagicMock
from mongoDB.CRUD_api import Database_Manager

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()
        
    def test_add_dryer_empty_request(self):
        """Test that the add_dryer endpoint can handle empty requests"""
        response = self.client.post('/add_dryer', data={})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('success', data)

    def test_add_dryer_exception(self):
        """Test that add_dryer handles exceptions and returns the correct error response."""
        with patch.object(interaction_manager, 'add_dryer', side_effect=Exception('Test error')):
            response = self.client.post('/add_dryer')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['error'], 'Test error')

    def test_add_dryer_failure(self):
        """Test that add_dryer handles failure to add a dryer and returns the correct response."""
        with patch.object(interaction_manager, 'add_dryer', return_value=False):
            response = self.client.post('/add_dryer')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Failed to add dryer')

    def test_add_dryer_invalid_content_type(self):
        """Test that the add_dryer endpoint can handle requests with invalid content types"""
        response = self.client.post('/add_dryer', data='invalid data', content_type='text/plain')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('success', data)

    def test_add_dryer_invalid_method(self):
        """Test that the add_dryer endpoint only responds to POST requests"""
        response = self.client.get('/add_dryer')
        self.assertEqual(response.status_code, 404)

    def test_add_dryer_success(self):
        """Test that add_dryer successfully adds a dryer and returns the correct response."""
        with patch.object(interaction_manager, 'add_dryer', return_value=True):
            response = self.client.post('/add_dryer')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Dryer added successfully')

    def test_add_user(self):
        """Test adding a user successfully with valid input data."""
        with patch.object(interaction_manager, 'add_user', return_value=True):
            test_data = {
                'user_name': 'testuser',
                'notification_preference': 'email',
                'user_phone_number': '1234567890',
                'user_email': 'testuser@example.com',
                'phone_carrier': 'AT&T',
                'is_admin': False,
                'password': 'testpassword123'
            }

            response = self.client.post('/add_user', json=test_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'success': True, 'message': 'User added successfully'})

    def test_add_user_empty_username(self):
        """Test adding a user with an empty username"""
        data = {
            'user_name': '',
            'notification_preference': 'email',
            'user_phone_number': '1234567890',
            'user_email': 'test@example.com',
            'phone_carrier': 'AT&T'
        }
        response = self.client.post('/add_user', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'No username was provided')

    def test_add_user_exception(self):
        """Test adding a user when an exception occurs."""
        with patch.object(interaction_manager, 'add_user', side_effect=Exception('Test exception')):
            test_data = {
                'user_name': 'testuser',
                'notification_preference': 'email',
                'user_phone_number': '1234567890',
                'user_email': 'testuser@example.com',
                'phone_carrier': 'AT&T'
            }

            response = self.client.post('/add_user', json=test_data)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json, {'success': False, 'error': 'Test exception'})

    def test_add_user_invalid_email(self):
        """Test adding a user with an invalid email address"""
        data = {
            'user_name': 'testuser',
            'notification_preference': 'email',
            'user_phone_number': '1234567890',
            'user_email': 'invalid_email',
            'phone_carrier': 'Sprint'
        }
        response = self.client.post('/add_user', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email', json.loads(response.data)['error'])

    def test_update_invalid_input(self):
        """Test update endpoint with invalid input"""
        response = self.client.post('/update', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Invalid input')

    def test_authenticate_log_in_success(self):
        """Test successful login authentication"""
        with patch.object(interaction_manager, 'authenticate_log_in', return_value=True):
            credentials = {
                'email_address': 'test@example.com',
                'password': 'testpass'
            }
            response = self.client.post('/authenticate_log_in', json=credentials)
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Authentication successful')

    def test_authenticate_log_in_failure(self):
        """Test failed login authentication"""
        with patch.object(interaction_manager, 'authenticate_log_in', return_value=False):
            credentials = {
                'email_address': 'wrong@example.com',
                'password': 'wrongpass'
            }
            response = self.client.post('/authenticate_log_in', json=credentials)
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Authentication failed')

    def test_logout(self):
        """Test logout functionality"""
        response = self.client.post('/logout')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Logged out successfully!')

    def test_add_washer_success(self):
        """Test successfully adding a washer"""
        with patch.object(interaction_manager, 'add_washer', return_value=True):
            response = self.client.post('/add_washer')
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Washer added successfully')

    def test_add_washer_failure(self):
        """Test failure in adding a washer"""
        with patch.object(interaction_manager, 'add_washer', return_value=False):
            response = self.client.post('/add_washer')
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Failed to add washer')

    def test_add_dryer_success(self):
        """Test successfully adding a dryer"""
        with patch.object(interaction_manager, 'add_dryer', return_value=True):
            response = self.client.post('/add_dryer')
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Dryer added successfully')

    def test_add_dryer_failure(self):
        """Test failure in adding a dryer"""
        with patch.object(interaction_manager, 'add_dryer', return_value=False):
            response = self.client.post('/add_dryer')
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Failed to add dryer')

    def test_send_notification_success(self):
        """Test successfully sending a notification"""
        notification_data = {
            'sending_user_name': 'sender',
            'receiving_user_name': 'receiver',
            'message': 'test message'
        }
        with patch.object(Database_Manager, 'get_specific_user', return_value=MagicMock()):
            with patch.object(interaction_manager, 'send_notification', return_value=None):
                response = self.client.post('/send_notification', json=notification_data)
                data = response.get_json()
                
                self.assertEqual(response.status_code, 200)
                self.assertTrue(data['success'])
                self.assertEqual(data['message'], 'Notification sent successfully')

    def test_add_user_success(self):
        """Test successfully adding a user"""
        test_data = {
            'user_name': 'testuser',
            'notification_preference': 'email',
            'user_phone_number': '1234567890',
            'user_email': 'test@example.com',
            'phone_carrier': 'AT&T',
            'is_admin': False,
            'password': 'testpassword123'
        }
        with patch.object(interaction_manager, 'add_user', return_value=True):
            response = self.client.post('/add_user', json=test_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'success': True, 'message': 'User added successfully'})

    def test_add_user_empty_username(self):
        """Test adding a user with empty username"""
        test_data = {
            'user_name': '',
            'notification_preference': 'email',
            'user_phone_number': '1234567890',
            'user_email': 'test@example.com',
            'phone_carrier': 'AT&T'
        }
        response = self.client.post('/add_user', json=test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'No username was provided')

    def test_add_user_invalid_email(self):
        """Test adding a user with invalid email"""
        test_data = {
            'user_name': 'testuser',
            'notification_preference': 'email',
            'user_phone_number': '1234567890',
            'user_email': 'invalid_email',
            'phone_carrier': 'AT&T'
        }
        response = self.client.post('/add_user', json=test_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid email', json.loads(response.data)['error'])

    def test_remove_user_success(self):
        """Test successfully removing a user"""
        with patch.object(interaction_manager, 'remove_user', return_value=True):
            response = self.client.delete('/remove_user', json={'user_name': 'testuser'})
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'User removed successfully')

    def test_remove_user_failure(self):
        """Test failure in removing a user"""
        with patch.object(interaction_manager, 'remove_user', return_value=False):
            response = self.client.delete('/remove_user', json={'user_name': 'testuser'})
            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Failed to remove user')

if __name__ == '__main__':
    unittest.main()