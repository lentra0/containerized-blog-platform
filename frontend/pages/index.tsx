
import { useEffect, useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';
import PostList from '../components/PostList';

axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Post {
  id: number;
  title: string;
  content: string;
  author: { username: string };
  created_at: string;
  comments: any[];
  likes_count: number;
}

const Home = () => {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    axios.get<Post[]>('/api/posts')
      .then(response => setPosts(response.data))
      .catch(console.error);
  }, []);

  return (
    <Layout>
      <h1>Blog Posts</h1>
      <PostList posts={posts} />
    </Layout>
  );
};

export default Home;
