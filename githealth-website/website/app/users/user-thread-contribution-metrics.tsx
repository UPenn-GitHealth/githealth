"use client";

import React, { useState, useEffect } from 'react';
import Head from 'next/head';

// Extend the Window interface to include Bokeh
declare global {
    interface Window {
        Bokeh: any;
    }
}

export default function ThreadContributionMetrics() {
    useEffect(() => {
        const ensureBokehIsLoaded = () => {
            console.log('ensureBokehIsLoaded')
            if (window.Bokeh) {
                console.log('Bokeh is already loaded')
                fetchAndEmbedPlot();
            } else {
                console.log('Bokeh is not loaded yet')
                const script = document.createElement('script');
                script.src = 'https://cdn.bokeh.org/bokeh/release/bokeh-3.3.1.min.js';
                script.onload = fetchAndEmbedPlot;
                document.head.appendChild(script);
            }
        };

        const fetchAndEmbedPlot = () => {
            console.log('fetchAndEmbedPlot')
            fetch('api/users/thread-contribution-metrics')
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    const plotDiv = document.getElementById("thread_contribution_metrics");
                    console.log(plotDiv); 
                    if (plotDiv !== null) {
                        plotDiv.innerHTML = ""; // Clear any existing content
                    }
                    window.Bokeh.embed.embed_item(data.plot_json, "thread_contribution_metrics");

                    // if (data.response_list) {
                    //     setCommentCountByDiscussionThreadAuthorData(data.response_list);
                    // }
                })
                .catch((error) => console.error("Error fetching Bokeh plot data:", error));
        };

        ensureBokehIsLoaded();
    }, []);

    return (
        <div className="flex justify-center">
            <Head>
                <link rel="stylesheet" href="https://cdn.bokeh.org/bokeh/release/bokeh-3.3.1.min.css" />
            </Head>
            <div id="thread_contribution_metrics"></div>
        </div>
    );
};
