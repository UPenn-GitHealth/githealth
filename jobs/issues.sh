python3 issues_v4.0.py
echo "uploading to aws"
aws s3 cp issues_2023_new.csv s3://githealth/
