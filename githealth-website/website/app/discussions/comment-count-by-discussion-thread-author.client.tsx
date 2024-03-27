"use client";
import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';
import Bokeh from 'bokehjs';

// Extend the Window interface to include Bokeh
declare global {
    interface Window {
        Bokeh: any;
    }
}

interface CommentCountByDiscussionThreadAuthor {
    discussion_thread_author: string
    comment_author: string
    comment_count: number
    normalized_comment_count: number
}


export default function CommentCountByDiscussionThreadAuthor() {
    const [commentCountByDiscussionThreadAuthorData, setCommentCountByDiscussionThreadAuthorData] = useState<CommentCountByDiscussionThreadAuthor[]>([]);

    // const [bokehPlot, setBokehPlot] = useState<BokehPlotData>({ div: '' });
    // const [isLoading, setIsLoading] = useState(true);
    // const [error, setError] = useState<string | null>(null);

    // const [plotData, setPlotData] = useState<BokehPlotData>();

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
            fetch('http://127.0.0.1:8000/discussions/comment-count-by-discussion-thread-author')
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    const plotDiv = document.getElementById("commenter_dta_connection_network");
                    if (plotDiv) {
                        plotDiv.innerHTML = ''; // Clear any existing content
                    }
                    window.Bokeh.embed.embed_item(data.plot_json, "commenter_dta_connection_network");

                    if (data.response_list) {
                        setCommentCountByDiscussionThreadAuthorData(data.response_list);
                    }
                })
                .catch((error) => console.error("Error fetching Bokeh plot data:", error));
        };

        ensureBokehIsLoaded();
    }, []);

    return (
        <div>
            <Head>
                <link rel="stylesheet" href="https://cdn.bokeh.org/bokeh/release/bokeh-3.3.1.min.css" />
            </Head>
            <div className='box-border h-360 w-90 p-4 border-4'>
                <div className="flex flex-row justify-around items-center">
                    <div id="commenter_dta_connection_network"></div>
                        <div className='max-h-[500px] overflow-y-auto'>
                        <table className="border border-gray-800 bg-gray-200 text-black">
                            <thead>
                                <tr>
                                    <th>Discussion Thread Author</th>
                                    <th>Comment Author</th>
                                    <th>Comment Count</th>
                                    <th>Normalized Comment Count</th>
                                </tr>
                            </thead>
                            <tbody>
                                {commentCountByDiscussionThreadAuthorData.map((commentCountByDiscussionThreadAuthor, index) => (
                                    <tr key={index}>
                                        <td>{commentCountByDiscussionThreadAuthor.discussion_thread_author}</td>
                                        <td>{commentCountByDiscussionThreadAuthor.comment_author}</td>
                                        <td>{commentCountByDiscussionThreadAuthor.comment_count}</td>
                                        <td>{commentCountByDiscussionThreadAuthor.normalized_comment_count.toFixed(5)}</td>
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
