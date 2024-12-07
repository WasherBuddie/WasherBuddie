import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './login';
import CreateAccount from './CreateAccount';
import HomePage from './homePage';
import Home from './home';
import ForgotPassword from './forgotPassword';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './Header';
import UserPreferences from './UserPreferences';
import Admin from './Admin';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/create-account" element={<CreateAccount />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/home-page" element={<HomePage />} />
        <Route path="/user-preferences" element={<UserPreferences />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
      <ToastContainer />
    </Router>
  );
}

export default App;