import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './LoginComponent.css'


export default function LoginComponent(onSignUpClick ) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const submit = (e) => {
        e.preventDefault();
        console.log('Username: ', username);
        console.log('Password: ', password);
        
        /*
        *
        * Insert Code for Authentication Here (when user hits submit)
        * 
        */

    };
    
    return (
        <div className='login-container'>
            <form className="login-form" onSubmit={submit}>
                <h2>Log In</h2>
                <label>Username</label>
                <input
                    type="username"
                    text="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
    
                <label>Password</label>
                <input
                    type="password"
                    text="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
    
                <button type="submit">Log In</button>
    
                <p>
                Don't have an account?&nbsp;<a className="next-page" href="/signup" onClick={onSignUpClick}>Sign Up</a>
                </p>
    
            </form>
        </div>
    );
    
    Login.propTypes = {
        onSignUpClick: PropTypes.func.isRequired,
    };
}
