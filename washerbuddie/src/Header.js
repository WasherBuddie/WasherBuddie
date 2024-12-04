import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import './Header.css';

function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate(); // Initialize navigate

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  // Function to handle redirection
  const redirectToHome = () => {
    navigate('/home-page'); // Redirect to the home page
  };

  return (
    <header className="app-header">
      <div className="bubbles">
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
        <div className="bubble"></div>
      </div>
      <div className="header-content">
        {/* Add onClick to the h1 */}
        <h1 onClick={redirectToHome} style={{ cursor: 'pointer' }}>
          WasherBuddie
        </h1>
      </div>
    </header>
  );
}

export default Header;
