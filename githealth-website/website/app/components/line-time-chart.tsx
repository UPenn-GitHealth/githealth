"use client";

import React from "react";
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
} from "chart.js";
import "chartjs-adapter-date-fns";
import { Line } from "react-chartjs-2";

ChartJS.register(
    Colors,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
);

export interface LineTimeChartPoint {
    x: Date;
    y: number;
}

type LineTimeChartProps = {
    title?: string;
    legend?: string;
    data?: LineTimeChartPoint[];
};

export default function LineTimeChart(props: LineTimeChartProps) {
    const options = {
        plugins: {
            title: {
                display: true,
                text: props.title ? props.title : "Untittled chart",
            },
        },
        scales: {
            x: {
                type: "time",
                time: {
                    unit: "day",
                },
            },
        },
    };

    const data = {
        datasets: [
            {
                label: props.legend ? props.legend : "Data",
                data: props.data ? props.data : [],
            },
        ],
    };
    return <Line options={options} data={data} />;
}
