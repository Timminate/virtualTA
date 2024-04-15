"use client";
import Link from "next/link";
import React, { useEffect } from "react";
import {useRouter} from "next/navigation";
import axios from "axios";
import './LoginComponent.css'


export default function LoginComponent(onSignup) {
    const router = useRouter();
    const [loading, setLoading] = React.useState(false);
    const [user, setUser] = React.useState({
        email: "",
        password: "",
    })
    const onLogin = async () => {
        try {
            setLoading(true);
            const response = await axios.post("/api/users/login", user);
            console.log("Login success!")
            router.push("/");
            
        } catch (error) {
            console.log("Login failed", error.message);
            
        }finally {
            setLoading(false);
        }
    }

    
    return (
        <div className='login-container'>
            <form className="login-form">
                <h2>Log In</h2>
                <label>Username/Email</label>
                <input
                    id="username"
                    type="username"
                    value={user.username || user.email}
                    onChange={(e) => setUser({...user, email: e.target.value})}
                    placeholder="Enter your username or email address."
                    required
                />
    
                <label>Password</label>
                <input
                    id="password"
                    type="password"
                    value={user.password}
                    onChange={(e) => setUser({...user, password: e.target.value})}
                    placeholder="Enter your password"
                    required
                />
    
                <button onClick={onLogin} type="submit">Log In</button>
    
                <p>
                Don't have an account?&nbsp;<a className="next-page" href="/signup">Sign Up</a>
                </p>
    
            </form>
        </div>
    );
}
