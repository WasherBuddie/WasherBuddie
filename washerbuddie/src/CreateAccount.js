import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './Header';
import './App.css';

function CreateAccount() {
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      user_name: email.split("@")[0], // Using email prefix as username
      notification_preference: 'Email', // Assuming email notifications by default
      user_phone_number: phone,
      user_email: email,
      phone_carrier: 'Verizon', // Add logic to capture this if needed
      password: password,
      is_admin: false, // Default to false
    };

    try {
      const response = await fetch('/add_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const result = await response.json();
      if (response.ok && result.success) {
        toast.success('Account created successfully!', { position: toast.POSITION.TOP_RIGHT });
        navigate('/home-page'); // Redirect on success
      } else {
        setError(result.error || 'Failed to create account.');
        toast.error(result.error || 'Failed to create account.', { position: toast.POSITION.TOP_RIGHT });
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      toast.error('An error occurred. Please try again.', { position: toast.POSITION.TOP_RIGHT });
    }
  };

  return (
    <div>
      <Header />
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Phone</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Create Account</button>
      </form>
      <div>
        <Link to="/login">Already have an account? Log In</Link>
      </div>
    </div>
  );
}

export default CreateAccount;
