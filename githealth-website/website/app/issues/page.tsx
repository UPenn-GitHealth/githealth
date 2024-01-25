import React from 'react';
import Image from 'next/image';
import IssueDataFirstResp from './issues-first-response.client';
import IssueDataClose from './issues-close.client';
import FirstResponseMeanChart from "./first-response-mean-chart";
import FirstResponseMedian from "./first-response-median-chart";
import Header from "../components/Header";

const IssuesPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div>
                <h2>Issues Data</h2>
                <FirstResponseMeanChart />
                <FirstResponseMedian />

                {/* <IssueDataFirstResp /> */}
                {/* <IssueDataClose /> */}

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
            </div>
        </div>
    );
};

export default IssuesPage;
