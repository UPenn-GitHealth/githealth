<<<<<<< HEAD
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

      {/* IssueDataFirstResp and Image side by side */}
      <div className="flex my-8">
        <section style={{ maxHeight: '600px', maxWidth: '200px', overflow: 'auto', marginRight: '16px' }}>
          <IssueDataFirstResp />
        </section>
        <section>
          <Image
            src="/avg_first_resp_time_plot.png"
            alt="Average First Response Time Plot"
            width={600}
            height={400}
          />
          <Image
          src="/median_first_resp_time_plot.png"
          alt="Median First Response Time Plot"
          width={600}
          height={400}
          />
        </section>
      </div>

      {/* IssueDataFirstResp and Image side by side */}
      <div className="flex my-8">
        <section style={{ maxHeight: '600px', maxWidth: '200px', overflow: 'auto', marginRight: '16px' }}>
          <IssueDataClose />
        </section>
        <section>
          <Image
            src="/avg_close_time_plot.png"
            alt="Average Close Time Plot"
            width={600}
            height={400}
          />
          <Image
          src="/median_close_time_plot.png"
          alt="Median Close Time Plot"
          width={600}
          height={400}
          />
        </section>
      </div>

      {/* CommentCountByDiscussionThreadAuthor and Image side by side */}
      <div className="flex my-8">
        <section style={{ maxHeight: '817px', overflow: 'auto', marginRight: '16px', maxWidth: '450px' }}>
          <CommentCountByDiscussionThreadAuthor />
        </section>
        <Image
          src="/discussion_dataset_network_visualization.png"
          alt="Discussion Dataset Network Visualization"
          width={728}
          height={817}
        />
      </div>

      {/* CommenterDTAConnectionCountAcrossOrganizations and Image side by side */}
      <div className="flex my-8">
        <section style={{ maxHeight: '814px', overflow: 'auto', marginRight: '16px', maxWidth: '450px' }}>
          <CommenterDTAConnectionCountAcrossOrganizations />
        </section>
        <Image
          src="/commenter-dta_connection_network_across_organizations.png"
          alt="Commenter DTA Connection Network Across Organizations"
          width={728}
          height={814}
        />
      </div>


    </main>
  );
}
=======
import React from "react";
import Image from "next/image";
import Header from './components/Header';
import Link from 'next/link';

const HomePage = () => {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />
      {/* Welcome Section with Background Image */}
      <div className="relative text-center py-20 px-6 bg-cover bg-center" style={{ backgroundImage: 'url(/githealth_background.jpg)' }}>
        <div className="bg-opacity-50 bg-black p-10 rounded-md inline-block">
          <Image
            src="/GitHealth_Logo.jpeg"
            alt="GitHealth Logo"
            width={200}
            height={200}
            className="mb-8 inline-block"
          />
          <h1 className="text-5xl font-extrabold text-white sm:text-6xl">
            Welcome to <span className="text-blue-300">GitHealth</span>
          </h1>
          <p className="mt-4 text-xl text-gray-200 max-w-xl mx-auto">
            A platform providing insights into open-source GitHub communities. 
            Discover metrics that matter and evaluate the health of collaborative projects with ease.
          </p>
        </div>
      </div>
      <div className="bg-white py-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Explore Our Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 mt-6">
            {/* Card for Issues */}
            <div className="bg-gray-100 rounded-xl p-6 hover:shadow-lg transition duration-300 ease-in-out">
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Issues Analysis</h3>
              <p className="text-gray-600">
                Dive into issue response times, resolution rates, and more to understand community responsiveness.
              </p>
              <Link href="/issues">
                <span className="text-blue-600 hover:underline mt-4 block">View Issues Metrics</span>
              </Link>
            </div>
            {/* Card for Discussions */}
            <div className="bg-gray-100 rounded-xl p-6 hover:shadow-lg transition duration-300 ease-in-out">
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Discussions Engagement</h3>
              <p className="text-gray-600">
                Analyze discussions to gauge topic engagement and community involvement.
              </p>
              <Link href="/discussions">
                <span className="text-blue-600 hover:underline mt-4 block">View Discussions Metrics</span>
              </Link>
            </div>
            {/* Card for CDI */}
            <div className="bg-gray-100 rounded-xl p-6 hover:shadow-lg transition duration-300 ease-in-out">
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Corporate Diversity Index (In Progress)</h3>
              <p className="text-gray-600">
                Assess diversity of contributers
              </p>
              <Link href="/discussions">
                <span className="text-blue-600 hover:underline mt-4 block">View CDI</span>
              </Link>
            </div>
            {/* Card for TSDoC */}
            <div className="bg-gray-100 rounded-xl p-6 hover:shadow-lg transition duration-300 ease-in-out">
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Time Series Distribution of Contribution (In Progress)</h3>
              <p className="text-gray-600">
                Contribution should be consistent and minimally volatile
              </p>
              <Link href="/discussions">
                <span className="text-blue-600 hover:underline mt-4 block">View TSDoC</span>
              </Link>
            </div>
            {/* Card for  */}
            <div className="bg-gray-100 rounded-xl p-6 hover:shadow-lg transition duration-300 ease-in-out">
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Coming soon...</h3>
              <p className="text-gray-600">
              </p>
              {/* <Link href="/discussions">
                <span className="text-blue-600 hover:underline mt-4 block">View CDI</span>
              </Link> */}
            </div>
          </div>
        </div>
      </div>
      {/* Additional sections for the home page can be added here */}
    </div>
  );
};

export default HomePage;
>>>>>>> 5d86f957e2057247185e05933af4b8a8ee305b31
