import React from 'react';
import Image from 'next/image';
import IssueDataFirstResp from './issues/issues-first-response.client';
import IssueDataClose from './issues/issues-close.client';
import CommentCountByDiscussionThreadAuthor from './discussions/comment-count-by-discussion-thread-author.client';
import CommenterDTAConnectionCountAcrossOrganizations from './discussions/commenter-dta-connection-count-across-organizations.client';

export default function Home() {
  
  return (
    <main className="flex flex-col min-h-screen justify-between p-24">
      
      {/* Header */}
      <header className="w-full flex justify-start items-center">
        <Image
          src="/GitHealth_Logo.jpeg"
          alt="GitHealth Logo"
          width={128} 
          height={128} 
          layout="intrinsic"
        />
        <h1 className="text-xl font-bold ml-8">Welcome to GitHealth!</h1>
      </header>


      {/* IssueData client component */}
      <section className="my-8" style={{ maxHeight: '350px', maxWidth: '200px', overflow: 'auto' }}>
        <IssueDataFirstResp />
      </section>
      <section className="my-8" style={{ maxHeight: '350px', maxWidth: '200px', overflow: 'auto' }}>
        <IssueDataClose />
      </section>

      {/* Average First Response Time Plot */}
      <Image
        src="/avg_first_resp_time_plot.png"
        alt="Average First Response Time Plot"
        width={1200/2}
        height={800/2}
      />
      {/* Median First Response Time Plot */}
      <Image
        src="/median_first_resp_time_plot.png"
        alt="Median First Response Time Plot"
        width={1200/2}
        height={800/2}
      />
      {/* Average Close Time Plot */}
      <Image
        src="/avg_close_time_plot.png"
        alt="Average Close Time Plot"
        width={1200/2}
        height={800/2}
      />
      {/* Median Close Time Plot */}
      <Image
        src="/median_close_time_plot.png"
        alt="Median Close Time Plot"
        width={1200/2}
        height={800/2}
      />

      <section className="my-8" style={{ maxHeight: '350px', maxWidth: '500px', overflow: 'auto' }}>
        <CommentCountByDiscussionThreadAuthor />
      </section>

      <section className="my-8" style={{ maxHeight: '350px', maxWidth: '500px', overflow: 'auto' }}>
        <CommenterDTAConnectionCountAcrossOrganizations />
      </section>

      {/* Commenter DTA Connection Network Across Organizations */}
      <Image
        src="/commenter-dta_connection_network_across_organizations.png"
        alt="Commenter DTA Connection Network Across Organizations"
        width={1415/2.5}
        height={1582/2.5}
      />
      {/* Discussion Dataset Network Visualization */}
      <Image
        src="/discussion_dataset_network_visualization.png"
        alt="Discussion Dataset Network Visualization"
        width={1820/2.5}
        height={2042/2.5}
      />

    </main>
  );
}
