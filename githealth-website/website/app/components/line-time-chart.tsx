"use client";

import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    Colors,
    CategoryScale,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ChartOptions,
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
    filter?: boolean;
    title?: string;
    legend?: string;
    data?: LineTimeChartPoint[];
};

export default function LineTimeChart(props: LineTimeChartProps) {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [filteredData, setFilteredData] = useState<LineTimeChartPoint[]>([]);

    useEffect(() => {
        if (props.data) {
            let data = props.data;
            // If startDate is set, filter the data to include points after the startDate
            if (startDate) {
                data = data.filter((point) => new Date(point.x) >= new Date(startDate));
            }
            // If endDate is set, filter the data to include points before the endDate
            if (endDate) {
                data = data.filter((point) => new Date(point.x) <= new Date(endDate));
            }
            setFilteredData(data);
        }
    }, [props.data, startDate, endDate]);

    const options: ChartOptions<"line"> = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: props.title ?? 'Chart',
            },
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'MMM yyyy'
                    }
                },
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                title: {
                    display: true,
                    text: props.legend ?? 'Value'
                }
            }
        }
    };

    const chartData = {
        labels: filteredData.map(d => d.x),
        datasets: [{
            label: props.legend ?? 'Dataset',
            data: filteredData.map(d => ({ x: d.x, y: d.y })),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            fill: false,
        }]
    };

    // Define a style object for the chart container
    const chartContainerStyle = {
        width: '100%', // Use 100% to make the chart responsive
        height: '400px', // Define a fixed height or use vh for viewport height
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        padding: '10px',
        borderRadius: '10px',
    };

    return (
        <div>
            <h2 className="text-center text-xl text-blue-500 font-bold my-4">{props.title ?? "Untitled Chart"}</h2>
            {props.filter && (
                <div className="flex justify-center gap-2 mb-4">
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                    />
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                    />
                </div>
            )}
            <div style={chartContainerStyle}>
                <Line options={options} data={chartData} /> {/* Use chartData instead of data */}
            </div>
        </div>
    );
}
