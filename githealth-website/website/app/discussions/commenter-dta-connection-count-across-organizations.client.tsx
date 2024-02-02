"use client";
import React, { useState, useEffect } from 'react';

interface CommenterDTAConnectionCountAcrossOrganizations {
<<<<<<< HEAD
  commenter_organization: string
  discussion_thread_author_organization: string
  commenter_dta_connection_count: number
}

export default function CommenterDTAConnectionCountAcrossOrganizationsData() {
  const [commenterDTAConnectionCountAcrossOrganizationsData, setCommenterDTAConnectionCountAcrossOrganizationsData] = useState<CommenterDTAConnectionCountAcrossOrganizations[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCommenterDTAConnectionCountAcrossOrganizationsData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/discussions/commenter-dta-connection-count-across-organizations');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: CommenterDTAConnectionCountAcrossOrganizations[] = await response.json();
        setCommenterDTAConnectionCountAcrossOrganizationsData(data);
      } catch (error: any) {
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchCommenterDTAConnectionCountAcrossOrganizationsData();
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
          <th>Commenter Organization</th>
          <th>Discussion Thread Author Organization</th>
          <th>Commenter DTA Connection Count</th>
        </tr>
      </thead>
      <tbody>
        {commenterDTAConnectionCountAcrossOrganizationsData.map((commenterDTAConnectionCountAcrossOrganizations, index) => (
          <tr key={index}>
            <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_organization}</td>
            <td>{commenterDTAConnectionCountAcrossOrganizations.discussion_thread_author_organization}</td>
            <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_dta_connection_count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
=======
    commenter_organization: string
    discussion_thread_author_organization: string
    commenter_dta_connection_count: number
}

export default function CommenterDTAConnectionCountAcrossOrganizationsData() {
    const [commenterDTAConnectionCountAcrossOrganizationsData, setCommenterDTAConnectionCountAcrossOrganizationsData] = useState<CommenterDTAConnectionCountAcrossOrganizations[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchCommenterDTAConnectionCountAcrossOrganizationsData() {
            try {
                const response = await fetch('http://127.0.0.1:8000/discussions/commenter-dta-connection-count-across-organizations');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data: CommenterDTAConnectionCountAcrossOrganizations[] = await response.json();
                setCommenterDTAConnectionCountAcrossOrganizationsData(data);
            } catch (error: any) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        }

        fetchCommenterDTAConnectionCountAcrossOrganizationsData();
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
                    <th>Commenter Organization</th>
                    <th>Discussion Thread Author Organization</th>
                    <th>Commenter DTA Connection Count</th>
                </tr>
            </thead>
            <tbody>
                {commenterDTAConnectionCountAcrossOrganizationsData.map((commenterDTAConnectionCountAcrossOrganizations, index) => (
                    <tr key={index}>
                        <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_organization}</td>
                        <td>{commenterDTAConnectionCountAcrossOrganizations.discussion_thread_author_organization}</td>
                        <td>{commenterDTAConnectionCountAcrossOrganizations.commenter_dta_connection_count}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
>>>>>>> 5d86f957e2057247185e05933af4b8a8ee305b31
