from django.db import models

class IssueMetric(models.Model):
    # Assuming 'year' and 'month' together uniquely identify each record
    year = models.PositiveIntegerField(help_text="The year the metrics were collected")
    month = models.PositiveIntegerField(help_text="The month the metrics were collected")

    # Average metrics
    average_time_to_first_response = models.FloatField(
        help_text="Average time (in hours) to first response for issues in a given month"
    )
    average_time_to_close = models.FloatField(
        help_text="Average time (in hours) to close issues in a given month"
    )

    # You can add additional fields for more metrics, such as:
    total_issues_opened = models.PositiveIntegerField(help_text="Total number of issues opened in the month")
    total_issues_closed = models.PositiveIntegerField(help_text="Total number of issues closed in the month")
    contributor_count = models.PositiveIntegerField(help_text="Number of unique contributors in the month")

    class Meta:
        unique_together = ('year', 'month')
        ordering = ['year', 'month']

    def __str__(self):
        return f"Issues Metrics for {self.month}/{self.year}"