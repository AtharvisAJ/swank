import React from 'react';

const TshirtCard = ({ title, price, imageSrc }) => {
  return (
    <div className="tshirt-card">
      <img src={imageSrc} alt={title} className="tshirt-image" />
      <h2 className="tshirt-title">{title}</h2>
      <p className="tshirt-price">Price: ${price}</p>
      <button className="add-to-cart-button">Add to Cart</button>
    </div>
  );
};

export default TshirtCard;
