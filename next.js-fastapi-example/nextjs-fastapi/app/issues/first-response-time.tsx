import React, { useState, useEffect } from 'react';

const IssuesFirstResponseTime = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/issues/first-response-time'); // Should be corresponding FastAPI endpoint
        if (!response.ok) throw new Error('Network response was not ok.');
        const data = await response.json();
        setData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Issues First Response Time</h1>
      <table>
        <thead>
          <tr>
            <th>Year</th>
            <th>Month</th>
            <th>Average First Response Time (Hours)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.year}</td>
              <td>{item.month}</td>
              <td>{item.issues_time_to_first_response_hours.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default IssuesFirstResponseTime;
