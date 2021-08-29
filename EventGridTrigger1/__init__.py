import logging
import azure.functions as func
from PIL import Image
import io;
from urllib import parse
from azure.storage.blob import BlobServiceClient,ContentSettings,BlobClient
import os

connection_string = os.environ["filestoragetesttest_STORAGE"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def main(event: func.EventGridEvent):

    result = {
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    }
    blob_url = result["data"]["url"]
    blob_url = parse.urlsplit(blob_url)
    account_url = blob_url.netloc
    container = blob_url.path.split('/',2)[1]
    blob_path = blob_url.path.split('/',2)[2]
    file_type = blob_path.split('.')[1]

    if file_type == 'jpg' or file_type == 'png':
        # get blob_client from account_url and container and blob_path
        blob_client = BlobClient(account_url,container,blob_path)
        # read content of blob 
        blob_bytes = blob_client.download_blob().readall()
        # convert blob into webp
        image = Image.open(io.BytesIO(blob_bytes)).convert('RGB')
        byte_array = io.BytesIO()
        image.save(byte_array,format='WEBP')
        
        blob_client = blob_service_client.get_blob_client(container="data",blob=f"webp/{blob_path.split('.')[0]}.webp")
        cnt_settings = ContentSettings(
            content_type="image/webp"
        )
        blob_client.upload_blob(byte_array.getvalue(),content_settings=cnt_settings,overwrite=True)


    logging.info('Python EventGrid trigger processed an event: %s', result)
