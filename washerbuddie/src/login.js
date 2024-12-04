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
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ borderColor: error ? 'red' : '' }}
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ borderColor: error ? 'red' : '' }}
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit">Log In</button>
            </form>
            <div>
                <Link to="/forgot-password">Forgot Password?</Link>
                <Link to="/create-Account">Create Account</Link>
            </div>
        </div>
    );
}

export default Login;