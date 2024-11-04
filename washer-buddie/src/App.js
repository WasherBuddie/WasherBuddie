import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import Login from './components/login';
import './App.css';
import CreateAccount from './components/CreateAccount';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">Washer Buddie</header>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create-account" element={<CreateAccount/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;