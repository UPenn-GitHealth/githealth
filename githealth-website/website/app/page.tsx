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
          src="/GitHealth Logo.jpeg"
          alt="GitHealth Logo"
          width={700} 
          height={700} 
          layout="intrinsic"
        />
        <h1 className="text-xl font-bold ml-8">Welcome to GitHealth!</h1>
      </header>

      {/* IssueData client components */}
      <section className="my-8">
        <IssueDataFirstResp />
      </section>
      <section className="my-8">
        <IssueDataClose />
      </section>

      {/* Average First Response Time Plot */}
      <Image
        src="/avg_first_resp_time_plot.png"
        alt="Average First Response Time Plot"
        width={1200}
        height={800}
      />
      {/* Median First Response Time Plot */}
      <Image
        src="/median_first_resp_time_plot.png"
        alt="Median First Response Time Plot"
        width={1200}
        height={800}
      />
      {/* Average Close Time Plot */}
      <Image
        src="/avg_close_time_plot.png"
        alt="Average Close Time Plot"
        width={1200}
        height={800}
      />
      {/* Median Close Time Plot */}
      <Image
        src="/median_close_time_plot.png"
        alt="Median Close Time Plot"
        width={1200}
        height={800}
      />

      <section className="my-8">
        <CommentCountByDiscussionThreadAuthor />
      </section>

      <section className="my-8">
        <CommenterDTAConnectionCountAcrossOrganizations />
      </section>

      {/* Commenter DTA Connection Network Across Organizations */}
      <Image
        src="/commenter-dta_connection_network_across_organizations.png"
        alt="Commenter DTA Connection Network Across Organizations"
        width={1415}
        height={1582}
      />
      {/* Discussion Dataset Network Visualization */}
      <Image
        src="/discussion_dataset_network_visualization.png"
        alt="Discussion Dataset Network Visualization"
        width={1820}
        height={2042}
      />

    </main>
  );
}
