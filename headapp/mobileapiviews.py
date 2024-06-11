from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from headapp.models import User,Section,Tab,TableBooking
from headapp.helpers import *
from headapp.models import *
import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def book_personal_meeting_apiview(request):
    response = {'ok':False}
    try:
        required_params = ['date','audio','type','start_time','end_time','personal_note']
        for param in required_params:
            if request.POST.get(param) is None:
                raise Exception(f'required_parameters{required_params}')
        meets = PersonalMeeting.objects.filter(date=request.POST.get('date'))
        if len(meets) > 0 :
            for meet in meets:
                start_time = datetime.datetime.strptime(request.POST.get('start_time'),'%H:%M').time()
                end_time = datetime.datetime.strptime(request.POST.get('end_time'),'%H:%M').time()
                cond_1 = start_time >= meet.start_time and start_time <= meet.end_time
                cond_2 = end_time >= meet.end_time and end_time <= meet.end_time
                if cond_1 or cond_2:
                    raise Exception('not_available')

        PersonalMeeting.objects.create(
            user = request.user,
            date = request.POST.get('date'),
            audio = request.POST.get('audio'),
            type = request.POST.get('type'),
            start_time = request.POST.get('start_time'),
            end_time = request.POST.get('end_time'),
            personal_note = request.POST.get('personal_note')
        )
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def book_treatment_apiview(request):
    response = {'ok':False}
    try:
        session_id = request.POST.get('session_id')
        time_id = request.POST.get('time_id')
        client_id = '1'
        if not session_id or not time_id:raise Exception('both_fields_required(session_id,time_id)')
        if not client_id:raise Exception('client_id_missing')
        # response['booking_details'] = book_treatment_(session_id,time_id,user_id)
        response['booking_id'] = '85204-800-0000044591'
        response['ok'] = True
    except Exception as e :
        response['details'] = str(e)
    return  Response(response)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def profile_apiview(request):
    response = {'ok':False}
    try:
        response['profile'] = {
            'username':request.user.username,
            'firstname':request.user.first_name,
            'lastname':request.user.last_name,
            'saluation':request.user.saluation,
            'user_profile':request.user.get_user_profile_url,
            'role':request.user.role,
            'dob':request.user.date_of_birth,
            'country':request.user.country,
            'phone_number':request.user.phone_number,
            'membership_start_date':request.user.membership_start_date,
            'membership_end_date':request.user.membership_end_date,
        }
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)




@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def tabs_format_apiview(request):
    response = {'ok':False}
    try:
        response['tabs'] = [
            {
                'id':tab.id,
                'tab_type':tab.tab_type,
                'parent_tab_name':tab.parent_tab_name,
                'tab_name':str(tab.tab_name).upper(),
                'title':str(tab.title).upper(),
                'tagline':str(tab.tagline).upper(),
                'image':tab.get_image_url,
            } for tab in Tab.objects.filter(tab_type = 'tab')
        ]
        response['subtabs'] = [
            {
                'id':tab.id,
                'tab_type':tab.tab_type,
                'parent_tab_name':tab.parent_tab_name,
                'tab_name':str(tab.tab_name).upper(),
                'title':str(tab.title).upper(),
                'tagline':str(tab.tagline).upper(),
            } for tab in Tab.objects.filter(tab_type = 'subtab')
        ]
        response['ok'] = True
    except Exception as e :
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
def membership_request_apiview(request):
    response = {'ok':False}
    try:
        for field in User.get_required_fields_list():
            if request.POST.get(field) is None:
                raise Exception(f'field_required_({field})')
        username = request.POST.get('email')
        if username == '':raise Exception('email_cannot_be_null')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        country = request.POST.get('country')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        saluation = request.POST.get('saluation')
        if saluation not in ['Mr','Ms','Mrs','Dr']:raise Exception("valid_saluation_options_are('Mr','Ms','Mrs','Dr')")
        user_obj = User(username=username,first_name=firstname,last_name=lastname,email=email,country=country,role='request',temp_password=password,phone_number=phone_number,saluation=saluation)
        user_obj.set_password(password)
        user_obj.save()
        response['ok'] = True
    except Exception as e : 
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
def forgotpassword_apiview(request):
    response = {'ok':False}
    try:
        username = request.POST.get('username')
        if not username: raise Exception('username_field_required')
        user = User.objects.filter(username=username)
        if len(user) !=  1:raise Exception('user_not_found')
        user = user[0]
        response['reset_link'] = handle_forgot_password_user(user)
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def fetch_content_apiview(request):
    response = {'ok':False}
    try:
        response['tabs'] = [
            {
                'id':tab.id,
                'tab_type':tab.tab_type,
                'parent_tab_name':tab.parent_tab_name,
                'tab_name':tab.tab_name,
                'title':str(tab.title).upper(),
                'tagline':str(tab.tagline).upper(),
                'image':tab.get_image_url,
            } for tab in Tab.objects.all()
        ]
        response['sections'] = [
            {
                'id':section.id,
                'tab':section.tab.tab_name,
                'image':section.get_image_url,
                'caption':str(section.caption).upper(),
                'details':section.details,
                'featured':section.featured,
                'blog':section.blog,
                'priority':section.priority,
            } for section in Section.objects.all()
        ] 
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    # print('Returning api repsonse : ',response)
    return Response(response)



