 import React, { Component } from 'react';
import './HomePage.scss';
import { connect } from 'react-redux';
import * as actions from '../../store/actions';
import PropTypes from 'prop-types';

import Modal from '../../components/UI/Modal/Modal';
import Button from '../../components/UI/Button/Button';
import ScrollToTopOnMount from '../../shared/ScrollToTopOnMount';


import slideOne from '../../assets/home_page/t_s-4400453.jpg';
import slideTwo  from '../../assets/home_page/t_s-4400454.jpg';
import slideThree from '../../assets/home_page/t_s-4400457.jpg';
import slideFour from '../../assets/home_page/t_s-4400458.jpg';
import slideFive from '../../assets/home_page/t_s-4400461.jpg';


const slides = [];
slides.push(slideFive,slideThree, slideFour, slideOne,slideTwo);

class HomePage extends Component {
  closeModal = () => {
    this.props.purchaseInit();
    this.props.closeModal();
  };

  render() {
    return (
      <>
        <ScrollToTopOnMount />
        <Modal
          modalType="small"
          showModal={this.props.purchased}
          showBackdrop={this.props.purchased}
          closeModal={this.closeModal}>
          <p>Order completed successfully.</p>
          <Button clicked={this.closeModal} btnType="dark">Got it</Button>
        </Modal>
        <div className="home-container">
          <div className="showcase">
            <h3 className="main-title">Customised T-Shirts for every Mood.</h3>
            <p className="main-info">Design your own T-Shirts</p>
          </div>
          
          <div className="slider">
            {slides.map(slide => (
              <div key={slide} style={{ backgroundImage: `url('${slide}')` }} className="slide">
                <h3 className="title">New Collection</h3>
                <h3 className="subtitle">Get Customised    T-Shirt Designs</h3>
              </div>
            ))}
          </div>
        </div>
      </>
    )
  }
};

HomePage.propTypes = {
  purchased: PropTypes.bool.isRequired,
  purchaseInit: PropTypes.func.isRequired,
  closeModal: PropTypes.func.isRequired
};

const mapStateToProps = state => {
  return {
    purchased: state.order.purchased
  };
};

const mapDispatchToProps = dispatch => {
  return {
    purchaseInit: () => dispatch(actions.purchaseInit()),
    closeModal: () => dispatch(actions.closeModal())
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(HomePage);