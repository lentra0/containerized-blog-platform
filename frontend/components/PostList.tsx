import React from 'react';
import Link from 'next/link';

const PostList = ({ posts }) => (
  <ul>
    {posts.map((post) => (
      <li key={post.id} style={{ marginBottom: '10px' }}>
        <Link href={`/posts/${post.id}`}>
          <a>{post.title}</a>
        </Link>
      </li>
    ))}
  </ul>
);

export default PostList;
