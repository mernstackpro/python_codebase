from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from headapp.models import *
from headapp.helpers import get_notification,post_infrasys_api
import requests,xmltodict,datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.




def meeting_bookings_apiview(request):
    if not (request.user.is_authenticated and request.user.role == 'admin'):
        return redirect('/adminlogin')
    context = {}
    if request.method == 'POST':
        print(request.POST)
    all_bookings = PersonalMeeting.objects.all().order_by('-id')
    p = Paginator(all_bookings,10)
    page_number = request.GET.get('page',1)
    try:
        page_obj = p.get_page(page_number)
        last_ten = page_obj.object_list
    except PageNotAnInteger:
        page_obj = p.page(1)
        last_ten = page_obj.object_list
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        last_ten = []
    bookings_count = len(all_bookings)
    context['page_obj'] = page_obj
    context['bookings'] = last_ten
    context['bookings_count'] = bookings_count
    context['url'] = 'meeting_bookings'
    context['notifications'] , context['is_notification'] = get_notification()
    return render(request,'meeting_bookings.html',context)


def manage_credentials_view(request):
    if not(request.user.is_authenticated and request.user.role == 'admin'):
        return redirect('/adminlogin')
    context = {}
    if request.method == 'POST':
        user = User.objects.get(id=int(request.POST.get('id')),role=request.POST.get('role'))
        if request.POST.get('password') is None or request.POST.get('username') is None:context['error'] = 'Something Went Wrong !'
        else:
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password'))
            user.save()
            context['success'] = 'Credentials Successfully Updated.'
    context['users'] = User.objects.exclude(role__in=['admin', 'member','request'])
    context['url'] = 'manage_credentials'
    context['notifications'] , context['is_notification'] = get_notification()
    return render(request,'manage_credentials.html',context)



