// app/page.tsx
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import IssueData from './issues/issues-data.client';
import CommentCountByDiscussionThreadAuthor from './discussions/comment-count-by-discussion-thread-author.client';
import CommenterDTAConnectionCountAcrossOrganizations from './discussions/commenter-dta-connection-count-across-organizations.client';

export default function Home() {
  // Render the main page along with the IssueData component
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">

      {/* The section where you include the IssueData client component */}
      <section className="my-8">
        <IssueData />
      </section>

      {/* The section where you include the CommentCountByDiscussionThreadAuthor client component */}
      <section className="my-8">
        <CommentCountByDiscussionThreadAuthor />
      </section>

      {/* Now, we add the corresponding network visualization image*/}
      <Image
        src="/discussions/discussion_dataset_network_visualization.png"
        alt="Network Visualization #1"
        width={800}
        height={600}
      />

      {/* The section where you include the CommenterDTAConnectionCountAcrossOrganizations client component */}
      <section className="my-8">
        <CommenterDTAConnectionCountAcrossOrganizations />
      </section>

      {/* Now, we add the corresponding network visualization image*/}
      <Image
        src="/discussions/commenter-dta_connection_network_across_organizations.png"
        alt="Network Visualization #2"
        width={800}
        height={600}
      />

    </main>
  );
}

// cd githealth/next.js-fastapi-example/nextjs-fastapi
// npm run dev