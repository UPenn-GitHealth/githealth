"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';

// Extend the Window interface to include Bokeh
declare global {
    interface Window {
        Bokeh: any;
    }
}

interface CommenterDTAConnectionCountAcrossOrganizations {
    commenter_organization: string
    discussion_thread_author_organization: string
    commenter_dta_connection_count: number
}

export default function CommenterDTAConnectionCountAcrossOrganizationsData() {
    const [commenterDTAConnectionCountAcrossOrganizationsData, setCommenterDTAConnectionCountAcrossOrganizationsData] = useState<CommenterDTAConnectionCountAcrossOrganizations[]>([]);
    // const [isLoading, setIsLoading] = useState(true);
    // const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const ensureBokehIsLoaded = () => {
            if (window.Bokeh) {
                fetchAndEmbedPlot();
            } else {
                const script = document.createElement('script');
                script.src = 'https://cdn.bokeh.org/bokeh/release/bokeh-3.3.1.min.js';
                script.onload = fetchAndEmbedPlot;
                document.head.appendChild(script);
            }
        };

        const fetchAndEmbedPlot = () => {
            fetch('/api/discussions/commenter-dta-connection-count-across-organizations')
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    const plotDiv = document.getElementById("commenter_dta_connection_count_across_orgs");
                    if (plotDiv) {
                        plotDiv.innerHTML = ''; // Clear any existing content
                    }
                    window.Bokeh.embed.embed_item(data.plot_json, "commenter_dta_connection_count_across_orgs");

                    if (data.response_list) {
                        setCommenterDTAConnectionCountAcrossOrganizationsData(data.response_list);
                    }
                })
                .catch((error) => console.error("Error fetching Bokeh plot data:", error));
        };

        ensureBokehIsLoaded();
    }, []);


    // useEffect(() => {
    //     async function fetchCommenterDTAConnectionCountAcrossOrganizationsData() {
    //         try {
    //             const response = await fetch('http://127.0.0.1:8000/discussions/commenter-dta-connection-count-across-organizations');
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }
    //             const data: CommenterDTAConnectionCountAcrossOrganizations[] = await response.json();
    //             setCommenterDTAConnectionCountAcrossOrganizationsData(data);
    //         } catch (error: any) {
    //             setError(error.message);
    //         } finally {
    //             setIsLoading(false);
    //         }
    //     }

    //     fetchCommenterDTAConnectionCountAcrossOrganizationsData();
    // }, []);

    // if (isLoading) {
    //     return <div>Loading data...</div>;
    // }

    // if (error) {
    //     return <div>Error fetching data: {error}</div>;
    // }

    return (
        <div>
            <Head>
                <link rel="stylesheet" href="https://cdn.bokeh.org/bokeh/release/bokeh-3.3.1.min.css" />
            </Head>
            <div className='box-border h-360 w-90 p-4 border-4'>
                <div className="flex flex-row justify-around items-center">
                    <div id="commenter_dta_connection_count_across_orgs"></div>
                    <div className='max-h-[500px] overflow-y-auto'>
                        <table className="border border-gray-800 bg-gray-200 text-black">
                            <thead>
                                <tr>
                                    <th>Commenter Organization</th>
                                    <th>Discussion Thread Author Organization</th>
                                    <th>Commenter DTA Connection Count</th>
                                </tr>
                            </thead>
                            <tbody>
                                {commenterDTAConnectionCountAcrossOrganizationsData.map((commenterDTAConnectionCountAcrossOrganizations, index) => (
                                    <tr key={index}>
                                        <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_organization}</td>
                                        <td>{commenterDTAConnectionCountAcrossOrganizations.discussion_thread_author_organization}</td>
                                        <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_dta_connection_count}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}
