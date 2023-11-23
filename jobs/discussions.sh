python3 discussions.py
echo "uploading to aws"
aws s3 cp ~/githealth/jobs/final_github_discussion_data.csv s3://githealth/
