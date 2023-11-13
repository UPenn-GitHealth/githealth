python3 github_analysis.py
echo "uploading to aws"
aws s3 cp data.csv s3://githealth/
