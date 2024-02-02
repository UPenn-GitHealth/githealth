import React from "react";
import Link from 'next/link';
import Header from '../components/Header';

export default function Metrics() {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <main className="flex-grow flex flex-col items-center justify-center">
              <div className="w-full max-w-4xl p-10 space-y-8">
                {/* Centered grid of navigation links */}
                <div className="w-full max-w-2xl grid grid-cols-2 gap-10 p-10">
                    <Link href="/issues">
                        <div className="flex flex-col items-center justify-center h-40 bg-white rounded-lg shadow-md cursor-pointer hover:bg-blue-100 transition duration-300">
                            <span className="text-lg font-semibold text-blue-600">Issues</span>
                            <span className="text-sm text-gray-600">Interact with issues data</span>
                        </div>
                    </Link>
                    <Link href="/discussions">
                        <div className="flex flex-col items-center justify-center h-40 bg-white rounded-lg shadow-md cursor-pointer hover:bg-blue-100 transition duration-300">
                            <span className="text-lg font-semibold text-blue-600">Discussions</span>
                            <span className="text-sm text-gray-600">View discussions metrics</span>
                        </div>
                    </Link>
                    {/* Add more grid items as needed */}
                </div>
              </div>
            </main>
        </div>
    );
}
