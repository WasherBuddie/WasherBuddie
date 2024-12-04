import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './menu.css';

function Menu() {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('/logout', { method: 'POST' });
  
      if (response.ok) {
        toast.success('Logged out successfully!');
        navigate('/login');
      } else {
        const errorData = await response.json();
        toast.error(errorData.message || 'Logout failed!');
      }
    } catch (error) {
      toast.error('An error occurred during logout.');
    }
  };
  

  return (
    <div className="menu-container">
      <button className="menu-toggle" onClick={toggleMenu}>
        Menu
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <ul>
            <li><button onClick={() => navigate('/user-preferences')}>Settings</button></ li>
            <li><button onClick={() => navigate('/login')}>Login</button></ li>
            <li><button onClick={handleLogout}>Log out</button></li>
          </ul>
        </div>
      )}
      <ToastContainer position="top-right" autoClose={1000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
    </div>
  );
}
export default Menu;