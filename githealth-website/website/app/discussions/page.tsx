import React from 'react';
import Image from 'next/image';
import CommentCountByDiscussionThreadAuthor from './comment-count-by-discussion-thread-author.client';
import CommenterDTAConnectionCountAcrossOrganizations from './commenter-dta-connection-count-across-organizations.client';
import Header from "../components/Header";

const DiscussionsPage = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div className="text-center p-4 bg-blue-600 text-white">
                <h2 className="text-2xl font-bold">Discussions Data</h2>
                <p className="mt-2">
                    This section visualizes discussions data within the Autoware community.
                </p>
                <p className="mt-2">
                    The bokeh graphs are interactive. Hover over a node to see connections.
                </p>
                <p className="mt-2">
                    This metric shows how people collaborate with each other across organizational boundaries.
                </p>
            </div>
            <div>
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
