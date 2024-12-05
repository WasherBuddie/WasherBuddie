import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './Header';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            });

            const result = await response.json();

            if (response.ok && result.success) {
                toast.success('Login successful!', { position: toast.POSITION.TOP_RIGHT });
                navigate('/home-page'); // Redirect to home page on successful login
            } else {
                setError(result.message || 'Authentication failed. Please try again.');
                toast.error(result.message || 'Authentication failed. Please try again.', { position: toast.POSITION.TOP_RIGHT });
            }
        } catch (err) {
            setError('An error occurred. Please try again.');
            toast.error('An error occurred. Please try again.', { position: toast.POSITION.TOP_RIGHT });
        }
    };

    return (
        <div>
            <Header />
            <div style={styles.container}>
                <h2 style={styles.title}>Login</h2>
                <form onSubmit={handleSubmit} style={styles.form}>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            style={{ ...styles.input, borderColor: error ? 'red' : '' }}
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            style={{ ...styles.input, borderColor: error ? 'red' : '' }}
                        />
                    </div>
                    {error && <p style={styles.error}>{error}</p>}
                    <button type="submit" style={styles.button}>Log In</button>
                </form>
                <div style={styles.links}>
                    <Link to="/forgot-password" style={styles.link}>Forgot Password?</Link>
                    <Link to="/create-Account" style={styles.link}>Create Account</Link>
                </div>
            </div>
        </div>
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
    error: {
        color: 'red',
        fontSize: '14px',
        marginBottom: '10px',
    },
    links: {
        marginTop: '20px',
        display: 'flex',
        justifyContent: 'space-between',
    },
    link: {
        color: '#007bff',
        textDecoration: 'none',
        fontSize: '14px',
    },
};

export default Login;