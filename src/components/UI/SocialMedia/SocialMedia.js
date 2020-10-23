import React from 'react';
import './SocialMedia.scss';

import fb from '../../../assets/social_media/fb.png';
import instagram from '../../../assets/social_media/instagram.png';
import whatsapp from '../../../assets/social_media/whatsapp.png';

const SocialMedia = () => (
  <div className="social-media">
    <h3 className="title">Social Media</h3>
    <div className="icons-wrapper">
      <a href="https://chat.whatsapp.com/JesFWQsHvpG1rKO3EssuU7" target="_blank" rel="noopener noreferrer"><img src={whatsapp} alt="whatsapp" /></a>
      <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer"><img src={fb} alt="facebook" /></a>
      <a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer"><img src={instagram} alt="instagram" /></a>
      
    </div>
  </div>
);

export default SocialMedia;