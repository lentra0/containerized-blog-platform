// @ts-nocheck
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import Layout from '../../components/Layout';

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const PostPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [post, setPost] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    axios.get(`/api/posts/${id}`)
      .then(res => setPost(res.data))
      .catch(() => setError('Post not found'));
  }, [id]);

  if (error) {
    return (
      <Layout>
        <h1>{error}</h1>
      </Layout>
    );
  }

  if (!post) {
    return (
      <Layout>
        <p>Loading...</p>
      </Layout>
    );
  }

  return (
    <Layout>
      <h1>{post.title}</h1>
      <p>By {post.author.username} on {new Date(post.created_at).toLocaleString()}</p>
      <div>{post.content}</div>
      <p>Likes: {post.likes_count}</p>
      <h2>Comments</h2>
      <ul>
        {post.comments.map(c => (
          <li key={c.id} style={{ marginBottom: '1em' }}>
            <p>{c.content}</p>
            <p><em>By {c.author?.username || 'Anonymous'} on {new Date(c.created_at).toLocaleString()}</em></p>
          </li>
        ))}
      </ul>
    </Layout>
  );
};

export default PostPage; 