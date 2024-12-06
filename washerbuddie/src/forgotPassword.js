import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './Header';
import { API_BASE_URL } from './config';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request to /reset_password
      const response = await fetch(`${API_BASE_URL}/api/reset_password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'email': email }),
      });

      // Check if the response was successful
      if (response.ok) {
        toast.success(
          'If an account with that email exists, you will receive a reset email shortly.',
          { position: toast.POSITION.TOP_RIGHT }
        );
      } else {
        toast.error('Failed to process your request. Please try again later.', {
          position: toast.POSITION.TOP_RIGHT,
        });
      }

      // Redirect after a short delay
      setTimeout(() => {
        navigate('/login');
      }, 1000);
    } catch (error) {
      toast.error('An error occurred. Please try again later.', {
        position: toast.POSITION.TOP_RIGHT,
      });
    }
  };

  return (
    <>
      <Header />
      <div style={styles.container}>
        <h1 style={styles.title}>Forgot Password</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Enter Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={styles.input}
            />
          </div>
          <button type="submit" style={styles.button}>Submit</button>
        </form>
      </div>
      <ToastContainer />
    </>
  );
}

const styles = {
  container: {
    width: '400px',
    margin: '50px auto',
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    textAlign: 'center',
  },
  title: {
    marginBottom: '20px',
    color: '#333',
    fontSize: '24px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
  },
  inputGroup: {
    marginBottom: '15px',
    textAlign: 'left',
  },
  label: {
    display: 'block',
    marginBottom: '5px',
    color: '#555',
  },
  input: {
    width: '100%',
    padding: '10px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    fontSize: '16px',
    boxSizing: 'border-box',
  },
  button: {
    padding: '10px 15px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
    marginTop: '10px',
  },
};

export default ForgotPassword;
