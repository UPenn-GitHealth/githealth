"use client";

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale,
    TimeSeriesScale
  } from 'chart.js';
  import 'chartjs-adapter-date-fns';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale,
    TimeSeriesScale
  );

// Interface for the response data
interface IssueResponseTime {
    date: string;
    issues_time_to_first_response_hours: number;
}

// Dynamically import Chart.js
const Chart = dynamic(() => import('react-chartjs-2').then((mod) => mod.Line), { ssr: false });

const FirstResponseMeanChart = () => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    // Initialize chartData with the structure expected by Chart.js
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Mean First Response Time (Hours)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
        ]
    });
    // Function to fetch data
    const fetchData = async () => {
        try {
            const response = await fetch(`/api/issues/first-response-time/mean?start_date=${startDate}&end_date=${endDate}`);
            const rawData: IssueResponseTime[] = await response.json();

            // Filter and process the data
            const filteredData = rawData.filter((item: IssueResponseTime) => {
                const itemDate = new Date(item.date);
                const start = startDate ? new Date(startDate) : new Date('1970-01-01');
                const end = endDate ? new Date(endDate) : new Date();
                return itemDate >= start && itemDate <= end;
            });

            const labels = filteredData.map((item: IssueResponseTime) => item.date.substring(0, 10));
            const data = filteredData.map((item: IssueResponseTime) => item.issues_time_to_first_response_hours);

            setChartData({
                labels,
                datasets: [{
                    label: 'Mean First Response Time (Hours)',
                    data: data,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    // Fetch data when dates change
    useEffect(() => {
        if (startDate && endDate) {
            fetchData();
        }
    }, [startDate, endDate]);

    return (
        <div>
            <h2 className="text-center text-blue-500 text-xl font-bold my-4">First Response Mean Time</h2>
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
            {chartData && <Chart data={chartData} options={{ responsive: true }} />}
        </div>
    );
};

export default FirstResponseMeanChart;
