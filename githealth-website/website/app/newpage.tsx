// app/page.tsx
import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Welcome to GitHealth</h1>
      
      {/* Navigation links to different data categories */}
      <nav className="my-8">
        <ul>
          <li><Link href="/issues">Issues Data</Link></li>
          <li><Link href="/discussions">Discussions Data</Link></li>
        </ul>
      </nav>
    </main>
  );
}
