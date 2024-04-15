'use client'

import { useState } from 'react';
import SignUpComponent from '../../components/SignUpComponent/SignUpComponent';
import styles from './styles.module.css'; // Import the CSS module

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [check, setCheck] = useState('');
  const [passwordMatch, setPasswordMatch] = useState(true);

  const confirmPassword = (e) => {
    setCheck(e.target.value);
    if(e.target.value !== password) {
      setPasswordMatch(false);
    } else {
      setPasswordMatch(true);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if(!passwordMatch) {
      setError('Passwords do not match!');
      console.log('Email:', email);
      console.log('Username:', username);
      console.log('Password:', password);
      return;
    }
    // For demonstration, we'll just display entered email and password
      console.log('Email:', email);
      console.log('Username:', username);
      console.log('Password:', password);
      console.log('Confirm Password:', check);
  };

  return (
    <div>
      <SignUpComponent/>
    </div>
    
  );
}
