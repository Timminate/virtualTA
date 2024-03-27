import { useState } from 'react';
import styles from './SignUpComponent.css'; // Import the CSS module

export default function SignUpComponent() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [check, setCheck] = useState('');
  const [passwordMatch, setPasswordMatch] = useState(true);

  const confirmPassword = (e) => {
    setCheck(e.target.value);
    if (e.target.value !== password) {
      setPasswordMatch(false);
    } else {
      setPasswordMatch(true);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!passwordMatch) { // Logic for if passwords are not the same
      setError('Passwords do not match!');
      console.log('Email:', email);
      console.log('Username:', username);
      console.log('Password:', password);
      return;
    }
    /*
    *
    * Insert logic for Sign Up Authentication
    * 
    */
    console.log('Email:', email);
    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Confirm Password:', check);
  };

  return (
    <div className='login-container'>
      <form className='login-form' onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
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
          <label>Username:</label>
          <input
            type="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={check}
            onChange={confirmPassword}
            required
          />
        </div>
        <button type="submit">Sign Up</button>
        <div>
          <p>
            Already have an account?&nbsp;
            <a className="next-page" href="/">Log in</a>
          </p>
        </div>
      </form>
    </div>
  );
}
