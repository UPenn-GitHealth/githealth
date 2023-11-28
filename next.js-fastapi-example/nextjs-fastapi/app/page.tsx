// app/page.tsx
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import IssueData from './issues/issues-data.client'; 

export default function Home() {
  // Render the main page along with the IssueData component
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {/* ... (rest of your component) ... */}

      {/* The section where you include the IssueData client component */}
      <section className="my-8">
        <IssueData />
      </section>

      {/* ... (rest of your component) ... */}
    </main>
  );
}

// cd githealth/next.js-fastapi-example/nextjs-fastapi
// npm run dev