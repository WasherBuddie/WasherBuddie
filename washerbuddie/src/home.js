import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import './home.css';
import './Header.css'

function Home() {
  const navigate = useNavigate();
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowButton(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      <Header />
      <div className="home-container">
        <h1 className='h1'>Welcome to Washer Buddie</h1>
        <p className='p'>Your one-stop spot for all laundry needs!</p>
        {showButton && (
          <button onClick={() => navigate('/home-page')}>Continue</button>
        )}
      </div>
    </>
  );
}

export default Home;
