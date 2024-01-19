import logging
import os
import azure.functions as func
import base64
import sendgrid
from sendgrid.helpers.mail import Mail, From, Personalization, To, Cc, HtmlContent, Attachment, FileContent, FileName, Disposition, ContentId
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from utils import get_secret_from_key_vault


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        sendgrid_api_key = get_secret_from_key_vault('clientSendGridAPIKey')
        mail = Mail()
        mail = compose_email(req, mail)
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.client.mail.send.post(request_body=mail.get())
        return func.HttpResponse(f'email sent ', status_code=response.status_code)
    except Exception as e:
        return func.HttpResponse(f'email failed, error message: {str(e)}', status_code=500)
 

def compose_email(request: func.HttpRequest, mail: Mail):
    try:
        requestJson = request.get_json()                   
        # mandatory fields
        sender_email = requestJson['sender_address']
        email_subject = requestJson['email_subject']

        # email body details
        if requestJson['html_content'] and requestJson['email_content']:
            mail = Mail(
                from_email=(sender_email),
                subject=email_subject,
                plain_text_content=(requestJson['email_content']),
                html_content=HtmlContent(requestJson['html_content'])
                )   
        elif requestJson['email_content']:
            mail = Mail(
                from_email=(sender_email),
                subject=email_subject,
                plain_text_content=(requestJson['email_content']),
                )
        elif requestJson['html_content']:
            mail = Mail(
                from_email=(sender_email),
                subject=email_subject,
                html_content=HtmlContent(requestJson['html_content'])
                )

        # attachment details
        if requestJson['with_attachment'].lower() == "yes":
            blob_connection_string= get_secret_from_key_vault('FuncappADLSConnString')
            try:
                attachment_blob_name = requestJson['blob_name']
                attachment_container = requestJson['container_name']
                blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
                blob_client = blob_service_client.get_blob_client(attachment_container, attachment_blob_name)
                stream_object_from_blob = blob_client.download_blob()
                stream = BytesIO()
                stream_object_from_blob.download_to_stream(stream)

 

                encoded = base64.b64encode(stream.getvalue()).decode()
                attachment = Attachment()
                attachment.file_content = FileContent(encoded)
                attachment.file_name = FileName(attachment_blob_name)
                attachment.disposition = Disposition('attachment')
                attachment.content_id = ContentId('Example Content ID')
                mail.attachment = attachment                 
            except Exception as e:
                raise Exception(f'failed to create attachment, error message: {str(e)}')

        # recipient details
        # unique email address in the personalizations array, won't allow duplicate addresses in To,Cc
        personalization = Personalization()
        if requestJson['recipient_address']:
            to_recipient_email = requestJson['recipient_address'].split(",")
            for to_address in to_recipient_email:
                personalization.add_to(To(to_address))
        if requestJson['cc_recipient_address']:
            cc_recipient_email = requestJson['cc_recipient_address'].split(",")
            for cc_address in cc_recipient_email:
                personalization.add_cc(Cc(cc_address))            
        mail.add_personalization(personalization)
        return mail
    except Exception as e:
        raise Exception(f'unable to compose email, error message: {str(e)}\n')