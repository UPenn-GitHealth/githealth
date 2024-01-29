"use client";

import React, { useState, useEffect } from "react";
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
    filter?: boolean;
    title?: string;
    legend?: string;
    data?: LineTimeChartPoint[];
};

export default function LineTimeChart(props: LineTimeChartProps) {

    const [startDate, setStartDate] = useState<Date>(new Date());
    const [endDate, setEndDate] = useState<Date>(new Date());
    const [filteredData, setFilteredData] = useState<LineTimeChartPoint[]>([]);

    const options = {
        plugins: {
            title: {
                display: true,
                text: props.title ? props.title : "Untittled chart",
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
                type: "time",
                time: {
                    unit: "month",
                },
            },
            y: {
                grid: {
                    display: false,
                },
            },
        },
    };

    const data = {
        datasets: [
            {
                label: props.legend ? props.legend : "Data",
                data: filteredData,
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1
            },
        ],
    };


    useEffect(() => {
        setFilteredData(props.data ?? [])
        props.data?.sort();
        setStartDate(props.data?.at(0)?.x ?? new Date());
        setEndDate(props.data?.at(props.data?.length - 1)?.x ?? new Date());
    }, [props.data])

    useEffect(() => {
        if (startDate && endDate) {
            const filteredData = props.data?.filter((item: LineTimeChartPoint) => {
                return item.x >= startDate && item.x <= endDate;
            });
            setFilteredData(filteredData ?? []);
        }
    }, [props.data, startDate, endDate])

    return (
        <div>

            {props.filter ?
                <>

                    <div className="flex justify-center gap-2 mb-4">
                        <input
                            type="date"
                            value={startDate.toString()}
                            onChange={(e) => setStartDate(e.target.value)}

                        />
                        <input
                            type="date"
                            value={endDate.toString()}
                            onChange={(e) => setEndDate(e.target.value)}
                        />
                    </div>
                </> : <></>}

            < div
                style={{
                    width: "75%",
                    backgroundColor: "rgba(255, 255, 255, 0.8)",
                    padding: "10px",
                    borderRadius: "10px",
                }
                }
            >
                <Line options={options} data={data} />
            </div >

        </div>
    );
}
