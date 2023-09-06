// App.js or your main application file
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Navbar from './components/Navbar'; // Import your Navbar component
import LandingPage from './components/LandingPage';
import "./App.css";

function App() {
  return (
    <Router>
      
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {/* Add routes for Login, Products, Cart, and About Us here */}
      </Routes>
    </Router>
  );
}

export default App;
