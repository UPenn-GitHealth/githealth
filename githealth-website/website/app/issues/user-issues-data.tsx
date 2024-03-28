"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../ContributionsTable.css';

interface UserIssueData {
    users: string;
    thread: number;
    thread_internal: number;
    thread_external: number;
    thread_collaboration_index: number;
    contribution: number;
    contribution_internal: number;
    contribution_external: number;
    contribution_collaboration_index: number;
}

const UserIssueDataTable: React.FC = () => {
    const [userIssueData, setUserIssueData] = useState<UserIssueData[]>([]);
    const [sortField, setSortField] = useState<string>('thread');

    useEffect(() => {
        const fetchUserIssueData = async () => {
            const response = await axios.get<UserIssueData[]>('/api/issues/user-issues-data');
            setUserIssueData(response.data);
        };

        fetchUserIssueData();
    }, []);

    const sortedUserIssueData = [...userIssueData].sort((a, b) => {
        const key = sortField as keyof UserIssueData;
        return (b[key] as number) - (a[key] as number);
    });

    return (
        <div>
            <select
                className="select-dropdown"
                value={sortField}
                onChange={(e) => setSortField(e.target.value)}
            >
                <option value="thread">Total Threads</option>
                <option value="thread_internal">Internal Threads</option>
                <option value="thread_external">External Threads</option>
                <option value="thread_collaboration_index">Thread Collaboration Index</option>
                <option value="contribution">Total Contributions</option>
                <option value="contribution_internal">Internal Contributions</option>
                <option value="contribution_external">External Contributions</option>
                <option value="contribution_collaboration_index">Contribution Collaboration Index</option>
            </select>

            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Total Threads</th>
                            <th>Internal Threads</th>
                            <th>External Threads</th>
                            <th>Thread Collaboration Index</th>
                            <th>Total Contributions</th>
                            <th>Internal Contributions</th>
                            <th>External Contributions</th>
                            <th>Contribution Collaboration Index</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedUserIssueData.map((data, index) => (
                            <tr key={index}>
                                <td>{data.users}</td>
                                <td>{data.thread}</td>
                                <td>{data.thread_internal}</td>
                                <td>{data.thread_external}</td>
                                <td>{data.thread_collaboration_index.toFixed(2)}</td>
                                <td>{data.contribution}</td>
                                <td>{data.contribution_internal}</td>
                                <td>{data.contribution_external}</td>
                                <td>{data.contribution_collaboration_index.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UserIssueDataTable;
