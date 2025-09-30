"""
Create command for S3 transfer of files
"""
import os
from urllib.parse import urlparse
from decouple import config
from django.core.management.base import BaseCommand
from claims.models import HowQuestion
from system_management.models import User  
import boto3
 
def extract_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename
 

def move_s3_how_question():
    questions = HowQuestion.objects.filter(
        question_type="file"
    ).values(
        'id',
        'question',
        'question_type',
        'date_created',
        'claim__application__user_id'
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

    for question in questions:
        if f"https://{bucket}.s3.amazonaws.com/" in question['question']:
            current_filepath = question['question']
            user_id = question['claim__application__user_id']
            user_data = users.filter(id=user_id).first()
            names = user_data['first_name'].replace(' ','').lower()
            surnames = user_data['last_name'].replace(' ','').lower()
            date_created = question['date_created']
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
    
            question_object = HowQuestion.objects.get(id=question['id'])
            question_object.question=f"https://{bucket}.s3.amazonaws.com/{new_file_key}"
            question_object.save()
           
       
class Command(BaseCommand):
    help = 'move_s3_how_question'
 
    def handle(self, *args, **options):
        move_s3_how_question()


