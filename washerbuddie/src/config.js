export const API_BASE_URL = 
  process.env.NODE_ENV === 'production'
    ? 'https://washerbuddie.onrender.com'
    : 'http://localhost:5000';