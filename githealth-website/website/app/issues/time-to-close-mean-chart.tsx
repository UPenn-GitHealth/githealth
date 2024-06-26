"use client";

import React, { useState, useEffect } from "react";
import LineTimeChart, {
    LineTimeChartPoint,
} from "../components/line-time-chart";

export default function TimeToCloseMean() {
    const [issueData, setIssueData] = useState<LineTimeChartPoint[]>([]);

    interface IssueResponseTime {
        date: Date;
        issues_time_to_first_response_hours: number;
    }

    useEffect(() => {
        async function fetchIssueData() {
            fetch("/api/issues/close-time/mean")
                .then((res) => res.json())
                .then((data) => {
                    // @ts-ignore
                    data.forEach((element) => {
                        element.x = element.date;
                        element.y = element.issues_time_to_close_hours;
                        delete element.date;
                        delete element.issues_time_to_close_hours;
                    });
                    setIssueData(data);
                });
        }

        fetchIssueData();
    }, []);
    return (
        <LineTimeChart
            filter={true}
            title="Mean Time to Close Issue"
            legend="Mean Time to Close Issue (hours)"
            data={issueData}
        />
    );
}
