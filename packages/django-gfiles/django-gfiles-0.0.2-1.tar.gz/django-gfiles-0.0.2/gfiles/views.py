# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import os
import copy
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.http import JsonResponse
from celery.result import AsyncResult

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, MultiTableMixin

from gfiles.models import GenericFile, TrackTasks
from gfiles.forms import GFileForm
from django.shortcuts import render
from django.views.generic import View

from gfiles.filter import GFileFilter, TrackTasksFilter
from gfiles.tables import GFileTableWithCheck, TrackTasksTable

from django_tables2.export.views import ExportMixin
from django.urls import reverse_lazy
from celery.task.control import revoke

class GFileCreateView(LoginRequiredMixin, CreateView):
    """ Class to create a save a generic file using the GenericFile model.

    Inherits the CreateView class and uses the LoginRequiredMixin
    """
    model = GenericFile
    success_msg = "File uploaded"
    success_url = reverse_lazy('success')
    form_class = GFileForm
    template_name = 'gfiles/gfile_form.html'

    def update_form(self, form):
        ofn = self.request.FILES['data_file'].name
        form.instance.original_filename = ofn
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form = self.update_form(form)
        return super(GFileCreateView, self).form_valid(form)


class GFileListView(ExportMixin, SingleTableMixin, FilterView):
    """ Class to view a table and filter all of the currently saved GenericFiles

    Inherits the FilterView class and uses the SingleTableMixin for viewing the django-tables2 table and
    uses the ExportMixin so that the table can be exported as a csv file
    """
    table_class = GFileTableWithCheck
    model = GenericFile
    template_name = 'gfiles/gfile_summary.html'
    filterset_class = GFileFilter


class TrackTasksListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """ Class to view a table and filter all of the currently saved GenericFiles

    Inherits the FilterView class and uses the SingleTableMixin for viewing the django-tables2 table and
    uses the ExportMixin so that the table can be exported as a csv file
    """
    table_class = TrackTasksTable
    model = TrackTasks
    template_name = 'gfiles/tracktask_summary.html'
    filterset_class = TrackTasksFilter

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return self.model.objects.none()
        qs = self.model.objects.filter(user=self.request.user)
        return qs


class TrackTasksProgressView(LoginRequiredMixin, View):
    """
    """
    def get(self, request, *args, **kwargs):


        tt = TrackTasks.objects.filter(pk=self.kwargs['pk'])

        if tt:
            request.session['result'] = tt[0].taskid

        return render(request, 'gfiles/status.html', {'s': 0, 'progress': 0})


class TrackTasksDeleteView(DeleteView):
    model = TrackTasks
    success_url = reverse_lazy('track_tasks')
    template_name = 'gfiles/confirm_delete.html'

    def post(self, request, *args, **kwargs):
        tt = self.get_object()
        revoke(tt.taskid, terminate=True)
        return self.delete(request, *args, **kwargs)

def async_task_progress(id):
    # https://blog.miguelgrinberg.com/post/using-celery-with-flask

    # Task has finished and information has been removed (i think)
    try:
        task = AsyncResult(id)
    except KeyError as e:
        print(e)
        # check if still have info in our database table regarding this task
        tt = TrackTasks.objects.filter(taskid=id)
        if tt:
            response = {
                'state': 'COMPLETED',
                'current': 1,
                'total': 1,
                'status': 'Task {} has completed'.format(tt[0].name),
            }
        else:
            response = {
                'state': 'REMOVED',
                'current': 1,
                'total': 1,
                'status': 'Task has been removed',
            }

        return JsonResponse(response)

    info = copy.deepcopy(task.info)  # incase things change or rabbit/redis deletes message
    if task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': info['status'] if info and 'status' in info else '',
        }
        tt = TrackTasks.objects.filter(taskid=id)
        if tt and tt[0].result:
            response['status'] = mark_safe('<p><a href="{}">View result</a></p>'.format(tt[0].result))


    elif task.state == 'PENDING':
        print('pending')
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':

        response = {
            'state': task.state,
            'current': info['current'],
            'total': info['total'],
            'status': info['status'],
        }
        # if 'result' in info:
        #     response['result'] = info
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 0,
            'total': 0,
            'status': 'FAILURE (unknown)',
        }



    if response['state']=='FAILURE-KNOWN':
        response['state'] = 'FAILURE'

    if response['state'] == 'FAILURE':
        tt = TrackTasks.objects.filter(taskid=id)
        if tt:
            tt[0].state = 'FAILURE'
            tt[0].save()

    if task.state == 'SUCCESS':
        response['progress'] = 100
    elif task.info:
        if float(response['total']) == 0:
            response['progress'] = 0
        else:
            response['progress'] = (float(response['current']) / float(response['total'])) * 100.0
    else:
        response['progress'] = 0

    return response

def status_update(request):
    """ Updates for tracking status of long processes via celery
    """

    id = request.session['result']
    response = async_task_progress(id)

    return JsonResponse(response)

# class DeleteMessages(LoginRequiredMixin, View):
#     """
#     """
#     def get(self, request, *args, **kwargs):
#
#         messages = get_messages(request)
#         for msg in messages:
#             del msg
#
#         next = request.POST.get('next', '/')
#         return HttpResponseRedirect(next)





def index(request):
    """ basic index view
    """
    return render(request, 'gfiles/index.html')


def success(request):
    """ basic success view
    """
    return render(request, 'gfiles/success.html')

def handler404(request):
    return render(request, 'gfiles/404.html', status=404)

def handler500(request):
    return render(request, 'gfiles/500.html', status=500)