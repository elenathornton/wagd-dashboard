import { useNavigate, useLocation } from 'react-router-dom';
import React from 'react';

export const withRouter = (Component) => {
  const Wrapper = (props) => {
    const navigate = useNavigate();
    const location = useLocation();
    
    return (
      <Component
        navigate={navigate}
        location={location}
        {...props}
        />
    );
  };
  
  return Wrapper;
};