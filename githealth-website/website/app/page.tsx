import React from "react";
import Image from "next/image";
import IssueDataFirstResp from "./issues/issues-first-response.client";
import IssueDataClose from "./issues/issues-close.client";
import CommentCountByDiscussionThreadAuthor from "./discussions/comment-count-by-discussion-thread-author.client";
import CommenterDTAConnectionCountAcrossOrganizations from "./discussions/commenter-dta-connection-count-across-organizations.client";
import LineTimeChart from "./components/line-time-chart";
import FirstResponseMeanChart from "./issues/first-response-mean-chart";
import FirstResponseMedian from "./issues/first-response-median-chart";

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

            <FirstResponseMeanChart />
            <FirstResponseMedian />
            {/* IssueDataFirstResp and Image side by side */}
            <div className="flex my-8">
                <section
                    style={{
                        maxHeight: "600px",
                        maxWidth: "200px",
                        overflow: "auto",
                        marginRight: "16px",
                    }}
                >
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
                <section
                    style={{
                        maxHeight: "600px",
                        maxWidth: "200px",
                        overflow: "auto",
                        marginRight: "16px",
                    }}
                >
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
                <section
                    style={{
                        maxHeight: "817px",
                        overflow: "auto",
                        marginRight: "16px",
                        maxWidth: "450px",
                    }}
                >
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
                <section
                    style={{
                        maxHeight: "814px",
                        overflow: "auto",
                        marginRight: "16px",
                        maxWidth: "450px",
                    }}
                >
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
