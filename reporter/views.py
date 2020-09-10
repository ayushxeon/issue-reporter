from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden ,HttpResponseNotAllowed,JsonResponse,HttpResponseServerError
import json

from .models import Report , Vote
from .forms import ReportForm
from profiles.models import UserInfo

def index_view(request):
    qs = []
    if request.user.is_authenticated:
        qs = Report.objects.filter(active=True,department=request.user.info.department,year=request.user.info.join_year,resolved=False)
    return render(request,'reporter/index.html',{'issue_list':qs})

@login_required
def resolved_view(request):
    qs = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=True)
    return render(request,'reporter/resolved.html',{'issue_list':qs})

@login_required
def close_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year):
        if(obj.active):
            obj.active = False
        else:
            obj.active = True
        obj.save()
        return redirect('reporter:close-stage')
    return HttpResponseForbidden


@login_required
def close_view(request):
    if(request.method=='POST'):
        id_ = int(request.POST.get('id',None))
        resolve_message = request.POST.get('c-line',None)
        obj = Report.objects.get(id=id_)
        obj.cr_line = resolve_message
        obj.save()
    qs = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=False)
    return render(request,'reporter/closed.html',{'issue_list':qs})


@login_required
def delete_resolve_line_view(request,pk):
    obj = Report.objects.get(id=pk)
    obj.cr_line = None
    obj.save()
    return redirect('reporter:close-stage')


@login_required
def issue_form_view(request):
    form = ReportForm()
    if request.method=='POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user_obj = UserInfo.objects.get(user=request.user)
            instance.user = user_obj
            instance.department = request.user.info.department
            instance.year = request.user.info.join_year
            instance.save()
            return redirect('reporter:index')
    return render(request,'reporter/issue-form.html',{'form':form})

@login_required
def resolve_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year):
        obj.resolved = True
        obj.save()
        return redirect('reporter:resolved')
    return HttpResponseForbidden

@login_required
def delete_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if((request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year) or (request.user == obj.user.user)):
        obj.delete()
        return redirect('reporter:index')
    return HttpResponseForbidden

@login_required
def edit_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    form = ReportForm(instance=obj)
    if(request.user==obj.user.user):
        if(request.method=='POST'):
            form = ReportForm(request.POST,instance=obj)
            if(form.is_valid()):
                form.save()
            return redirect('reporter:index')
        return render(request,'reporter/edit-issue.html',{'form':form,'issue':obj})
    return HttpResponseForbidden

@login_required
def vote_update_view(request):
    if request.method == 'POST':
        data_ = json.loads(request.body)
        id_ = data_['id']
        type = data_['type']
        try:
            report_obj = Report.objects.get(id=id_)
            vote_obj,created = Vote.objects.get_or_create(user=request.user,issue=report_obj)
        except:
            raise HttpResponseServerError
        if(type=='upvote'):
            (report_obj.upvotes)+=1
            vote_obj.type = 1
        elif(type=='downvote'):
            (report_obj.downvotes)-=1
            vote_obj.type = 0
        elif(type=='downvoted'):
            (report_obj.downvotes)+=1
            vote_obj.type = -1
        elif(type=='upvoted'):
            (report_obj.upvotes)-=1
            vote_obj.type = -1
        report_obj.save()
        vote_obj.save()
        return JsonResponse({'Success':'Voted'})
    return HttpResponseNotAllowed


@login_required
def vote_get_view(request):
    if request.method == 'POST':
        data_ = json.loads(request.body)
        id_ = data_['id']
        report_obj = Report.objects.get(id=id_)
        data = {}
        obj,created = Vote.objects.get_or_create(user=request.user,issue=report_obj)
        type_ = obj.type
        if(type_ == 1):
            data = {'type':'upvoted'}
        elif(type_ == 0):
            data = {'type':'downvoted'}
        elif(type_ == -1):
            data = {'type':'none'}
        return JsonResponse(data)
    return HttpResponseNotAllowed
