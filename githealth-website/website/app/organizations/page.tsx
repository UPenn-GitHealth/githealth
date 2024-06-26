import React from 'react';
import Header from '../components/Header';
import OrganizationContributionsTable from './org-contributions';

const OrganizationsPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen">
            <Header />
            <div className="text-center p-4 bg-blue-600 text-white">
                <h2 className="text-2xl font-bold">Organization Contributions</h2>
                <p className="mt-2">
                    Review the contributions made by organizations to the Autoware community.
                </p>
            </div>
            <div className="w-full px-4 sm:px-6 lg:px-8">
                <div className="mb-8 w-full">
                    <OrganizationContributionsTable />
                </div>
            </div>
        </div>
    );
};

export default OrganizationsPage;
