import os
from urllib.parse import urlparse
from datetime import datetime
from decouple import config
from django.core.management.base import BaseCommand
from claims.models import AssessmentNote
from system_management.models import User  
import boto3

def extract_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return filename

def move_s3_assessment_note():
    notes = AssessmentNote.objects.filter(
        question__question_type="file"
    ).values(
        'id',
        'note',
        'file',
        'date_created',
        'assessment__application__user_id'
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

    for note in notes:
        if f"https://{bucket}.s3.amazonaws.com/" in note['question']:
            current_filepath = note['note']
            user_id = note['survey__application__user_id']
            user_data = users.filter(id=user_id).first()
            names = user_data['first_name'].replace(' ','').lower()
            surnames = user_data['last_name'].replace(' ','').lower()
            date_created = note['date_created']
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
    
            note_object = AssessmentNote.objects.get(id=note['id'])
            note_object.note=f"https://{bucket}.s3.amazonaws.com/{new_file_key}"
            note_object.save()
           
       
class Command(BaseCommand):
    help = 'assessment_note'
 
    def handle(self, *args, **options):
        move_s3_assessment_note()