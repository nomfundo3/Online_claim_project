"""
This module is used for the management of claim applications front end logic
"""
import io
import os
import json
import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from system_management import constants
from system_management.decorators import check_token_in_session
from system_management.general_func_classes import host_url, api_connection
from system_management.amazons3 import upload_to_s3
from django.http import JsonResponse, FileResponse
from django.conf import settings
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, ListFlowable
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth


@check_token_in_session
def get_claim_application(request):
    """
    Get sub claim process.

    :param request:
        Django rest framework.

    :return:
        Json AJAX response for claim inforamtion.
    """
    if request.method == "GET":
        token = request.session.get('token')
        claim_id = request.GET.get('claim_id')

        url = f"{host_url(request)}{reverse('get_claim_application_api')}"

        payload = json.dumps({
            "claim_id": claim_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        status = response_data.get('status')

        context = {}

        if status == 'success':
            claim_data = response_data.get('data')
            application_types = response_data.get('application_types')

            categories = response_data.get('categories')

            context = {
                'claim_object': claim_data,
                'categories': categories,
                'application_types': application_types
            }

        else:
            context = {
                'claim_object': '',
                'categories': '',
                'application_types': ''
            }

        return JsonResponse(context, safe=True)


@check_token_in_session
def create_sub_claim(request):
    """
    Create sub claim process.

    :param request:
        Django rest framework.

    :return:
        HTML Template for claim process.
    """
    if request.method == "POST":
        token = request.session.get('token')
        application_id = request.POST.get('application_id')
        application_type = request.POST.get('application_type')

        url = f"{host_url(request)}{reverse('create_sub_claim_api')}"

        payload = json.dumps({
            "application_id": application_id,
            'application_type': application_type
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)
        return JsonResponse(response_data, safe=True)


@check_token_in_session
def assessment_preview(request, application_id):
    if request.method == "GET":
        token = request.session.get('token')

        url = f"{host_url(request)}{reverse('preview_report_claim_api')}"

        payload = json.dumps({
            "application_id": application_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)
        status = response_data.get('status')

        context = {}

        if status == 'success':
            application = response_data.get('data')

            context = {
                'current_application': application,
                'application_id': application_id
            }
        return render(request, 'assessor/assessment_preview.html', context)


@check_token_in_session
def manage_application(request, application_id):
    """
    Manage claim process.

    :param request:
        Django rest framework.

    :param application_id:
        Current application id.

    :return:
        HTML Template for claim process.
    """
    if request.method == "GET":
        token = request.session.get('token')
        user_role = request.session.get('role_type')

        url = f"{host_url(request)}{reverse('manage_application_api')}"

        payload = json.dumps({
            "application_id": application_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)
        application_data = response_data.get('data')

        if application_data:
            current_application = application_data.get('current_application')
            claims = application_data.get('claims')
        else:
            current_application = ''
            claims = ''

        payload = json.dumps({

        })

        url = f"{host_url(request)}{reverse('get_claim_info_api')}"
        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)
        claim_info = response_data.get('data')

        if not claim_info:
            insurance_provider = []
            assessors = []
            statuses = []
            application_types = []

        else:
            insurance_provider = claim_info.get('insurance_provider')
            assessors = claim_info.get('assessors')
            statuses = claim_info.get('statuses')
            application_types = claim_info.get('application_types')

        context = {
            "current_application": current_application,
            "user_role": user_role,
            "application_id": application_id,
            'insurance_provider': insurance_provider,
            'assessors': assessors,
            'statuses': statuses,
            'claims': claims,
            'application_types': application_types
        }
        return render(request, 'claims/admin_application.html', context)


@check_token_in_session
def claim_client_add(request):
    """
    This function is used for the claim applications page
    :param request:
        Django request parameter
    
    :return:
        Render HTML Template for add client information.
    """
    application_type = request.GET.get('application_type')

    if application_type != constants.PERSONAL and \
            application_type != constants.BUSINESS:
        return render(request, '404_error.html')

    token = request.session.get('token')
    url = f"{host_url(request)}{reverse('insurance_providers_api')}"

    payload = json.dumps({

    })

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': constants.JSON_APPLICATION
    }

    response_data = api_connection(method="GET", url=url, data=payload, headers=headers)
    providers = get_data_on_success(response_data)

    context = {
        "application_type": application_type,
        "insurance_providers": providers,
    }

    return render(request, 'admin/claim_forms.html', context)


@check_token_in_session
def add_claim_client(request):
    """
    Add client info for claim application.

    :param request:
        Django request parameter.
    :return:
        Json response an status of api call and message.
    """
    if request.method == "POST":
        application_type = request.POST.get('application_type')
        has_business_info = request.POST.get('business_info')
        name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        insurer_id = request.POST.get('insurer_id')
        id_number = request.POST.get('id_number')
        policy_number = request.POST.get('policy_number')

        incident_location = request.POST.get('incident_location')
        incident_city = request.POST.get('incident_city')
        incident_province = request.POST.get('incident_province')
        incident_postal = request.POST.get('incident_postal')
        incident_date = request.POST.get('incident_date')

        token = request.session.get('token')
        user_id = request.session.get('user_id')

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        url = f"{host_url(request)}{reverse('add_claim_client_api')}"

        payload = json.dumps({
            "name": name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "insurer_id": insurer_id,
            "id_number": id_number,
            "policy_number": policy_number,
            "incident_location": incident_location,
            "incident_city": incident_city,
            "incident_province": incident_province,
            "incident_postal": incident_postal,
            "incident_date": incident_date
        })

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)
        status = response_data.get('status')

        if status == 'success':
            client_id = response_data.get('data')

            url = f"{host_url(request)}{reverse('create_application_api')}"

            payload = json.dumps({
                "user_id": user_id,
                "application_type": application_type,
                "application_category": constants.CLAIM,
                "client_id": client_id,
            })

            response_data = api_connection(method="POST", url=url, data=payload,
                                           headers=headers)

            status = response_data.get('status')

            if status != 'success':
                return JsonResponse(response_data, safe=False)

            application_id = response_data.get('data')['id']
            manage_application_link = reverse('manage_application', args=(application_id,))
            redirect_url = f"{host_url(request)}{manage_application_link}"

            if has_business_info == 'Yes':
                business_name = request.POST.get('business_name')
                business_reg_number = request.POST.get('business_reg_number')
                business_vat_number = request.POST.get('business_vat_number')
                business_email = request.POST.get('business_email')
                business_phone_number = request.POST.get('business_phone_number')

                url = f"{host_url(request)}{reverse('add_claim_business_api')}"

                payload = json.dumps({
                    "client_id": client_id,
                    "business_name": business_name,
                    "business_reg_number": business_reg_number,
                    "business_vat_number": business_vat_number,
                    "business_email": business_email,
                    "business_phone_number": business_phone_number
                })

                response_data = api_connection(method="POST", url=url, data=payload,
                                               headers=headers)

                status = response_data.get('status')

            if status == 'success':
                response_data = {
                    'status': 'success',
                    'message': 'Client created successfully',
                    'redirect_url': redirect_url
                }

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def manage_claims(request):
    """
    Manage claim application fields.

    :param request:
        Django request parameter.
    :return:
        Render HTML Template for manage claim application.
    """
    token = request.session.get('token')
    payload = json.dumps({

    })

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': constants.JSON_APPLICATION
    }

    url = f"{host_url(request)}{reverse('get_claim_categories_api')}"
    response_data = api_connection(method="GET", url=url, data=payload, headers=headers)

    context = response_data.get('data')

    return render(request, 'claims/manage_claims.html', context)


@check_token_in_session
def add_what_category(request):
    """
    Add claim what category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        category = request.POST.get('category')
        cause_id = request.POST.get('cause_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('add_what_category_api')}"

        payload = json.dumps({
            "category": category,
            "cause_id": cause_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_what_category(request):
    """
    Edit claim what category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        category = request.POST.get('category')
        cause_id = request.POST.get('cause_id')
        what_id = request.POST.get('what_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('edit_what_category_api')}"

        payload = json.dumps({
            "category": category,
            "cause_id": cause_id,
            "what_id": what_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def del_what_category(request):
    """
    Delete claim what category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        what_id = request.POST.get('what_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('del_what_category_api')}"

        payload = json.dumps({
            "what_id": what_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def add_how_category(request):
    """
    Add claim how category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        category = request.POST.get('category')
        cause_id = request.POST.get('cause_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('add_how_category_api')}"

        payload = json.dumps({
            "category": category,
            "cause_id": cause_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_how_category(request):
    """
    Edit claim how category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        category = request.POST.get('category')
        cause_id = request.POST.get('cause_id')
        how_id = request.POST.get('how_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('edit_how_category_api')}"

        payload = json.dumps({
            "category": category,
            "cause_id": cause_id,
            "how_id": how_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def del_how_category(request):
    """
    Delete claim how category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        how_id = request.POST.get('how_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('del_how_category_api')}"

        payload = json.dumps({
            "how_id": how_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def add_cause_category(request):
    """
    Add claim cause category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        application_type = request.POST.get('application_type')
        category = request.POST.get('category')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('add_cause_category_api')}"

        payload = json.dumps({
            "category": category,
            "application_type": application_type
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_cause_category(request):
    """
    Edit claim cause category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        category = request.POST.get('category')
        cause_id = request.POST.get('cause_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('edit_cause_category_api')}"

        payload = json.dumps({
            "category": category,
            "cause_id": cause_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def del_cause_category(request):
    """
    Delete claim cause category dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        cause_id = request.POST.get('cause_id')
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('del_cause_category_api')}"

        payload = json.dumps({
            "cause_id": cause_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def all_claims(request):
    """
    Claim information for scheduled, pending and complete claims.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "GET":
        token = request.session.get('token')
        user_role = request.session.get('role_type')

        payload = json.dumps({})
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        url = f"{host_url(request)}{reverse('get_all_claims_api')}"
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        applications = response_data.get('data')
        applications_df = pd.DataFrame(applications)

        if not applications_df.empty:
            if user_role == constants.ADMIN:
                completed_applications = applications_df[
                    applications_df['application_status__name'] == 'Completed'
                ].to_dict('records')

                pending_applications = applications_df[
                    applications_df['application_status__name'] == 'Pending'
                ].to_dict('records')

                scheduled_applications = applications_df[
                    applications_df['application_status__name'] == 'Scheduled'
                ].to_dict('records')

            elif user_role == constants.ASSESSOR:
                user_id = request.session.get('user_id')
                completed_applications = applications_df[
                    (applications_df['application_status__name'] == 'Completed') &
                    (applications_df['assessor_id'] == user_id)
                ].to_dict('records')

                pending_applications = applications_df[
                    (applications_df['application_status__name'] == 'Pending') &
                    (applications_df['assessor_id'] == user_id)
                ].to_dict('records')

                scheduled_applications = applications_df[
                    (applications_df['application_status__name'] == 'Scheduled') &
                    (applications_df['assessor_id'] == user_id)
                ].to_dict('records')
                
            else:
                completed_applications = []
                pending_applications = []
                scheduled_applications = []
        else:
            completed_applications = []
            pending_applications = []
            scheduled_applications = []

        scheduled_claims = len(scheduled_applications)
        pending_claims = len(pending_applications)
        complete_claims = len(completed_applications)

        url = f"{host_url(request)}{reverse('get_all_assessors_api')}"
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        assessors = get_data_on_success(response_data)

        url = f"{host_url(request)}{reverse('get_application_types_api')}"
        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)

        application_types = get_data_on_success(response_data)

        context = {
            "assessors": assessors,
            "application_types": application_types,
            "scheduled_claims": scheduled_claims,
            "pending_claims": pending_claims,
            "complete_claims": complete_claims,
            "completed_applications": completed_applications,
            "pending_applications": pending_applications,
            "scheduled_applications": scheduled_applications
        }

        return render(request, 'claims/claims.html', context)


@check_token_in_session
def assessor_claims(request):
    """
    Claim information for scheduled, pending and complete claims.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "GET":
        token = request.session.get('token')
        user_id = request.session.get('user_id')
        payload = json.dumps({})
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        url = f"{host_url(request)}{reverse('get_all_claims_api')}"
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        applications = response_data.get('data')

        applications_df = pd.DataFrame(applications)

        if not applications_df.empty:
            completed_applications = applications_df[
                (applications_df['application_status__name'] == 'Completed') &
                (applications_df['assessor_id'] == user_id)
                ].to_dict('records')

            pending_applications = applications_df[
                (applications_df['application_status__name'] == 'Pending') &
                (applications_df['assessor_id'] == user_id)
                ].to_dict('records')

            scheduled_applications = applications_df[
                (applications_df['application_status__name'] == 'Scheduled') &
                (applications_df['assessor_id'] == user_id)
                ].to_dict('records')

        else:
            completed_applications = []
            pending_applications = []
            scheduled_applications = []

        scheduled_claims = len(scheduled_applications)
        pending_claims = len(pending_applications)
        complete_claims = len(completed_applications)

        url = f"{host_url(request)}{reverse('get_all_assessors_api')}"
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        assessors = get_data_on_success(response_data)

        url = f"{host_url(request)}{reverse('get_application_types_api')}"
        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)

        application_types = get_data_on_success(response_data)

        context = {
            "assessors": assessors,
            "application_types": application_types,
            "scheduled_claims": scheduled_claims,
            "pending_claims": pending_claims,
            "complete_claims": complete_claims,
            "completed_applications": completed_applications,
            "pending_applications": pending_applications,
            "scheduled_applications": scheduled_applications
        }

        return render(request, 'assessor/assessor.html', context)


@check_token_in_session
def edit_client_application(request):
    """
    Edit application dynamically.
    
    :param request:
    Django request parameter.
    :return:
    Json response a status of api call and message.
    """
    if request.method == "POST":
        token = request.session.get('token')
        client_id = request.POST.get('client_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        id_number = request.POST.get('id_number')
        phone_number = request.POST.get('phone_number')

        url = f"{host_url(request)}{reverse('edit_client_application_api')}"

        payload = json.dumps({
            "client_id": client_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "id_number": id_number,
            "phone_number": phone_number
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)
        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_business_application(request):
    """
    Edit business application dynamically.
    
    :param request:
    Django request parameter.
    :return:
    Json response a status of api call and message.
    """
    if request.method == "POST":
        token = request.session.get('token')
        client_id = request.POST.get('client_id')
        business_name = request.POST.get('business_name')
        business_email = request.POST.get('business_email')
        reg_number = request.POST.get('reg_number')
        vat_number = request.POST.get('vat_number')
        phone_no = request.POST.get('phone_no')

        url = f"{host_url(request)}{reverse('edit_business_application_api')}"

        payload = json.dumps({
            "client_id": client_id,
            "business_name": business_name,
            "business_email": business_email,
            "reg_number": reg_number,
            "vat_number": vat_number,
            "phone_no": phone_no
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)
        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_claim_application(request):
    """
    Edit claim application dynamically.
    
    :param request:
    Django request parameter.
    :return:
    Json response a status of api call and message.
    """
    if request.method == "POST":
        token = request.session.get('token')
        client_id = request.POST.get('client_id')
        insurance_id = request.POST.get('insurance_id')
        policy_no = request.POST.get('policy_no')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        url = f"{host_url(request)}{reverse('edit_claim_application_api')}"

        payload = json.dumps({
            "client_id": client_id,
            "insurance_id": insurance_id,
            "policy_no": policy_no,
            "street_address": street_address,
            "city": city,
            "postal_code": postal_code
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)
        return JsonResponse(response_data, safe=False)


def get_data_on_success(response_data):
    status = response_data.get('status')
    if status == 'success':
        data = response_data.get('data')
    else:
        data = []
    return data


@check_token_in_session
def change_application_type(request):
    """
    Change application type dynamically.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        application_id = request.POST.get('application_id')
        application_type = request.POST.get('client_type')

        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('change_application_type_api')}"

        payload = json.dumps({
            "application_id": application_id,
            "application_type": application_type
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        status = response_data.get('status')
        if status == 'success':
            application_type_name = response_data.get('data')
            payload = json.dumps({
                "application_type": application_type
            })
            url = f"{host_url(request)}{reverse('application_type_categories_api')}"

            response_data = api_connection(method="GET", url=url, data=payload, headers=headers)
            status = response_data.get('status')

            if status == 'success':
                categories = response_data.get('data')
                if not categories:
                    how_categories = []
                    what_categories = []
                    cause_categories = []
                    application_types = []

                else:
                    how_categories = categories.get('how_categories')
                    what_categories = categories.get('what_categories')
                    cause_categories = categories.get('cause_categories')
                    application_types = categories.get('application_types')

                response_data = {
                    "status": 'success',
                    "application_type": application_type,
                    "how_categories": how_categories,
                    "what_categories": what_categories,
                    "cause_categories": cause_categories,
                    "application_types": application_types,
                    "application_type_name": application_type_name,
                    "message": "Application type changed successfully"
                }
        return JsonResponse(response_data, safe=False)


@check_token_in_session
def assign_what_application(request):
    """
    Assign a what category to the application.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        claim_id = request.POST.get('claim_id')
        what_id = request.POST.get('what_id')

        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('assign_what_application_api')}"

        payload = json.dumps({
            "claim_id": claim_id,
            "what_id": what_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def assign_how_application(request):
    """
    Assign a how category to the application.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        claim_id = request.POST.get('claim_id')
        how_id = request.POST.get('how_id')

        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('assign_how_application_api')}"

        payload = json.dumps({
            "claim_id": claim_id,
            "how_id": how_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def assign_cause_application(request):
    """
    Assign a cause category to the application.

    :param request:
        Django request parameter.
    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":
        claim_id = request.POST.get('claim_id')
        cause_id = request.POST.get('cause_id')

        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('assign_cause_application_api')}"

        payload = json.dumps({
            "claim_id": claim_id,
            "cause_id": cause_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def how_category_questions(request, how_id):
    """
    Get how category questions

    :param request:
        Django request parameter.

    :param how_id:
        How id for passed how category.

    :return:
        Json response a status of api call and message.
    """
    if request.method == "GET":
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('how_category_questions_api')}"

        payload = json.dumps({
            "category_id": how_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, data=payload,
                                       headers=headers)

        question_titles = get_data_on_success(response_data)

        how_category = response_data.get('how_category')

        context = {
            "question_titles": question_titles,
            "how_id": how_id,
            "how_category": how_category
        }

        return render(request, 'claims/how_category_questions.html', context)


@check_token_in_session
def what_category_questions(request, what_id):
    """
    Get what category questions

    :param request:
        Django request parameter.

    :param what_id:
        What id for passed category.

    :return:
        Json response a status of api call and message.
    """
    if request.method == "GET":
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('what_category_questions_api')}"

        payload = json.dumps({
            "category_id": what_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, data=payload,
                                       headers=headers)
        question_titles = get_data_on_success(response_data)

        what_category = response_data.get('what_category')

        context = {
            "question_titles": question_titles,
            "what_id": what_id,
            "what_category": what_category
        }
        return render(request, 'claims/what_category_questions.html', context)


@check_token_in_session
def create_how_title(request):
    """
    Create how category title
    
    :param request:
        Django request parameter.
    :return:
        Call to api for create how title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        what_id = request.POST.get('category_id')
        title = request.POST.get('title')
        url = f"{host_url(request)}{reverse('create_how_title_api')}"

        payload = json.dumps({
            'category_id': what_id,
            'title': title
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def create_what_title(request):
    """
    Create what category title

    :param request:
        Django request parameter.
    :return:
        Call to api for create what title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        what_id = request.POST.get('category_id')
        title = request.POST.get('title')

        url = f"{host_url(request)}{reverse('create_what_title_api')}"

        payload = json.dumps({
            "category_id": what_id,
            "title": title
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def create_how_question(request):
    """
    Create how category questions

    :param request:
        Django request parameter.
    :return:
        Call to api for create how question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')
        question = request.POST.get('question')
        question_type = request.POST.get('question_type')
        question_option = request.POST.getlist('options[]')
        is_mandatory = request.POST.get('is_mandatory')
        has_other_field = request.POST.get('has_other_field')

        url = f"{host_url(request)}{reverse('create_question_how_api')}"

        payload = json.dumps({
            "title_id": title_id,
            "question": question,
            "question_type": question_type,
            "options": question_option,
            "is_mandatory": is_mandatory,
            "has_other_field": has_other_field
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def create_what_question(request):
    """
    Create what category questions
    
    :param request:
        Django request parameter.
    :return:
        Call to api for create what question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')
        question = request.POST.get('question')
        question_type = request.POST.get('question_type')
        question_option = request.POST.getlist('options[]')
        is_mandatory = request.POST.get('is_mandatory')
        has_other_field = request.POST.get('has_other_field')

        url = f"{host_url(request)}{reverse('create_question_what_api')}"

        payload = json.dumps({
            "title_id": title_id,
            "question": question,
            "question_type": question_type,
            "options": question_option,
            "is_mandatory": is_mandatory,
            "has_other_field": has_other_field
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def save_claim_questions(request):
    """
    Save claim how and what questions.

    :param request:
        Django request parameter.

    :return:
        Json response a status of api call and message.
    """
    if request.method == "POST":

        claim_id = request.POST.get('claim_id')
        application_id = request.POST.get('application_id')
        what_answers = request.POST.getlist('what_answers[]')
        how_answers = request.POST.getlist('how_answers[]')
        if what_answers:
            what_answers = [json.loads(answer) for answer in what_answers]
            df_what = pd.DataFrame(what_answers)
            df_what = df_what.apply(lambda series:
                                    save_file_s3(request, series, application_id, claim_id), axis=1)
            what_answers = df_what.to_dict('records')

        if how_answers:
            how_answers = [json.loads(answer) for answer in how_answers]
            df_how = pd.DataFrame(how_answers)
            df_how = df_how.apply(lambda series:
                                  save_file_s3(request, series, application_id, claim_id), axis=1)
            how_answers = df_how.to_dict('records')

        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('save_claim_questions_api')}"

        payload = json.dumps({
            "claim_id": claim_id,
            "what_answers": what_answers,
            "how_answers": how_answers
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


def save_file_s3(request, series, application_id, claim_id):
    """
    Save file to s3 bucket.
    
    :param request:
        Django request parameter with file info.

    :param series:
        Series of question.

    :param application_id:
        Application id.
    
    :return:
        Series of question.

    """
    answer = series['answer']
    question_type = series['question_type']
    if question_type == 'file':
        file = request.FILES.get(answer)
        file_name = file.name
        file_extension = file_name.split('.')[-1]
        survey_answer = f"survey_{claim_id}/{answer}.{file_extension}"
        file_path = f"application_files/application_{application_id}/{survey_answer}"
        file_link = upload_to_s3(file, file_path)
        series['answer'] = file_link
    return series


@check_token_in_session
def edit_title_how(request):
    """
    Edit how category title

    :param request:
        Django request parameter.
    :return:
        Call to api for edit how title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')
        title = request.POST.get('title')

        url = f"{host_url(request)}{reverse('edit_title_how_api')}"

        payload = json.dumps({
            "title_id": title_id,
            "title": title
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_title_what(request):
    """
    Edit what category title

    :param request:
        Django request parameter.
    :return:
        Call to api for edit how title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')
        title = request.POST.get('title')

        url = f"{host_url(request)}{reverse('edit_title_what_api')}"

        payload = json.dumps({
            "title_id": title_id,
            "title": title
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def delete_title_how(request):
    """
    Delete how category title

    :param request:
        Django request parameter.
    :return:
        Call to api for delete how title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')

        url = f"{host_url(request)}{reverse('delete_title_how_api')}"

        payload = json.dumps({
            "title_id": title_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def delete_title_what(request):
    """
    Delete what category title

    :param request:
        Django request parameter.
    :return:
        Call to api for delete how title response
    """
    if request.method == "POST":
        token = request.session.get('token')
        title_id = request.POST.get('title_id')

        url = f"{host_url(request)}{reverse('delete_title_what_api')}"

        payload = json.dumps({
            "title_id": title_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_how_question(request):
    """
    Edit how category questions

    :param request:
        Django request parameter.
    :return:
        Call to api for edit how question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        question = request.POST.get('question')
        question_type = request.POST.get('question_type')
        question_option = request.POST.getlist('options[]')
        is_mandatory = request.POST.get('is_mandatory')
        has_other_field = request.POST.get('has_other_field')
        how_question_id = request.POST.get('question_id')

        url = f"{host_url(request)}{reverse('edit_how_question_api')}"

        payload = json.dumps({
            "question": question,
            "question_type": question_type,
            "options": question_option,
            "is_mandatory": is_mandatory,
            "has_other_field": has_other_field,
            "question_id": how_question_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_what_question(request):
    """
    Edit what category questions

    :param request:
        Django request parameter.
    :return:
        Call to api for edit what question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        question = request.POST.get('question')
        question_type = request.POST.get('question_type')
        question_option = request.POST.getlist('options[]')
        is_mandatory = request.POST.get('is_mandatory')
        has_other_field = request.POST.get('has_other_field')
        what_question_id = request.POST.get('question_id')

        url = f"{host_url(request)}{reverse('edit_what_question_api')}"

        payload = json.dumps({
            "question": question,
            "question_type": question_type,
            "options": question_option,
            "is_mandatory": is_mandatory,
            "has_other_field": has_other_field,
            "question_id": what_question_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def delete_what_question(request):
    """
    Delete what category questions

    :param request:
        Django request parameter.
    :return:
        Call to api for delete what question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        question_id = request.POST.get('question_id')

        url = f"{host_url(request)}{reverse('delete_what_question_api')}"

        payload = json.dumps({
            "question_id": question_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def delete_how_question(request):
    """
    Delete how category questions

    :param request:
        Django request parameter.
    :return:
        Call to api for delete how question response
    """
    if request.method == "POST":
        token = request.session.get('token')
        question_id = request.POST.get('question_id')

        url = f"{host_url(request)}{reverse('delete_how_question_api')}"

        payload = json.dumps({
            "question_id": question_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload,
                                       headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def generate_report_claim(request, application_id):
    """
    Generate report all claims.

    :param request:
        Django incoming request
    
    :param application_id:
        Current application id

    :param return:
        PDF for claim application
    """
    if request.method == "GET":
        url = f"{host_url(request)}{reverse('generate_report_claim_api')}"

        payload = json.dumps({
            "application_id": application_id
        })

        headers = {
            'Authorization': f'Token {request.session.get("token")}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(
            method="POST",
            url=url,
            headers=headers,
            data=payload
        )

        if 'status' not in response_data:
            return JsonResponse(response_data, safe=True)

        status = response_data.get('status')

        if status != 'success':
            return JsonResponse(response_data, safe=True)

        application = response_data.get('data')
        client_object = application.get('client')
        client_incident = client_object.get('client_incident')
        assessment = application.get('assessment')
        assessment_exists = False

        if assessment:
            assessment_exists = True
            assessment = application.get('assessment')[0]

        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
        pdf_canvas.setTitle(f"Assessment-Report-{str(application['id'])}")
        base_image = os.path.join(settings.BASE_DIR, "system_management", "static", 'images',
                                  'claim')
        path_cover = os.path.join(base_image, 'Cover.png')
        pdf_canvas.drawImage(path_cover, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                             mask='auto')

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 225,
                              f"{client_object['first_name']} {client_object['last_name']}")

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 155,
                              f"{application['assessor_id__first_name']} {application['assessor_id__last_name']}")

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 80, f"{client_object['insurer__insurance_name']}")

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(320, 225, f"{client_object['policy_no']}")

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(320, 155, f"{client_object['client_incident']['date_of_incident']}")

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)

        if assessment_exists:
            pdf_canvas.drawString(320, 80,
                                  f"{assessment['scheduled_date_time']}")
        else:
            pdf_canvas.drawString(320, 80, "No date scheduled")
        pdf_canvas.showPage()

        path_client = os.path.join(base_image, 'client.png')
        pdf_canvas.drawImage(path_client, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                             mask='auto')

        message_style = styles['Normal']
        message_style.textColor = HexColor('#000000')
        message_style.fontSize = 12

        msg = f"{client_object['first_name']} {client_object['last_name']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=585,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['id_number']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=540,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['phone_number']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=540,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        client_address = f"""
        {client_incident['street_address']},{client_incident['city']},{client_incident['province']},{client_incident['postal_code']}
        """

        msg = f"{client_address}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=513,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_incident['postal_code']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=445,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['policy_no']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=445,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['email']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=400,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{application['date_created']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=260,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_incident['date_of_incident']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=260,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['insurer__insurance_name']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=220,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        application_type = "Multi"

        msg = f"{application_type}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=175,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica-Bold", 25)
        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
        pdf_canvas.showPage()

        claims = application.get('claims')
        if claims:
            for claim in claims:
                if claim['application_type__name'] == 'Business':
                    path_business = os.path.join(base_image, 'business.png')
                    pdf_canvas.drawImage(path_business, x=0, y=0, width=8.268 * inch,
                                         height=11.693 * inch,
                                         mask='auto')

                    pdf_canvas.showPage()

                elif claim['application_type__name'] == 'Personal':
                    path_personal = os.path.join(base_image, 'personal.png')
                    pdf_canvas.drawImage(path_personal, x=0, y=0, width=8.268 * inch,
                                         height=11.693 * inch,
                                         mask='auto')
                    pdf_canvas.showPage()

                path_overview = os.path.join(base_image, 'overview.png')
                pdf_canvas.drawImage(path_overview, x=0, y=0, width=8.268 * inch,
                                     height=11.693 * inch,
                                     mask='auto')

                message_style = styles['Normal']
                message_style.textColor = HexColor('#000000')
                message_style.fontSize = 18
                message_style.fontName = 'Helvetica-Bold'

                msg = f"{claim['application_type__name']}"
                pdf_canvas = draw_paragraph(
                    pdf_canvas=pdf_canvas,
                    msg=msg,
                    x=195,
                    y=485,
                    max_height=300,
                    max_width=300,
                    message_style=message_style
                )
                if claim['application_cause'] == '':
                    msg = "Unselected"
                else:
                    msg = f"{claim['application_cause']['cause_id__name']}"

                pdf_canvas = draw_paragraph(
                    pdf_canvas=pdf_canvas,
                    msg=msg,
                    x=195,
                    y=380,
                    max_height=300,
                    max_width=300,
                    message_style=message_style
                )

                if claim['application_what'] == '':
                    msg = "Unselected"
                else:
                    msg = f"{claim['application_what']['what_id__name']}"

                pdf_canvas = draw_paragraph(
                    pdf_canvas=pdf_canvas,
                    msg=msg,
                    x=195,
                    y=275,
                    max_height=300,
                    max_width=300,
                    message_style=message_style
                )

                if claim['application_how'] == '':
                    msg = "Unselected"
                else:
                    msg = f"{claim['application_how']['how_id__name']}"

                pdf_canvas = draw_paragraph(
                    pdf_canvas=pdf_canvas,
                    msg=msg,
                    x=195,
                    y=160,
                    max_height=300,
                    max_width=300,
                    message_style=message_style
                )

                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                pdf_canvas.setFont("Helvetica-Bold", 25)
                pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                pdf_canvas.showPage()

                list_columns = ['title', 'questions']

                how_questions = pd.DataFrame(columns=list_columns)
                what_questions = pd.DataFrame(columns=list_columns)
                
                if 'details' in claim:
                    details = claim['details']
                    how_questions_list = details['how_questions']
                    what_questions_list = details['what_questions']
                    
                    if not how_questions_list == '':
                        how_questions = pd.DataFrame(how_questions_list)
                    
                    if not what_questions_list == '':
                        what_questions = pd.DataFrame(what_questions_list)

                if not how_questions.empty and not what_questions.empty:
                    how_questions = how_questions[list_columns]
                    what_questions = what_questions[list_columns]
                    questions = pd.concat([what_questions, how_questions])

                elif not how_questions.empty and what_questions.empty:
                    questions = how_questions[list_columns]

                elif not what_questions.empty and how_questions.empty:
                    questions = what_questions[list_columns]
                
                else:
                    questions = pd.DataFrame(columns=list_columns)

                background_image = os.path.join(base_image, 'Back.png')

                message_style = styles['Normal']
                message_style.textColor = HexColor('#000000')
                message_style.fontSize = 12
                message_style.fontName = 'Helvetica'

                if not questions.empty:
                    
                    path_question = os.path.join(base_image, 'question.png')
                    pdf_canvas.drawImage(path_question, x=0, y=0, width=8.268 * inch,
                                         height=11.693 * inch,
                                         mask='auto')
                    y_axis = 550

                    for _, title in questions.iterrows():

                        title_name = title['title']
                        question_answers_df = pd.DataFrame(title['questions'])
                        question_answers_df = question_answers_df.assign(
                            title=title_name
                        )

                        question_answers_df = question_answers_df.fillna('')
                        question_answers_df = question_answers_df.loc[
                            (question_answers_df['answer'] != "")]
                        question_answers_df = question_answers_df.loc[
                            ~(question_answers_df['answer'].isnull())]

                        list_columns = [
                            'title',
                            'question',
                            'answer',
                            'question_type',
                            'has_file'
                        ]
                        group_answers_df = question_answers_df[list_columns]
                        group_answers_df = group_answers_df.sort_values(by=['has_file'],
                                                                        ascending=False)
                        group_answers_df['answer'] = group_answers_df['answer'].apply(
                            lambda answer:
                            answer[0]['answer']
                        )
                        data = list(group_answers_df.values.tolist())

                        if not data:
                            continue

                        first_question = True

                        for question in data:

                            if type(question[2]) == list:
                                question[2] = question[2][0]

                            if str(question[3]) == 'file':
                                height = 250
                                y_axis_check = y_axis - height

                                if y_axis_check < 130:
                                    y_axis = 625

                                    pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                    pdf_canvas.setFont("Helvetica-Bold", 25)
                                    pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                                    pdf_canvas.showPage()
                                    pdf_canvas.drawImage(background_image, x=0, y=0,
                                                         width=8.268 * inch,
                                                         height=11.693 * inch,
                                                         mask='auto')

                                if first_question:
                                    pdf_canvas.setFillColor(HexColor('#C40001'))
                                    pdf_canvas.setFont("Helvetica-Bold", 18)
                                    pdf_canvas.drawString(20, (y_axis + 14), f"{title_name}")
                                    first_question = False

                                pdf_canvas.roundRect(10, y_axis - (0.14 * inch + height),
                                                     7.8 * inch,
                                                     (0.07 * inch + height), 8,
                                                     stroke=True)
                                pdf_canvas.drawImage(str(question[2]), 25,
                                                     (y_axis - height + 30), 200, 180)

                                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                msg_width = stringWidth(f"{question[1]}", "Helvetica", 12)
                                pdf_canvas.rect(25, y_axis - 0.12 * inch, msg_width, 0.25 * inch,
                                                fill=True,
                                                stroke=False)

                                msg = f"{question[1]}"
                                message_style = styles['Normal']
                                message_style.textColor = HexColor('#000000')
                                pdf_canvas = draw_paragraph(pdf_canvas, msg, 30,
                                                            y_axis + 0.03 * inch,
                                                            7.5 * inch, 0.25 * inch,
                                                            message_style)

                                y_axis = y_axis - (height + 40)

                            else:

                                msg = f"{question[2]}"
                                message_style = styles['Normal']
                                message_style.textColor = HexColor('#000000')
                                height = paragraph_height(pdf_canvas, question[2],
                                                          7.5 * inch,
                                                          0.75 * inch,
                                                          message_style)

                                question_height = paragraph_height(pdf_canvas, question[1],
                                                                   7.5 * inch,
                                                                   0.25 * inch, message_style)

                                if height < 0.75 * inch:
                                    height = 0.75 * inch

                                y_diff = height + question_height
                                y_axis_check = y_axis - question_height

                                if y_axis_check < 130:
                                    y_axis = 625 - question_height

                                    pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                    pdf_canvas.setFont("Helvetica-Bold", 25)
                                    pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                                    pdf_canvas.showPage()

                                    pdf_canvas.drawImage(background_image, x=0, y=0,
                                                         width=8.268 * inch,
                                                         height=11.693 * inch,
                                                         mask='auto')

                                if first_question:
                                    pdf_canvas.setFillColor(HexColor('#C40001'))
                                    pdf_canvas.setFont("Helvetica-Bold", 18)
                                    pdf_canvas.drawString(20, (y_axis + 14), f"{title_name}")
                                    first_question = False

                                pdf_canvas.roundRect(
                                    10,
                                    y_axis - (0.14 * inch + height + (question_height / 2)),
                                    7.8 * inch,
                                    (0.07 * inch + height + (question_height / 2)), 8,
                                    stroke=True
                                )

                                pdf_canvas = draw_paragraph(pdf_canvas, msg, 25,
                                                            (y_axis - question_height / 2) - 10,
                                                            7.5 * inch,
                                                            0.75 * inch, message_style)

                                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                msg_width = stringWidth(f"{question[1]}", "Helvetica", 12)

                                pdf_canvas.rect(
                                    25,
                                    (y_axis - question_height / 2),
                                    msg_width + 20,
                                    question_height + 5,
                                    fill=True,
                                    stroke=False
                                )

                                msg = f"{question[1]}"
                                pdf_canvas = draw_paragraph(
                                    pdf_canvas,
                                    msg,
                                    30,
                                    (y_axis + (question_height / 2)) - 5, 7.4 * inch,
                                    0.25 * inch,
                                    message_style
                                )

                                y_axis = y_axis - (y_diff + 40)

                        if y_axis < 255:

                            if first_question:
                                y_axis = 600

                            else:
                                y_axis = 625

                            pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                            pdf_canvas.setFont("Helvetica-Bold", 25)
                            pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                            pdf_canvas.showPage()
                            pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                                    height=11.693 * inch, mask='auto')
                
                assessment_notes = claim.get('notes')

                if assessment_notes:
                    path_notes = os.path.join(base_image, 'notes.png')
                    pdf_canvas.drawImage(path_notes, x=0, y=0, width=8.268 * inch,
                                         height=11.693 * inch,
                                         mask='auto')
                    height = 550
                    for note in assessment_notes:
                        check_height = height - 250
                        if check_height <= 110:

                            pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                            pdf_canvas.setFont("Helvetica-Bold", 25)
                            pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                            pdf_canvas.showPage()
                            pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                                 height=11.693 * inch,
                                                 mask='auto')
                            height = 625

                            pdf_canvas.setFont("Helvetica-Bold", 10)
                            pdf_canvas.setFillColor(HexColor('#000000'))
                            pdf_canvas.drawString(30, height, 'Note description:')
                            pdf_canvas.drawString(150, height, note['note'])
                            pdf_canvas.drawString(30, height - 15, 'Picture:')
                            height = height - 235
                            pdf_canvas.drawImage(note['file'], 30, height, width=500,
                                                 height=200)

                            height = height - 15

                        else:
                            pdf_canvas.setFont("Helvetica-Bold", 10)
                            pdf_canvas.setFillColor(HexColor('#000000'))
                            pdf_canvas.drawString(30, height, 'Note description:')
                            pdf_canvas.drawString(150, height, note['note'])
                            pdf_canvas.drawString(30, height - 15, 'Picture:')
                            height = height - 235
                            pdf_canvas.drawImage(note['file'], 30, height, width=500,
                                                 height=200)
                            height = height - 15

                    pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                    pdf_canvas.setFont("Helvetica-Bold", 25)
                    pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                    pdf_canvas.showPage()
        
        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica-Bold", 25)
        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")

        pdf_canvas.save()

        buffer.seek(0)
        filename = f"Assessment-Report-{str(application['id'])}.pdf"
        return FileResponse(
            buffer,
            content_type='application/pdf',
            as_attachment=False,
            filename=filename
        )


@check_token_in_session
def report_single_claim(request):
    """
    Generate report for selected claim.

    :param request:
        Django incoming request
    
    :param return:
        PDF for claim application
    """
    if request.method == "POST":
        claim_id = request.POST.get('claim_id')
        url = f"{host_url(request)}{reverse('report_single_claim_api')}"

        payload = json.dumps({
            "claim_id": claim_id
        })

        headers = {
            'Authorization': f'Token {request.session.get("token")}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(
            method="POST",
            url=url,
            headers=headers,
            data=payload
        )

        if 'status' not in response_data:
            return JsonResponse(response_data, safe=True)

        status = response_data.get('status')

        if status != 'success':
            return JsonResponse(response_data, safe=True)

        data = response_data.get('data')

        application = data.get('application')
        client_object = application.get('client')
        client_incident = client_object.get('client_incident')
        assessment = application.get('assessment')
        assessment_exists = False

        if assessment:
            assessment_exists = True
            assessment = application.get('assessment')[0]

        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
        pdf_canvas.setTitle(f"Assessment-Report-Claim-{str(claim_id)}")
        base_image = os.path.join(settings.BASE_DIR, "system_management", "static", 'images',
                                  'claim')
        path_cover = os.path.join(base_image, 'Cover.png')
        pdf_canvas.drawImage(path_cover, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                             mask='auto')

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 225,
                              f"{client_object['first_name']} {client_object['last_name']}")

        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 155,
                              f"{application['assessor_id__first_name']} {application['assessor_id__last_name']}")

        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(22, 80, f"{client_object['insurer__insurance_name']}")

        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(320, 225, f"{client_object['policy_no']}")

        pdf_canvas.setFont("Helvetica", 14)
        pdf_canvas.drawString(320, 155, f"{client_object['client_incident']['date_of_incident']}")

        pdf_canvas.setFont("Helvetica", 14)

        if assessment_exists:
            pdf_canvas.drawString(320, 80,
                                  f"{assessment['scheduled_date_time']}")
        else:
            pdf_canvas.drawString(320, 80, "No date scheduled")
        pdf_canvas.showPage()

        path_client = os.path.join(base_image, 'client.png')
        pdf_canvas.drawImage(path_client, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                             mask='auto')

        message_style = styles['Normal']
        message_style.textColor = HexColor('#000000')
        message_style.fontSize = 12

        msg = f"{client_object['first_name']} {client_object['last_name']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=585,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['id_number']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=540,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['phone_number']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=540,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        client_address = f"""
        {client_incident['street_address']},{client_incident['city']},{client_incident['province']},{client_incident['postal_code']}
        """

        msg = f"{client_address}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=513,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_incident['postal_code']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=445,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['policy_no']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=445,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['email']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=400,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{application['date_created']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=260,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_incident['date_of_incident']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=360,
            y=260,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        msg = f"{client_object['insurer__insurance_name']}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=220,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        claim = data.get('claim')

        application_type = f"{claim['application_type__name']}"

        msg = f"{application_type}"
        pdf_canvas = draw_paragraph(
            pdf_canvas=pdf_canvas,
            msg=msg,
            x=105,
            y=175,
            max_height=300,
            max_width=300,
            message_style=message_style
        )

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica-Bold", 25)
        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
        pdf_canvas.showPage()

        if claim:
            if claim['application_type__name'] == 'Business':
                path_business = os.path.join(base_image, 'business.png')
                pdf_canvas.drawImage(path_business, x=0, y=0, width=8.268 * inch,
                                     height=11.693 * inch,
                                     mask='auto')

                pdf_canvas.showPage()

            elif claim['application_type__name'] == 'Personal':
                path_personal = os.path.join(base_image, 'personal.png')
                pdf_canvas.drawImage(path_personal, x=0, y=0, width=8.268 * inch,
                                     height=11.693 * inch,
                                     mask='auto')
                pdf_canvas.showPage()

            path_overview = os.path.join(base_image, 'overview.png')
            pdf_canvas.drawImage(path_overview, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                                 mask='auto')

            message_style = styles['Normal']
            message_style.textColor = HexColor('#000000')
            message_style.fontSize = 18
            message_style.fontName = 'Helvetica-Bold'

            msg = f"{claim['application_type__name']}"
            pdf_canvas = draw_paragraph(
                pdf_canvas=pdf_canvas,
                msg=msg,
                x=195,
                y=485,
                max_height=300,
                max_width=300,
                message_style=message_style
            )
            if claim['application_cause'] == '':
                msg = "Unselected"
            else:
                msg = f"{claim['application_cause']['cause_id__name']}"

            pdf_canvas = draw_paragraph(
                pdf_canvas=pdf_canvas,
                msg=msg,
                x=195,
                y=380,
                max_height=300,
                max_width=300,
                message_style=message_style
            )

            if claim['application_what'] == '':
                msg = "Unselected"
            else:
                msg = f"{claim['application_what']['what_id__name']}"

            pdf_canvas = draw_paragraph(
                pdf_canvas=pdf_canvas,
                msg=msg,
                x=195,
                y=275,
                max_height=300,
                max_width=300,
                message_style=message_style
            )

            if claim['application_how'] == '':
                msg = "Unselected"
            else:
                msg = f"{claim['application_how']['how_id__name']}"

            pdf_canvas = draw_paragraph(
                pdf_canvas=pdf_canvas,
                msg=msg,
                x=195,
                y=160,
                max_height=300,
                max_width=300,
                message_style=message_style
            )

            pdf_canvas.setFillColor(HexColor('#FFFFFF'))
            pdf_canvas.setFont("Helvetica-Bold", 25)
            pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
            pdf_canvas.showPage()

            list_columns = ['title', 'questions']

            how_questions = pd.DataFrame(columns=list_columns)
            what_questions = pd.DataFrame(columns=list_columns)

            if 'details' in claim:
                details = claim['details']
                how_questions_list = details['how_questions']
                what_questions_list = details['what_questions']
                if not how_questions_list == '':
                    how_questions = pd.DataFrame(how_questions_list)
                if not what_questions_list == '':
                    what_questions = pd.DataFrame(what_questions_list)

            if not how_questions.empty and not what_questions.empty:
                how_questions = how_questions[list_columns]
                what_questions = what_questions[list_columns]
                questions = pd.concat([what_questions, how_questions])

            elif not how_questions.empty:
                questions = how_questions[list_columns]
            elif not what_questions.empty:
                questions = what_questions[list_columns]
            else:
                questions = pd.DataFrame(columns=list_columns)

            background_image = os.path.join(base_image, 'Back.png')

            message_style = styles['Normal']
            message_style.textColor = HexColor('#000000')
            message_style.fontSize = 12
            message_style.fontName = 'Helvetica'

            if not questions.empty:
                path_question = os.path.join(base_image, 'question.png')
                pdf_canvas.drawImage(path_question, x=0, y=0, width=8.268 * inch,
                                     height=11.693 * inch,
                                     mask='auto')

                y_axis = 550

                for _, title in questions.iterrows():

                    title_name = title['title']
                    question_answers_df = pd.DataFrame(title['questions'])
                    question_answers_df = question_answers_df.assign(
                        title=title_name
                    )

                    question_answers_df = question_answers_df.fillna('')
                    question_answers_df = question_answers_df.loc[
                        (question_answers_df['answer'] != "")]
                    question_answers_df = question_answers_df.loc[
                        ~(question_answers_df['answer'].isnull())]

                    list_columns = [
                        'title',
                        'question',
                        'answer',
                        'question_type',
                        'has_file'
                    ]
                    group_answers_df = question_answers_df[list_columns]
                    group_answers_df = group_answers_df.sort_values(by=['has_file'],
                                                                    ascending=False)
                    group_answers_df['answer'] = group_answers_df['answer'].apply(
                        lambda answer:
                        answer[0]['answer']
                    )
                    data = list(group_answers_df.values.tolist())

                    if not data:
                        continue

                    first_question = True

                    for question in data:

                        if type(question[2]) == list:
                            question[2] = question[2][0]

                        if str(question[3]) == 'file':
                            height = 250
                            y_axis_check = y_axis - height

                            if y_axis_check < 130:
                                y_axis = 625

                                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                pdf_canvas.setFont("Helvetica-Bold", 25)
                                pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                                pdf_canvas.showPage()
                                pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                                     height=11.693 * inch,
                                                     mask='auto')

                            if first_question:
                                pdf_canvas.setFillColor(HexColor('#C40001'))
                                pdf_canvas.setFont("Helvetica-Bold", 18)
                                pdf_canvas.drawString(20, (y_axis + 14), f"{title_name}")
                                first_question = False

                            pdf_canvas.roundRect(10, y_axis - (0.14 * inch + height), 7.8 * inch,
                                                 (0.07 * inch + height), 8,
                                                 stroke=True)
                            pdf_canvas.drawImage(str(question[2]), 25,
                                                 (y_axis - height + 30), 200, 180)

                            pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                            msg_width = stringWidth(f"{question[1]}", "Helvetica", 12)
                            pdf_canvas.rect(25, y_axis - 0.12 * inch, msg_width, 0.25 * inch,
                                            fill=True,
                                            stroke=False)

                            msg = f"{question[1]}"
                            message_style = styles['Normal']
                            message_style.textColor = HexColor('#000000')
                            pdf_canvas = draw_paragraph(pdf_canvas, msg, 30, y_axis + 0.03 * inch,
                                                        7.5 * inch, 0.25 * inch,
                                                        message_style)

                            y_axis = y_axis - (height + 40)

                        else:

                            msg = f"{question[2]}"
                            message_style = styles['Normal']
                            message_style.textColor = HexColor('#000000')
                            height = paragraph_height(pdf_canvas, question[2],
                                                      7.5 * inch,
                                                      0.75 * inch,
                                                      message_style)

                            question_height = paragraph_height(pdf_canvas, question[1],
                                                               7.5 * inch,
                                                               0.25 * inch, message_style)

                            if height < 0.75 * inch:
                                height = 0.75 * inch

                            y_diff = height + question_height
                            y_axis_check = y_axis - question_height

                            if y_axis_check < 130:
                                y_axis = 625 - question_height

                                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                                pdf_canvas.setFont("Helvetica-Bold", 25)
                                pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                                pdf_canvas.showPage()

                                pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                                     height=11.693 * inch,
                                                     mask='auto')

                            if first_question:
                                pdf_canvas.setFillColor(HexColor('#C40001'))
                                pdf_canvas.setFont("Helvetica-Bold", 18)
                                pdf_canvas.drawString(20, (y_axis + 14), f"{title_name}")
                                first_question = False

                            pdf_canvas.roundRect(
                                10,
                                y_axis - (0.14 * inch + height + (question_height / 2)),
                                7.8 * inch,
                                (0.07 * inch + height + (question_height / 2)), 8,
                                stroke=True
                            )

                            pdf_canvas = draw_paragraph(pdf_canvas, msg, 25,
                                                        (y_axis - question_height / 2) - 10,
                                                        7.5 * inch,
                                                        0.75 * inch, message_style)

                            pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                            msg_width = stringWidth(f"{question[1]}", "Helvetica", 12)

                            pdf_canvas.rect(
                                25,
                                (y_axis - question_height / 2),
                                msg_width + 20,
                                question_height + 5,
                                fill=True,
                                stroke=False
                            )

                            msg = f"{question[1]}"
                            pdf_canvas = draw_paragraph(
                                pdf_canvas,
                                msg,
                                30,
                                (y_axis + (question_height / 2)) - 5, 7.4 * inch,
                                0.25 * inch,
                                message_style
                            )

                            y_axis = y_axis - (y_diff + 40)

                    if y_axis < 255:

                        if first_question:
                            y_axis = 600

                        else:
                            y_axis = 625

                        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                        pdf_canvas.setFont("Helvetica-Bold", 25)
                        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                        pdf_canvas.showPage()
                        pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                             height=11.693 * inch, mask='auto')

            assessment_notes = claim.get('notes')

            if assessment_notes:
                path_notes = os.path.join(base_image, 'notes.png')
                pdf_canvas.drawImage(path_notes, x=0, y=0, width=8.268 * inch, height=11.693 * inch,
                                     mask='auto')
                height = 550
                for note in assessment_notes:
                    check_height = height - 250
                    if check_height <= 110:

                        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                        pdf_canvas.setFont("Helvetica-Bold", 25)
                        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                        pdf_canvas.showPage()
                        pdf_canvas.drawImage(background_image, x=0, y=0, width=8.268 * inch,
                                             height=11.693 * inch,
                                             mask='auto')
                        height = 625

                        pdf_canvas.setFont("Helvetica-Bold", 10)
                        pdf_canvas.setFillColor(HexColor('#000000'))
                        pdf_canvas.drawString(30, height, 'Note description:')
                        pdf_canvas.drawString(150, height, note['note'])
                        pdf_canvas.drawString(30, height - 15, 'Picture:')
                        height = height - 235
                        pdf_canvas.drawImage(note['file'], 30, height, width=500,
                                             height=200)

                        height = height - 15

                    else:
                        pdf_canvas.setFont("Helvetica-Bold", 10)
                        pdf_canvas.setFillColor(HexColor('#000000'))
                        pdf_canvas.drawString(30, height, 'Note description:')
                        pdf_canvas.drawString(150, height, note['note'])
                        pdf_canvas.drawString(30, height - 15, 'Picture:')
                        height = height - 235
                        pdf_canvas.drawImage(note['file'], 30, height, width=500,
                                             height=200)
                        height = height - 15

                pdf_canvas.setFillColor(HexColor('#FFFFFF'))
                pdf_canvas.setFont("Helvetica-Bold", 25)
                pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")
                pdf_canvas.showPage()

        pdf_canvas.setFillColor(HexColor('#FFFFFF'))
        pdf_canvas.setFont("Helvetica-Bold", 25)
        pdf_canvas.drawString(520, 47, f"{pdf_canvas.getPageNumber()}")

        pdf_canvas.save()

        buffer.seek(0)
        filename = f"Assessment-Report-Claim-{str(claim['id'])}.pdf"
        return FileResponse(
            buffer,
            content_type='application/pdf',
            as_attachment=False,
            filename=filename
        )


def chunks(data_list, number_per_iteration):
    """
    Break the data in chunks for overflow control.
    """
    for index in range(0, len(data_list), number_per_iteration):
        yield data_list[index:index + number_per_iteration]


def draw_list(pdf_canvas, list_items, x, y, max_width, max_height):
    """
    Create list of elements on the pdf report.
    """
    list_flowable = ListFlowable(list_items)
    _, h = list_flowable.wrapOn(pdf_canvas, max_width, max_height)
    list_flowable.drawOn(pdf_canvas, x, y - h)
    return pdf_canvas


def draw_paragraph(pdf_canvas, msg, x, y, max_width, max_height, message_style):
    """
    Draw paragraph on the pdf report.
    """
    message = str(msg).replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    _, h = message.wrap(max_width, max_height)
    message.drawOn(pdf_canvas, x, y - h)
    return pdf_canvas


def paragraph_height(pdf_canvas, msg, max_width, max_height, message_style):
    """
    Get the height of the content passed then return the height.
    """
    message = str(msg).replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    message.wrapOn(pdf_canvas, max_width, max_height)
    height = message.height
    return height


@check_token_in_session
def get_client_claims(request):
    """
    Get client claim info.

    Args:
        request(django): Django request parameter.

    Return:
        render(HTMLResponse): Render template.
    """
    if request.method == "GET":
        token = request.session.get('token')

        payload = json.dumps({
            'user_id': request.session.get('user_id')
        })
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        url = f"{host_url(request)}{reverse('get_client_claims_api')}"
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)

        applications = response_data.get('data')
        applications_df = pd.DataFrame(applications)

        if not applications_df.empty:
            completed_applications = applications_df[
                applications_df['application_status__name'] == 'Completed'
            ].to_dict('records')

            pending_applications = applications_df[
                applications_df['application_status__name'] == 'Pending'
            ].to_dict('records')

            scheduled_applications = applications_df[
                applications_df['application_status__name'] == 'Scheduled'
            ].to_dict('records')
                
        else:
            completed_applications = []
            pending_applications = []
            scheduled_applications = []

        scheduled_claims = len(scheduled_applications)
        pending_claims = len(pending_applications)
        complete_claims = len(completed_applications)
        
        context = {
            "scheduled_claims": scheduled_claims,
            "pending_claims": pending_claims,
            "complete_claims": complete_claims,
            "completed_applications": completed_applications,
            "pending_applications": pending_applications,
            "scheduled_applications": scheduled_applications
        }

        return render(request, 'claims/claims.html', context)