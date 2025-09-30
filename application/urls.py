"""
The `urls.py` module defines the URL patterns for the application.

The URL patterns define the routes that are available in the application,
as well as the views that are associated with those routes.
"""
from django.urls import path
from application import views


urlpatterns = [
    path('join_meeting/<int:assessment_id>', views.join_meeting, name="join_meeting"),

    path('insurance_providers/', views.insurance_providers, name="insurance_providers"),
    path('add_insurance_provider/', views.add_insurance_provider, name="add_insurance_provider"),
    path('edit_insurance_provider/', views.edit_insurance_provider, 
        name="edit_insurance_provider"),
    path('del_insurance_provider/', views.del_insurance_provider, name="del_insurance_provider"),
    path('schedule_assessment/', views.schedule_assessment, name="schedule_assessment"),
    path('save_assessment_notes/', views.save_assessment_notes, name="save_assessment_notes"),
    path('edit_assessment_note_file/', views.edit_assessment_note_file, 
        name="edit_assessment_note_file"),
    path('complete_status/<int:application_id>', views.complete_status, name="complete_status"),
    path('change_application_status/', views.change_application_status, 
        name="change_application_status"),

    path('event_calendar/', views.event_calendar, name="event_calendar"),
    path('create_room/', views.create_room, name="create_room"),
    path('get_assessments/', views.get_assessments, name="get_assessments"),
    path('get_assessment_info/', views.get_assessment_info, name="get_assessment_info"),
    path('video_conference/<int:assessment_id>', views.video_conference, name="video_conference"),
    path('get_event_token/', views.get_event_token, name="get_event_token"),
    path('mark_event_complete/', views.mark_event_complete, name="mark_event_complete"),
    path('video_complete_status/<int:twilio_room_id>', views.video_complete_status, name="video_complete_status"),
    
    
]
