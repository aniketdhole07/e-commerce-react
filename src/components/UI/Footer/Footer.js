import React from 'react';
import './Footer.scss';


import SocialMedia from '../SocialMedia/SocialMedia';

const footer = () => (
  <footer className="footer">
    <div className="questions">
      <div className="questions-wrapper">
        <div className="questions-text">
          <h3 className="title">Questions</h3>
          <p className="subtitle">Ask your Questions directly to the given Contact Number : +91 8767383986 (WhatsApp and Call) </p>
        </div>
      
      </div>
    </div>
    <SocialMedia />
    
    <p className="advertising">Made by Aniket Dhole</p>
  </footer>
);

export default footer;