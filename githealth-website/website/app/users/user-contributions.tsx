"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../ContributionsTable.css';

interface UserContribution {
    user: string;
    user_affiliation: string;
    issues_created: number;
    issues_commented: number;
    average_time_to_first_response_hours: number;
    average_time_to_close_hours: number;
    total_comments: number;
    total_commits: number;
    total_checks: number;
    total_files_changed: number;
    total_lines_changed: number;
}

const UserContributionsTable: React.FC = () => {
    const [contributions, setContributions] = useState<UserContribution[]>([]);
    const [sortField, setSortField] = useState<string>('issues_commented');

    useEffect(() => {
        const fetchContributions = async () => {
            const response = await axios.get<UserContribution[]>('/api/users/contributions');
            setContributions(response.data);
        };

        fetchContributions();
    }, []);

    const sortedContributions = [...contributions].sort((a, b) => {
        const key = sortField as keyof UserContribution;
        return (b[key] as number) - (a[key] as number);
    });

    return (
        <div>
            <select
                className="select-dropdown" // Add this class
                value={sortField}
                onChange={(e) => setSortField(e.target.value)}
            >
                <option value="issues_commented">Most Comments</option>
                <option value="issues_created">Most Issues Created</option>
                <option value="total_commits">Most Commits</option>
                <option value="total_files_changed">Most Files Changed</option>
                <option value="total_lines_changed">Most Lines Changed</option>
            </select>

            <div className="table-container"> {/* Add this div to wrap the table */}
                <table>
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Affiliation</th>
                            <th>Issues Created</th>
                            <th>Issues Commented</th>
                            <th>Avg Time to First Response (hrs)</th>
                            <th>Avg Time to Close (hrs)</th>
                            <th>Total Comments</th>
                            <th>Total Commits</th>
                            <th>Total Checks</th>
                            <th>Total Files Changed</th>
                            <th>Total Lines Changed</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sortedContributions.map((contribution, index) => (
                            <tr key={index}>
                                <td>{contribution.user}</td>
                                <td>{contribution.user_affiliation}</td>
                                <td>{contribution.issues_created}</td>
                                <td>{contribution.issues_commented}</td>
                                <td>{contribution.average_time_to_first_response_hours.toFixed(2)}</td>
                                <td>{contribution.average_time_to_close_hours.toFixed(2)}</td>
                                <td>{contribution.total_comments}</td>
                                <td>{contribution.total_commits}</td>
                                <td>{contribution.total_checks}</td>
                                <td>{contribution.total_files_changed}</td>
                                <td>{contribution.total_lines_changed}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UserContributionsTable;
