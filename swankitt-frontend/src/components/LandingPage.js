import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TshirtCard from './TshirtCard'; // Import your TshirtCard component
import Navbar from './Navbar'; // Import the Navbar component

const LandingPage = () => {
  const [tshirts, setTshirts] = useState([]);

  useEffect(() => {
    console.log('Fetching t-shirts...');
    axios.get('http://localhost:8000/tshirts')
      .then((response) => {
        console.log('T-shirts received:', response.data);
        setTshirts(response.data);
      })
      .catch((error) => {
        console.error('Error fetching t-shirts:', error);
      });
  }, []);
  
  return (
    <center>
    <div>
      <Navbar /> {/* Include the Navbar component here */}
      <h1>Welcome to Swankitt</h1>
      <div className="tshirt-list" style={{ display: 'flex', flexWrap: 'wrap' }}>
        {tshirts.map((tshirt) => (
          <TshirtCard
            key={tshirt.id}
            title={tshirt.title}
            price={tshirt.price}
            imageSrc={`http://localhost:8000/tshirts/images/${tshirt.id}`} // Replace with your backend URL
            style={{ flex: '0 0 calc(33.33% - 10px)', border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }} // Adjust styling as needed
          />
        ))}
      </div>
    </div>
    </center>
  );
};

export default LandingPage;
