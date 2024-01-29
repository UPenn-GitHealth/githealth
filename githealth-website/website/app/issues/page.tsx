import React from 'react';
import Image from 'next/image';
// import IssueDataFirstResp from './issues-first-response.client';
// import IssueDataClose from './issues-close.client';
import FirstResponseMeanChart from "./first-response-mean-chart";
import FirstResponseMedian from "./first-response-median-chart";
import Header from "../components/Header";
import TimeToCloseMedian from './time-to-close-median-chart';
import TimeToCloseMean from './time-to-close-mean-chart';

const IssuesPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div>
                <h2>Issues Data</h2>
                <FirstResponseMeanChart />
                <FirstResponseMedian />
                <TimeToCloseMean />
                <TimeToCloseMedian />

            </div>
        </div>
    );
};

export default IssuesPage;
