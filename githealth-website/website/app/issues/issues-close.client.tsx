// issues-time-to-close.client.tsx
"use client";
import React, { useState, useEffect } from 'react';

interface IssueTimeToClose {
<<<<<<< HEAD
  year: number;
  month: number;
  issues_time_to_close_hours: number;
}

const IssuesTimeToClose: React.FC = () => {
  const [timeToCloseData, setTimeToCloseData] = useState<IssueTimeToClose[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTimeToCloseData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/issues/time-to-close');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: IssueTimeToClose[] = await response.json();
        setTimeToCloseData(data);
      } catch (error: any) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchTimeToCloseData();
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
          <th>Time to Close (Hours)</th>
        </tr>
      </thead>
      <tbody>
        {timeToCloseData.map((item, index) => (
          <tr key={index}>
            <td>{item.year}</td>
            <td>{item.month}</td>
            <td>{item.issues_time_to_close_hours.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
=======
    year: number;
    month: number;
    issues_time_to_close_hours: number;
}

const IssuesTimeToClose: React.FC = () => {
    const [timeToCloseData, setTimeToCloseData] = useState<IssueTimeToClose[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchTimeToCloseData() {
            try {
                const response = await fetch('http://127.0.0.1:8000/issues/time-to-close');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data: IssueTimeToClose[] = await response.json();
                setTimeToCloseData(data);
            } catch (error: any) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        }

        fetchTimeToCloseData();
    }, []);

    if (isLoading) {
        return <div>Loading data...</div>;
    }

    if (error) {
        return <div>Error fetching data: {error}</div>;
    }

    return (
        <table className="table">
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Month</th>
                    <th>Time to Close (Hours)</th>
                </tr>
            </thead>
            <tbody>
                {timeToCloseData.map((item, index) => (
                    <tr key={index}>
                        <td>{item.year}</td>
                        <td>{item.month}</td>
                        <td>{item.issues_time_to_close_hours.toFixed(2)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
>>>>>>> 5d86f957e2057247185e05933af4b8a8ee305b31
};

export default IssuesTimeToClose;
