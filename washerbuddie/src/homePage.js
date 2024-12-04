import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import Header from './Header';
import Menu from './menu';
import './App.css';

function HomePage() {
    const [machines, setMachines] = useState([]);
    const navigate = useNavigate();
    const userName = 'test_user'; // Replace with the logged-in user's name

    const fetchMachines = async () => {
        try {
            const response = await fetch('/get_machines');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();

            if (Array.isArray(data.DB_machines)) {
                const machineArray = data.DB_machines.map((machine) => {
                    const startTime = new Date(machine._start_time);
                    const endTime = new Date(machine._end_time);
                    const now = new Date();

                    let timeRemaining = 0;
                    if (machine._current_state === 'In Use' && now < endTime) {
                        timeRemaining = Math.max(0, Math.round((endTime - now) / 60000));
                    }

                    return {
                        id: machine._machine_id,
                        type: machine._machine_type,
                        status: machine._current_state,
                        timeRemaining,
                    };
                });
                setMachines(machineArray);
            } else {
                console.error('Expected an array of machines but got:', data);
            }
        } catch (error) {
            console.error('Error fetching machine data:', error);
        }
    };

    useEffect(() => {
        fetchMachines();

        const interval = setInterval(() => {
            setMachines((prevMachines) =>
                prevMachines.map((machine) => {
                    if (machine.status === 'In Use' && machine.timeRemaining > 0) {
                        const newTimeRemaining = machine.timeRemaining - 1;

                        // Call end_session when timeRemaining reaches 0
                        if (newTimeRemaining === 0) {
                            endSession(machine.id);
                        }

                        return { ...machine, timeRemaining: newTimeRemaining };
                    }
                    return machine;
                })
            );
        }, 60000); // Decrement timeRemaining every minute

        return () => clearInterval(interval);
    }, []);

    const endSession = async (machineId) => {
        try {
            const response = await fetch('/end_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    machine_id: machineId,
                    user_name: userName,
                }),
            });

            const result = await response.json();
            if (response.ok && result.success) {
                console.log(`Session ended for machine ${machineId}: ${result.message}`);
                setMachines((prevMachines) =>
                    prevMachines.map((machine) =>
                        machine.id === machineId
                            ? { ...machine, status: 'Available', timeRemaining: 0 }
                            : machine
                    )
                );
            } else {
                console.error(`Failed to end session for machine ${machineId}:`, result.error);
            }
        } catch (error) {
            console.error('Error ending session:', error);
        }
    };

    const handleStartEndUse = async (id) => {
        const machine = machines.find((m) => m.id === id);

        if (machine) {
            if (machine.status === 'Available') {
                try {
                    const response = await fetch('/create_session', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            machine_id: machine.id,
                            user_name: userName,
                        }),
                    });

                    const result = await response.json();
                    if (response.ok && result.success) {
                        const timeRemaining = machine.type === 'Dryer' ? 60 : 50;
                        setMachines((prevMachines) =>
                            prevMachines.map((m) =>
                                m.id === id
                                    ? { ...m, status: 'In Use', timeRemaining }
                                    : m
                            )
                        );
                    } else {
                        toast.error(result.error || 'Failed to create session.');
                    }
                } catch (error) {
                    toast.error('You must sign in to start a session.');
                }
            } else {
                endSession(id);
            }
        }
    };

    const handleLogout = () => {
        navigate('/login');
    };

    return (
        <div>
            <Menu />
            <Header />
            <div className="machine-list">
                {machines.map((machine) => (
                    <div key={machine.id} className="machine-tile">
                        <h3>
                            {machine.type} {machine.id}
                        </h3>
                        <p>Status: {machine.status}</p>
                        <p>Time Remaining: {machine.timeRemaining} mins</p>
                        <button
                            onClick={() => handleStartEndUse(machine.id)}
                            disabled={machine.status !== 'Available'}
                            style={{
                                backgroundColor: machine.status === 'Available' ? '#007bff' : '#d3d3d3',
                                color: machine.status === 'Available' ? '#fff' : '#808080',
                                cursor: machine.status === 'Available' ? 'pointer' : 'not-allowed',
                            }}
                        >
                            {machine.status === 'Available' ? 'Start Use' : 'End Use'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default HomePage;
