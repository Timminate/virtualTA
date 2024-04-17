import { useState } from 'react';
import Link from "next/link";
import React, { useEffect } from "react";
import {useRouter} from "next/navigation";
import axios from "axios";
import styles from './SignUpComponent.css'; // Import the CSS module

export default function SignupPage() {
  const router = useRouter();
  const [user, setUser] = React.useState({
      email: "",
      password: "",
      username: "",
  })

  const onSignup = async (e) => {
    try {
      e.preventDefault()
      const response = await axios.post("/api/users/signup", user)
      router.push("/login")
    } catch (error) {
      console.log("Signup failed", error.message)
    }
  }

  return (
    <div className='login-container'>
      <form className='login-form'>
        <h2>Sign Up</h2>
        <div>
          <label>Email</label>
          <input 
            id="email"
            type="email"
            value={user.email}
            onChange={(e) => setUser({...user, email: e.target.value})}
            placeholder="email"
            required
            />
        </div>
        <div>
          <label>Username</label>
          <input
            id="username"
            type="username"
            value={user.username}
            onChange={(e) => setUser({...user, username: e.target.value})}
            placeholder="username"
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            id="password"
            type="password"
            value={user.password}
            onChange={(e) => setUser({...user, password: e.target.value})}
            placeholder="password"
            required
            />
        </div>
        <button onClick={onSignup} type="submit" href="/">Sign Up</button>
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
