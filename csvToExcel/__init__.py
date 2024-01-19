import azure.functions as func
import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import StringIO,BytesIO
from utils import get_secret_from_key_vault
 
def main(req: func.HttpRequest) -> func.HttpResponse:    
    try:
        reqJson = req.get_json()
        csv_file_name=reqJson['csv_file_name']
        excel_file_name=reqJson['excel_file_name']
        container_name=reqJson['container_name']
        directory_name=reqJson['directory_name']
        storage_connection_string= get_secret_from_key_vault('FuncappADLSConnString')
    
        # Connect to Azure Storage
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        # Get the CSV file from Azure Storage
        blob_client = blob_service_client.get_blob_client(container=container_name + directory_name, blob=csv_file_name)
        csv_data = blob_client.download_blob().content_as_text()
        # Convert CSV to DataFrame
        df = pd.read_csv(StringIO(csv_data))        
        # Convert DataFrame to Excel
        excel_data = BytesIO()
        df.to_excel(excel_data, index=False)
        excel_data.seek(0)
        # Upload the Excel file to Azure Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=directory_name + excel_file_name)
        blob_client.upload_blob(excel_data)

        return func.HttpResponse(f"File '{excel_file_name}' saved to Azure storage", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)