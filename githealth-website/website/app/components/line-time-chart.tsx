"use client";

import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    Colors,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    Colors,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

type LineTimeChartProps = {
    title?: string;
    legend: string;
    data?: { x: Date, y: number }[]
}

export default function LineTimeChart(props: LineTimeChartProps) {
    const options = {
        plugins: {
            title: {
                display: true,
                text: props.title ? props.title : "Untittled chart"
            }
        },
        scales: {
            x: {
                type: "time",
                time: {
                    unit: "day"
                }
            }
        }
    };

    // TODO: Remove dummy data
    const default_dataset = [{ x: new Date("2069-04-20"), y: 5 },
    { x: new Date("2069-06-09"), y: 2 }
    ];

    const data = {
        datasets: [{
            data: props.data ? props.data : default_dataset
        }]
    }
    return <Line options={options} data={data} />
}
