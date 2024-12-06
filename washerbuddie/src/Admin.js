import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import Menu from './menu';
import './App.css';
import { API_BASE_URL } from './config';

function AdminPage() {
    const [machines, setMachines] = useState([]);
    const [users, setUsers] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Check if the user is an admin
    useEffect(() => {
        const checkAdminStatus = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/get_admin`);
                if (!response.ok) {
                    throw new Error('Failed to check admin status');
                }
                const isAdmin = await response.json();
                if (!isAdmin) {
                    navigate('/login'); // Redirect to login if not an admin
                }
            } catch (error) {
                console.error('Error checking admin status:', error);
                navigate('/login'); // Redirect to login on error
            }
        };

        checkAdminStatus();
    }, [navigate]);

    // Fetch machine data
    const fetchMachines = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/get_machines`);
            if (!response.ok) {
                throw new Error(`Failed to fetch machines: ${response.statusText}`);
            }
            const data = await response.json();
            if (Array.isArray(data.DB_machines)) {
                const machineArray = data.DB_machines.map((machine) => ({
                    id: machine._machine_id,
                    type: machine._machine_type,
                    status: machine._current_state,
                }));
                setMachines(machineArray);
            }
        } catch (error) {
            console.error('Error fetching machine data:', error);
        }
    };

    // Fetch user data
    const fetchUsers = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/get_users`);
            if (!response.ok) {
                throw new Error(`Failed to fetch users: ${response.statusText}`);
            }
            const data = await response.json();
            if (Array.isArray(data.DB_users)) {
                const userArray = data.DB_users.map((user) => ({
                    id: user._user_name,
                    name: user._user_name, // Use _user_name for the display name
                    email: user._user_email, // If you want to show the email as well
                    role: user._is_admin ? "Admin" : "Member",
                }));
                setUsers(userArray);
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    };

    useEffect(() => {
        const loadData = async () => {
            await fetchMachines();
            await fetchUsers();
            setTimeout(() => setLoading(false), 2000); // Wait for 2 seconds
        };
        loadData();
    }, []);

    // Set machine out of order
    const handleSetOutOfOrder = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/set_out_of_order`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ machine_id: id }),
            });
            if (response.ok) {
                setMachines((prevMachines) =>
                    prevMachines.map((m) =>
                        m.id === id ? { ...m, status: 'Out of Order' } : m
                    )
                );
            } else {
                console.error('Failed to set machine out of order');
            }
        } catch (error) {
            console.error('Error setting machine out of order:', error);
        }
    };

    // Return machine to service
    const handleReturnToService = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/return_to_service`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ machine_id: id }),
            });
            if (response.ok) {
                setMachines((prevMachines) =>
                    prevMachines.map((m) =>
                        m.id === id ? { ...m, status: 'Available' } : m
                    )
                );
            } else {
                console.error('Failed to return machine to service');
            }
        } catch (error) {
            console.error('Error returning machine to service:', error);
        }
    };

    // Delete user account
    const handleDeleteUser = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/delete_user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: id }),
            });
            if (response.ok) {
                setUsers((prevUsers) => prevUsers.filter((user) => user.id !== id));
            } else {
                console.error('Failed to delete user');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    // Promote user to admin
    const handlePromoteUser = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/promote_user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: id }),
            });
            if (response.ok) {
                setUsers((prevUsers) =>
                    prevUsers.map((user) =>
                        user.id === id ? { ...user, role: 'Admin' } : user
                    )
                );
            } else {
                console.error('Failed to promote user');
            }
        } catch (error) {
            console.error('Error promoting user:', error);
        }
    };

    // Send message
    const handleSendMessage = async () => {
        if (message.trim()) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/send_message`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message }),
                });
                if (response.ok) {
                    alert('Message sent successfully!');
                    setMessage('');
                } else {
                    console.error('Failed to send message');
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
    };

    if (loading) {
        return (
            <div className="loading-screen">
                <h2>Page is loading...</h2>
            </div>
        );
    }

    return (
        <div>
            <Menu />
            <Header />
            <div className="admin-controls">
                {/* Machines section */}
                <h2 className="admin-titles">Machines</h2>
                <div className="section">
                    <div className="machine-list">
                        {machines.map((machine) => (
                            <div key={machine.id} className="machine-tile">
                                <h3>
                                    {machine.type} {machine.id}
                                </h3>
                                <p>Status: {machine.status}</p>
                                <button
                                    onClick={
                                        machine.status === 'Out of Order'
                                            ? () => handleReturnToService(machine.id)
                                            : () => handleSetOutOfOrder(machine.id)
                                    }
                                    style={{
                                        backgroundColor: machine.status === 'Out of Order' ? '#007bff' : '#ff0000',
                                        color: '#fff',
                                        cursor: 'pointer',
                                    }}
                                >
                                    {machine.status === 'Out of Order' ? 'Return to Service' : 'Set Out of Order'}
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Users section */}
                <h2 className="admin-titles">Users</h2>
                <div className="section">
                    <div className="machine-list">
                        {users.length > 0 ? (
                            users.map((user) => (
                                <div key={user.id} className="machine-tile">
                                    <h3>{user.name}</h3>
                                    <p>Email: {user.email}</p>
                                    <p>Role: {user.role}</p>
                                    <button
                                        onClick={() => handleDeleteUser(user.id)}
                                        style={{ backgroundColor: '#ff0000', color: '#fff' }}
                                    >
                                        Delete Account
                                    </button>
                                    <button className='spacer'
                                        onClick={() => handlePromoteUser(user.id)}
                                        style={{
                                            backgroundColor: user.role === 'Admin' ? '#d3d3d3' : '#007bff',
                                            color: user.role === 'Admin' ? '#808080' : '#fff',
                                        }}
                                        disabled={user.role === 'Admin'}
                                    >
                                        Promote
                                    </button>
                                </div>
                            ))
                        ) : (
                            <p>No users available.</p> // Show this if no users are present
                        )}
                    </div>
                </div>

{/* Send Message section */}
<div className="section message-section">
    <h2 className="message-title">Send Message</h2>
    <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter your message here..."
        className="message-textarea"
    />
    <button onClick={handleSendMessage} className="send-button">Send Message</button>
</div>

            </div>
        </div>
    );
}

export default AdminPage;
