"use client";
import React, { useState, useEffect } from 'react';

interface IssueResponseTime {
  year: number;
  month: number;
  issues_time_to_first_response_hours: number;
}

export default function IssueData() {
  const [issueData, setIssueData] = useState<IssueResponseTime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchIssueData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/issues/first-response-time');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: IssueResponseTime[] = await response.json();
        setIssueData(data);
      } catch (error: any) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchIssueData();
  }, []);

  if (isLoading) {
    return <div>Loading data...</div>;
  }

  if (error) {
    return <div>Error fetching data: {error}</div>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Year</th>
          <th>Month</th>
          <th>First Response Time (Hours)</th>
        </tr>
      </thead>
      <tbody>
        {issueData.map((issue, index) => (
          <tr key={index}>
            <td>{issue.year}</td>
            <td>{issue.month}</td>
            <td>{issue.issues_time_to_first_response_hours.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}



