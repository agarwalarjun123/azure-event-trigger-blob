import logging

import azure.functions as func
from PIL import Image
import io;
from azure.storage.blob import BlobServiceClient,ContentSettings
import os



connection_string = os.environ["filestoragetesttest_STORAGE"]
service = BlobServiceClient.from_connection_string(conn_str=connection_string)


def main(myblob: func.InputStream):
    file_name= myblob.name.split('/')[1]
    file_type= file_name.split('.')[len(file_name.split('.')) - 1]
    if file_type == 'jpg' or file_type == 'png':
        image = Image.open(myblob).convert('RGB')
        byte_array = io.BytesIO()
        image.save(byte_array,format='WEBP')
        blob_client = service.get_blob_client(container="data",blob=f"webp/{file_name.split('.')[0]}.webp")
        cnt_settings = ContentSettings(
            content_type="image/webp"
        )
        blob_client.upload_blob(byte_array.getvalue(),content_settings=cnt_settings,overwrite=True)




