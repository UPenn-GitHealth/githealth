import React from 'react';
import Header from "../components/Header";
import FirstResponseMeanChart from "./first-response-mean-chart";
import FirstResponseMedian from "./first-response-median-chart";
import TimeToCloseMean from './time-to-close-mean-chart';
import TimeToCloseMedian from './time-to-close-median-chart';

const IssuesPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen">
            <Header />
            <div className="text-center p-4 bg-blue-600 text-white">
                <h2 className="text-2xl font-bold">Issues Data</h2>
                <p className="mt-2">
                    This section provides an analysis of issue response times within the Autoware community.
                </p>
                <p className="mt-2">
                    Use the date pickers to filter the data according to specific time frames.
                </p>
                <p className="mt-2">
                    This metric provides insight into the efficiency and responsiveness of the community to issues over time.
                </p>
            </div>
            <div className="w-full px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 px-4">
                    <div className="mb-8 w-full">
                        <FirstResponseMeanChart />
                    </div>
                    <div className="mb-8 w-full">
                        <FirstResponseMedian />
                    </div>
                    <div className="mb-8 w-full">
                        <TimeToCloseMean />
                    </div>
                    <div className="mb-8 w-full">
                        <TimeToCloseMedian />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default IssuesPage;