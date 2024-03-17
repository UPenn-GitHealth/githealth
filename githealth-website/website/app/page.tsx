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
          <h1 className="text-5xl font-extrabold text-white sm:text-6xl">
            Welcome to <span className="text-blue-300">GitHealth</span>
          </h1>
          <p className="mt-4 text-xl text-gray-200 max-w-xl mx-auto">
            Easily evaluate the health of open-source GitHub communities with insightful metrics.
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
          </div>
        </div>
      </div>
      {/* Additional sections for the home page can be added here */}
    </div>
  );
};

export default HomePage;
