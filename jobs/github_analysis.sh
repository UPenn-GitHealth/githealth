python3 github_analysis.py
echo "uploading to aws"
aws s3 cp ~/githealth/jobs/data.csv s3://githealth/
