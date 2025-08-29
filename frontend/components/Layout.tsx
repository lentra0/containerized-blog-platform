// @ts-nocheck
import React, { ReactNode, useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';

interface LayoutProps {
  children: ReactNode;
}

// Set API base URL
axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const Layout = ({ children }: LayoutProps) => {
  const [username, setUsername] = useState('Anonymous');
  useEffect(() => {
    axios.get('/api/auth/me')
      .then(res => setUsername(res.data.username))
      .catch(() => setUsername('Anonymous'));
  }, []);

  return (
    <>
      <Head>
        <title>Cloud Blog Platform</title>
      </Head>
      <nav style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <Link href="/">
            <a style={{ marginRight: '10px' }}>Home</a>
          </Link>
          <Link href="/login">
            <a style={{ marginRight: '10px' }}>Login</a>
          </Link>
          <Link href="/admin">
            <a>Admin</a>
          </Link>
        </div>
        <div>
          Logged in as: <strong>{username}</strong>
        </div>
      </nav>
      <main>{children}</main>
    </>
  );
};

export default Layout;