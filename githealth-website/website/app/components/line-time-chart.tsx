"use client";

import React, { useState, useEffect, useMemo } from 'react';
import {
    Chart as ChartJS,
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
    CategoryScale,
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
    filter: boolean;
    title?: string;
    legend?: string;
    data?: LineTimeChartPoint[];
};

function subtractDate(date: Date, months: number, years: number) {
    let newDate = new Date(date.getTime());
    newDate.setFullYear(newDate.getFullYear() - years);
    newDate.setMonth(newDate.getMonth() - months);
    newDate.setDate(newDate.getDate());
    return newDate;
}

export default function LineTimeChart(props: LineTimeChartProps) {
    const [filteredData, setFilteredData] = useState<LineTimeChartPoint[]>(props.data || []);

    useEffect(() => {
        setFilteredData(props.data || []);
    }, [props.data]);

    const setTimeRangeBasedOnEndDate = (months: number, years: number, end: Date) => {
        let data = props.data || [];
        if (months || years) {
            const startDate = subtractDate(end, months, years);
            data = data.filter(point =>
                new Date(point.x) >= startDate && new Date(point.x) <= end
            );
        }
        setFilteredData(data);
    };

    const setTimeRange = (months: number, years: number) => {
        const endDate = new Date();
        setTimeRangeBasedOnEndDate(months, years, endDate);
    };

    const options: ChartOptions<"line"> = useMemo(() => ({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top' as const, // Explicitly set the position to 'top'
            },
            title: {
                display: true,
                text: props.title ?? 'Chart',
            },
            tooltip: {
                callbacks: {
                    title: function(tooltipItems: { parsed: { x: string | number | Date; }; }[]) {
                        // Ensure that we're getting a valid date object
                        const date = new Date(tooltipItems[0].parsed.x);
                        return date.toLocaleString('default', { month: 'short', year: 'numeric' });
                    }
                }
            }
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
    }), [props.title, props.legend]);

    const chartData = useMemo(() => ({
        labels: filteredData.map(d => d.x),
        datasets: [{
            label: props.legend ?? 'Dataset',
            data: filteredData,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            fill: false,
        }],
    }), [filteredData, props.legend]);

    const chartContainerStyle = {
        width: '100%',
        height: '400px',
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        padding: '10px',
        borderRadius: '10px',
    };

    return (
        <div>
            <h2 className="text-center text-xl text-blue-500 font-bold my-4">{props.title ?? "Untitled Chart"}</h2>
            <div className="flex justify-center gap-2 mb-4">
                <button onClick={() => setTimeRange(1, 0)} style={{ color: 'blue' }}>1M</button>
                <button onClick={() => setTimeRange(3, 0)} style={{ color: 'blue' }}>3M</button>
                <button onClick={() => setTimeRange(6, 0)} style={{ color: 'blue' }}>6M</button>
                <button onClick={() => setTimeRange(9, 0)} style={{ color: 'blue' }}>9M</button>
                <button onClick={() => setTimeRange(0, 1)} style={{ color: 'blue' }}>1YR</button>
                <button onClick={() => setTimeRange(0, 2)} style={{ color: 'blue' }}>2YR</button>
                <button onClick={() => setTimeRange(0, 5)} style={{ color: 'blue' }}>5YR</button>
                <button onClick={() => setTimeRangeBasedOnEndDate(0, 0, new Date())} style={{ color: 'blue' }}>ALL</button>
            </div>
            <div style={chartContainerStyle}>
                <Line options={options} data={chartData} />
            </div>
        </div>
    );
}

