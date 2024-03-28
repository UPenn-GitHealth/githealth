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
    discussion_thread_author_id: string
    discussion_comment_author: string
    discussion_comment_author_affiliation: number
    number_of_comments_across_DTA_threads: number
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
                                    <th className='text-center'>Discussion Thread Author (DTA)</th>
                                    <th className='text-center'>Discussion Comment Author</th>
                                    <th className='text-center'>Discussion Comment Author Affiliation</th>
                                    <th className='text-center'>Number of Comments Across DTA Threads </th>
                                </tr>
                            </thead>
                            <tbody>
                                {commentCountByDiscussionThreadAuthorData.map((commentCountByDiscussionThreadAuthor, index) => (
                                    <tr key={index}>
                                        <td className='text-center'>{commentCountByDiscussionThreadAuthor.discussion_thread_author_id}</td>
                                        <td className='text-center'>{commentCountByDiscussionThreadAuthor.discussion_comment_author}</td>
                                        <td className='text-center'>{commentCountByDiscussionThreadAuthor.discussion_comment_author_affiliation}</td>
                                        <td className='text-center'>{commentCountByDiscussionThreadAuthor.number_of_comments_across_DTA_threads}</td>
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
