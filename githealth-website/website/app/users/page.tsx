import React from 'react';
import Header from '../components/Header';
import UserContributionsTable from './user-contributions';
import ThreadContributionMetrics from './user-thread-contribution-metrics';

const UsersPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen">
            <Header />
            <div className="text-center p-4 bg-blue-600 text-white">
                <h2 className="text-2xl font-bold">User Contributions</h2>
                <p className="mt-2">
                    Explore the contributions of individual users to the Autoware community.
                </p>
            </div>
            <div className="w-full px-4 sm:px-6 lg:px-8">
                <div className="mb-8 w-full">
                    <UserContributionsTable />
                </div>
                {/* Insert the table of thread and contribution metrics per user here */}
                <div className='mb-8 w-full'>
                    <ThreadContributionMetrics />
                </div>
            </div>
        </div>
    );
};

export default UsersPage;
