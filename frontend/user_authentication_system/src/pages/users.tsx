'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface UsersProps {}

const Users: React.FC<UsersProps> = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-gray-100 p-4">
        <h1 className="text-3xl font-bold">Users</h1>
      </header>
      <main className="container mx-auto p-4">
        {/* Page content */}
      </main>
    </div>
  );
};

export default Users;
