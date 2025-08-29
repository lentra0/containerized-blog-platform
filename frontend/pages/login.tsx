// @ts-nocheck
import React, { useState } from 'react';
import Layout from '../components/Layout';
import axios from 'axios';

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const AuthPage = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    try {
      await axios.post('/api/auth/register', { username, password });
      setMessage('Registered successfully! Please login.');
      setIsRegister(false);
      setUsername('');
      setPassword('');
    } catch (err) {
      setMessage(err.response?.data.detail || 'Registration failed');
    }
  };

  const handleLogin = async () => {
    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);
      const res = await axios.post('/api/auth/login', params);
      const token = res.data.access_token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
      setMessage('Login successful!');
      setUsername('');
      setPassword('');
    } catch (err) {
      setMessage(err.response?.data.detail || 'Login failed');
    }
  };

  return (
    <Layout>
      <h1>{isRegister ? 'Register' : 'Login'}</h1>
      <div>
        <label>Username:</label>
        <input value={username} onChange={e => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      </div>
      <button onClick={isRegister ? handleRegister : handleLogin}>
        {isRegister ? 'Register' : 'Login'}
      </button>
      <button onClick={() => { setIsRegister(!isRegister); setMessage(''); }} style={{ marginLeft: '10px' }}>
        {isRegister ? 'Switch to Login' : 'Switch to Register'}
      </button>
      {message && <p>{message}</p>}
    </Layout>
  );
};

export default AuthPage;