"""
Create command for S3 transfer of files
"""
import os
from urllib.parse import urlparse
from datetime import datetime
from decouple import config
from django.core.management.base import BaseCommand
from surveys.models import SurveyAnswer
from system_management.models import User  
import boto3
 
def extract_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename
 

def move_s3_file():
    answers = SurveyAnswer.objects.filter(
        question__question_type="file"
    ).values(
        'id',
        'answer',
        'question_id',
        'date_created',
        'survey__application__user_id'
    )
    s3 = boto3.client('s3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
    )
    bucket = config('AWS_STORAGE_BUCKET_NAME')
    company_name = config('COMPANY_PATH')
    users = User.objects.values(
        'first_name', 
        'last_name', 
        'date_joined', 
        'id'
    )

    for answer in answers:  
        if f"https://{bucket}.s3.amazonaws.com/" in answer['answer']:
            current_filepath = answer['answer']
            user_id = answer['survey__application__user_id']
            user_data = users.filter(id=user_id).first()
            names = user_data['first_name'].replace(' ','').lower()
            surnames = user_data['last_name'].replace(' ','').lower()
            date_created = answer['date_created']
            current_file_key = str(current_filepath).replace(f"https://{bucket}.s3.amazonaws.com/", "")
            file_name = extract_filename_from_url(current_filepath)
            new_file_key =  f"{company_name}/{date_created.year}/{date_created.month}/{names}{surnames}_{str(user_id)}/{file_name}"
    
            s3.copy_object(
                Bucket=bucket,
                CopySource={
                    "Bucket": bucket,
                    "Key": current_file_key
                },
                Key=new_file_key
            )
    
            s3.delete_object(
                Bucket=bucket,
                Key=current_file_key
            )
    
            answer_object = SurveyAnswer.objects.get(id=answer['id'])
            answer_object.answer=f"https://{bucket}.s3.amazonaws.com/{new_file_key}"
            answer_object.save()
           
       
class Command(BaseCommand):
    help = 'move_s3_file'
 
    def handle(self, *args, **options):
        move_s3_file()
 