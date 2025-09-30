"""
Application api views url for external connections and front end logic.
"""
from django.urls import path
from application.api import views

urlpatterns = [
    path('join_meeting_api/', views.join_meeting_api, name="join_meeting_api"),
    path('insurance_providers_api/', views.insurance_providers_api, name="insurance_providers_api"),

    path('get_application_types_api/', views.get_application_types_api,
         name="get_application_types_api"),

    path('add_insurance_provider_api/', views.add_insurance_provider_api,
         name="add_insurance_provider_api"),

    path('edit_insurance_provider_api/', views.edit_insurance_provider_api,
         name="edit_insurance_provider_api"),

    path('del_insurance_provider_api/', views.del_insurance_provider_api,
         name="del_insurance_provider_api"),

    path('create_application_api/', views.create_application_api, name="create_application_api"),
    path('edit_assessment_note_file_api/', views.edit_assessment_note_file_api,
         name="edit_assessment_note_file_api"),

    path('get_application_api/', views.get_application_api, name="get_application_api"),
    path('create_assessment_api/', views.create_assessment_api, name="create_assessment_api"),
    path('save_assessment_notes_api/', views.save_assessment_notes_api,
         name="save_assessment_notes_api"),
     path('complete_status_api/', views.complete_status_api, name="complete_status_api"),
     path('change_status_api/', views.change_status_api, name="change_status_api"),

     path('event_calendar_api/', views.event_calendar_api, name="event_calendar_api"),
     path('get_assessments_api/', views.get_assessments_api, name="get_assessments_api"),
     path('get_assessment_info_api/', views.get_assessment_info_api, name="get_assessment_info_api"),
     path('create_room_api/', views.create_room_api, name="create_room_api"),
     path('get_event_token_api/', views.get_event_token_api, name="get_event_token_api"),

     path('video_conference_api/', views.video_conference_api, name="video_conference_api"),
     path('mark_event_complete_api/', views.mark_event_complete_api, name="mark_event_complete_api"),
     path('recording_to_s3_api/', views.recording_to_s3_api, name="recording_to_s3_api"),
]
