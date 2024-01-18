"use client";
import React, { useState, useEffect } from 'react';

interface CommentCountByDiscussionThreadAuthor {
    discussion_thread_author: string
    comment_author: string
    comment_count: number
    normalized_comment_count: number
}

export default function CommentCountByDiscussionThreadAuthor() {
    const [commentCountByDiscussionThreadAuthorData, setCommentCountByDiscussionThreadAuthorData] = useState<CommentCountByDiscussionThreadAuthor[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchCommentCountByDiscussionThreadAuthorData() {
            try {
                const response = await fetch('http://127.0.0.1:8000/discussions/comment-count-by-discussion-thread-author');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data: CommentCountByDiscussionThreadAuthor[] = await response.json();
                setCommentCountByDiscussionThreadAuthorData(data);
            } catch (error: any) {
                setError(error.message);
            } finally {
                setIsLoading(false);
            }
        }

        fetchCommentCountByDiscussionThreadAuthorData();
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
                    <th>Discussion Thread Author</th>
                    <th>Comment Author</th>
                    <th>Comment Count</th>
                    <th>Normalized Comment Count</th>
                </tr>
            </thead>
            <tbody>
                {commentCountByDiscussionThreadAuthorData.map((commentCountByDiscussionThreadAuthor, index) => (
                    <tr key={index}>
                        <td>{commentCountByDiscussionThreadAuthor.discussion_thread_author}</td>
                        <td>{commentCountByDiscussionThreadAuthor.comment_author}</td>
                        <td>{commentCountByDiscussionThreadAuthor.comment_count}</td>
                        <td>{commentCountByDiscussionThreadAuthor.normalized_comment_count.toFixed(5)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
