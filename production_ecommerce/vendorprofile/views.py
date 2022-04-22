from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib import auth
from vendorprofile.models import  Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


import sys

import os
import datetime
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
loc = os.path.join(__location__, 'media/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, 'media')



def rhome(request):
    return HttpResponseRedirect('/home/')
def cpath(fpath):
    return os.path.join(__location__, fpath)
def onTeacher(request):
      if request.session.get('teacher'):
         return Teacher.objects.get(emailId=request.session.get('teacher'))
      else:
         return None



def index(request):
    if request.session.get('teacher',None):
        unsetDepartmentCourseBatch(request)
        teacher=onTeacher(request)
        return render(request,'vendorprofile/home.html',{"user":teacher,'range':range(2010,2222)})
    else:

       return HttpResponseRedirect('/')



def isLogin(func):
      def newFunc(request):
          if onTeacher(request) == None :
                  return HttpResponseRedirect("/login/")
          else:
             return func(request)
      return newFunc

def login(request):
    error=""
    if request.POST:
     data=request.POST
     emailId=data.get('emailId')
     password=data.get('password')
     print (emailId,password)
     flag=False
     try:
          teacher=Teacher.objects.get(emailId=emailId)

          if teacher.emailId==emailId and teacher.password==password:
               flag=True
               request.session['teacher']=emailId
               return HttpResponseRedirect('/home')
          else:
               flag=False
     except Exception as e:
          error=e
    return render(request,'vendorprofile/login.html',{"error":error})


@isLogin
def logout(request):
      del request.session['teacher']
      return HttpResponseRedirect('/home')


@isLogin
def help(request):
      teacher = onTeacher(request)
      return render(request,'vendorprofile/help.html',{'user':teacher})
#-----------------------------------------------------------------------#



#-----Admin -------------#
@login_required(login_url='/admin/login/')
def adminhelp(request):
     user={}
     return  render(request,'vendorprofile/adminhelp.html',{'user':user})

@login_required(login_url='/admin/login/')
def admin(request):
     user={}
     return  render(request,'vendorprofile/admin.html',{'user':user})


@login_required(login_url='/admin/login/')
def domore(request):
     user={}
     return render(request,'vendorprofile/domore.html',{'user':user})
