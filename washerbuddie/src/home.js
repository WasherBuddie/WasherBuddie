import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from './Header';

function Home() {
  const navigate = useNavigate();
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowButton(true);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      <Header />
      <div>
        <h1>Welcome to Washer Buddie</h1>
        <p>Your one-stop spot for all laundry needs!</p>
        {showButton && (
          <button onClick={() => navigate('/home-page')}>Continue</button>
        )}
      </div>
    </>
  );
}

export default Home;