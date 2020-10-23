 import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { filterProducts } from '../../../store/actions';
import '../Navigation.scss';

import NavigationItem from './NavigationItem';

const femaleCategories = [
   {
    category: 'men-t-shirts',
    content: 'T-Shirts',
  },
  {
    category: 'watches',
    content: 'Watches',
  },
   {
    category: 'shoes',
    content: 'Shoes',
  },
  {
    category: 'earphones',
    content: 'Earphones',
  },
 
  {
    category: 'camerastands',
    content: 'Tripod Stands',
  }
  
];

const sideNavigation = ({ filterProducts, children }) => (
  <nav className="side-navigation">
    <ul className="side-navigation-list">
      {femaleCategories.map(femaleCategory => {
        const { category, linkType, content } = femaleCategory;

        return (
          <NavigationItem
            key={category}
            clicked={() => filterProducts(category)}
            linkType={'main'}
            link={`/productlist/${category}`}>
            {content}
          </NavigationItem>
        )
      })}
      {children}
    </ul>
  </nav>
);

sideNavigation.propTypes = {
  filterProducts: PropTypes.func.isRequired
};

export default connect(null, { filterProducts })(sideNavigation);