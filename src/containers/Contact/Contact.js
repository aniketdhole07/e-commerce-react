import React from 'react';
import './Contact.scss';
import ScrollToTopOnMount from '../../shared/ScrollToTopOnMount';

const contact = () => (
  <>
    <ScrollToTopOnMount />
    <div className="contact-container">
      <h2 className="main-title">Contact</h2>
      <p className="main-info">Send your Orders on the WhatsApp Number along with your T-Shirt Designs</p>
      
      <h4 className="title">Phone number:</h4>
      <h3 className="title">Ashish Pise</h3>
      <p>+91 8767383986 (WhatsApp)</p>
      <h3 className="title">Work hours:</h3>
      <p>Monday - Friday: 9.00 - 20.00</p>
      <p>Saturday - SUnday: 10.00 - 16.00</p>
    </div>
  </>
);

export default contact;