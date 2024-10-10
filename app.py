import io
import pandas as pd
import json
from flask import Flask, request, jsonify, Response
from google.cloud import secretmanager
from google.cloud import storage
from google.oauth2 import service_account
import google.auth.transport.requests

app = Flask(__name__)

def get_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

@app.route('/', methods=['POST'])
def trigger_etl():
    data = request.get_json()

    # Extract the bucket name and file name from the request
    bucket_name = data.get('bucket_name')
    file_name = data.get('file_name')

    if not bucket_name or not file_name:
        return jsonify({'error': 'Missing bucket_name or file_name'}), 400
    
    # Get the file from Google Cloud Storage
    storage_client = storage.Client()

    # Access the bucket and the uploaded file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download file content as bytes
    file_content = blob.download_as_bytes()

    # Read the Excel file into a DataFrame
    df = pd.read_excel(io.BytesIO(file_content))

    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False)

    # Return the CSV response
    return Response(csv_data, mimetype='text/csv')

@app.route('/token', methods=['POST'])
def generate_token_and_check_subscription():
    data = request.get_json()

    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    # Check if the user is subscribed (this is a placeholder, implement your own logic)
    if not is_user_subscribed(user_id):
        return jsonify({'error': 'User is not subscribed'}), 403

    # Retrieve the service account key from Secret Manager
    key_json = get_secret("163924279121", "excel_python")
    key_data = json.loads(key_json)

    # Generate access token
    credentials = service_account.Credentials.from_service_account_info(key_data)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    auth_request = google.auth.transport.requests.Request()
    scoped_credentials.refresh(auth_request)
    token = scoped_credentials.token

    return Response(token, mimetype='text/plain')

def is_user_subscribed(user_id):
    # Implement your subscription check logic here
    # For example, query your database to check if the user is subscribed
    return True  # Placeholder, replace with actual check

