'use client'

import { useState } from 'react';
import styles from './styles.module.css'; // Import the CSS module

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // For demonstration, we'll just display entered email and password
    console.log('Email:', email);
    console.log('Password:', password);
  };

  return (
    <div className={styles['login-container']}> {/* Use styles.login-container */}
      <form className={styles['login-form']} onSubmit={handleSubmit}>
        <h2>Login</h2>
        {error && <p className={styles.error}>{error}</p>}
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
