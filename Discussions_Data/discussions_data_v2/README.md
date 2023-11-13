## Final GitHub Discussion Data : 

| Column Name                        | Description                                                                                                                                                                     |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `discussion_title`                  | Title of the discussion thread. Each row represents a discussion thread, and this column holds the title for each thread                                                        |
| `discussion_thread_id`              | Unique ID assigned to each discussion thread. This ID helps in uniquely identifying and tracking each discussion thread.                                                          |
| `discussion_thread_created_at`      | Timestamp indicating when the discussion thread was created.                                                                                                                      |
| `discussion_thread_author_id`       | User ID of the creator of the discussion thread.                                                                                                                                  |
| `discussion_thread_comment_count`   | Number of comments in the discussion thread. If there are no comments, it would be 0.                                                                                           |
| `discussion_answered_or_unanswered` | Indicates whether the discussion thread is answered or unanswered. If `discussion_thread_comment_count` is 0, it is considered unanswered.                                      |
| `discussion_comment_id`             | Unique ID assigned to each comment in the discussion thread. If there are no comments (i.e., `discussion_thread_comment_count` is 0), this field would be NaN.                 |
| `discussion_parent_comment_id`      | Records the comment ID for each sub-comment. If a comment is a top-level comment, this field would be NaN.                                                                      |
| `discussion_comment_created_at`     | Timestamp indicating when a comment or reply was created.                                                                                                                        |
| `discussion_comment_author`         | User ID of the author who made the comment or reply.                                                                                                                              |
| `discussion_comment_text`           | The text of the comment or reply.                                                                                                                                               |

