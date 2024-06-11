from rest_framework.decorators import api_view
from rest_framework.response import Response
from headapp.models import User,Tab,Section
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes
from headapp.helpers import send_email
from django.contrib.auth import login,logout,authenticate


@api_view(['GET'])
def email_available_apiview(request):
    response = {'ok':False}
    try:
        if len(User.objects.filter(username=request.GET.get('email','.'))) == 0:
            response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def auth_me_apiview(request):
    response = {'ok':False}
    try:
        if request.user.is_authenticated and request.user.role not in ['member','request']:
            response['role'] = request.user.role
            response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    print(response)
    return Response(response)



@api_view(['POST'])
def admin_login_apiview(request):
    response = {'ok':False}
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user=user)
            response['role'] = user.role
            response['ok'] = True
        else:
            response['details'] = 'no_user_found'
    except Exception as e :
        response['details'] = str(e)
    print(response)
    return Response(response)



@api_view(['GET'])
def tabs_meta_apiview(request):
    response = {'ok':False}
    try:
        response['tabs']  = [
            {
                'id':tab.id,
                'tab_type':tab.tab_type,
                'tab_name':tab.tab_name,
                'parent_tab_name':tab.parent_tab_name
            } for tab in Tab.objects.all()
        ]
    except Exception as e:
        print('tabs_meta_apiview : ',e)
        response['details'] = str(e)
    return Response(response)



@api_view(['POST'])
def update_membership_apiview(request):
    response = {'ok':False}
    try:
        print(request.POST)
        user_id = request.POST.get('user_id')
        start_date = request.POST.get('membership_start_date')
        end_date = request.POST.get('membership_end_date')
        user_obj = User.objects.get(id=int(user_id))
        user_obj.membership_start_date = start_date
        user_obj.membership_end_date = end_date
        user_obj.save()
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)



@api_view(['POST'])
def operate_member_reqeust_apiview(request):
    response = {'ok':False}
    try:
        print(request.POST)
        user_obj = User.objects.get(id=int(request.POST.get('user_id')))
        if request.POST.get('operation') == 'accept':
            message = f'your login credentials are : {user_obj.email} , {user_obj.temp_password}'
            send_email(user_obj=user_obj,message=message)
            user_obj.temp_password = None
            user_obj.role = 'member'
            user_obj.save()
        elif request.POST.get('operation') == 'cancle':
            user_obj.delete()
            pass
        response['ok'] = True
    except Exception as e:
        print('operate_member_request_apiview : ',str(e))
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def get_notifications_apiview(request):
    response = {'ok':False}
    try:
        response['requests'] = [
            {
                'user_id':user.id,
                'username':user.username,
                'email':user.email,
                'country':user.country,
                'date_joined':user.get_date_joined,
            } for user in User.objects.filter(role='request')
        ]
        response['ok'] = True
    except Exception as e :
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
def update_subtab_apiview(request):
    response = {'ok':False}
    try:
        response['ok'] = True
        print(request.POST)
    except Exception as e: 
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
def update_section_apiview(request):
    response = {'ok':False}
    try:
        section_object = Section.objects.get(id=int(request.POST.get('section_id')))
        if request.FILES.get('image') is not None:
            section_object.image = request.FILES.get('image')
        section_object.caption = request.POST.get('caption')
        section_object.details = request.POST.get('details')
        section_object.featured = True if request.POST.get('featured') == 'on' else False
        section_object.blog = True if request.POST.get('blog') == 'on' else False
        if request.POST.get('priority') not in ['',None]:section_object.priority = request.POST.get('priority')
        section_object.save()
        response['ok'] = True
        print(request.POST)
    except Exception as e :
        response['details'] = str(e)
    return Response(response)


@api_view(['POST'])
def add_section_apiview(request):
    response = {'ok':False}
    try:
        parent_tab_id = request.POST.get('parent-tab-id')
        image = request.FILES.get('image')
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        featured = True if request.POST.get('featured') == 'on' else False
        blog = True if request.POST.get('blog') == 'on' else False
        priority = request.POST.get('priority')
        print(request.POST)
        Section.objects.create(
            tab = Tab.objects.get(id=int(parent_tab_id)),
            image = image,
            caption = heading,
            details = description,
            featured = featured,
            blog = blog,
            priority = priority,
        )
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def sections_content_apiview(request,tab_id):
    response = {'ok':False}
    try:
        response['sections'] = [
            {
                'section_id':section.id,
                'tab_name':section.tab.tab_name,
                'image':section.get_image_url,
                'caption':section.caption,
                'details':section.details,
                'featured':section.featured,
                'blog':section.blog,
                'priority':section.priority if section.priority else '',
            } for section in Section.objects.filter(tab=Tab.objects.get(id=int(tab_id)))
        ]
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def subtab_names_apiview(request):
    response = {'ok':False}
    try:
        response['subtab_names'] = [ tab.tab_name for tab in Tab.objects.filter(tab_type__in = ['menu','tab'])]
        response['ok'] = True
    except Exception as e:
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def tab_names_apiview(request):
    response = {'ok':False}
    try:
        response['tab_names'] = [
            {
                'id':tab.id,
                'tab_name': tab.tab_name,
                'tab_type':tab.tab_type,
            } for tab in Tab.objects.all()
            ]
        response['ok'] = True
    except Exception as e :
        response['details'] = str(e)
    return Response(response)


@api_view(['GET'])
def fetch_content(request):
    response = {'ok':False}
    try:
        section_objects = Section.objects.all()
        
        response['ok'] = True
    except Exception as e : 
        response['details'] = str(e)
    return Response(response)









