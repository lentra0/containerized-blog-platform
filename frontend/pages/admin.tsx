// @ts-nocheck
import React, { useState } from 'react';
import Layout from '../components/Layout';
import axios from 'axios';

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const Admin = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');

  const handleCreate = async () => {
    try {
      await axios.post('/api/posts', { title, content });
      setMessage('Post created successfully');
      setTitle('');
      setContent('');
    } catch (err) {
      setMessage(err.response?.data.detail || 'Post creation failed');
    }
  };

  return (
    <Layout>
      <h1>Admin Panel</h1>
      <div>
        <label>Title:</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} />
      </div>
      <div>
        <label>Content:</label>
        <textarea value={content} onChange={(e) => setContent(e.target.value)} />
      </div>
      <button onClick={handleCreate}>Create Post</button>
      {message && <p>{message}</p>}
    </Layout>
  );
};

export default Admin;
