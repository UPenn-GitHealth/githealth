import React from 'react';
import Image from 'next/image';
import CommentCountByDiscussionThreadAuthor from './comment-count-by-discussion-thread-author.client';
import CommenterDTAConnectionCountAcrossOrganizations from './commenter-dta-connection-count-across-organizations.client';
import Header from "../components/Header";

const DiscussionsPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div>
                <h2>Discussions Data</h2>
                {/* <CommentCountByDiscussionThreadAuthor /> */} 
                {/* <CommenterDTAConnectionCountAcrossOrganizations /> */} 
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
            </div>
        </div>

        
    );
};

export default DiscussionsPage;
