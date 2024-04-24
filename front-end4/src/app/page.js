'use client'

import { useState } from 'react';
import LoginComponent from '../components/LoginComponent/LoginComponent';
import styles from './page.module.css'; // Import the CSS module

export default function App() {

  const handleClick = () => {
    console.log("TESTING");
  }


  return (
    <div>
      <LoginComponent onSignUpClick={handleClick}/>
    </div>
  );
}
