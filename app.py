from flask import Flask, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

app = Flask(__name__)

# Configure your AWS credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"
BUCKET_NAME = "cpsc5910-lab6-bucket"
FILE_NAME = "lab6-object"

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


@app.route("/hello")
def read_file_from_s3():
    try:
        # Read the file from S3
        s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        file_content = s3_object["Body"].read().decode("utf-8")

        return jsonify(file_content)

    except NoCredentialsError:
        return jsonify({"error": "Credentials not available"}), 403

    except PartialCredentialsError:
        return jsonify({"error": "Incomplete credentials"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
