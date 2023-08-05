# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from misa.utils.isa_upload import upload_assay_data_files_dir
from gfiles.models import TrackTasks
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe

@shared_task(bind=True)
def upload_assay_data_files_dir_task(self, filelist, username, mapping_l, assayid, save_as_link, create_assay_details):
    """
    """

    tt = TrackTasks(taskid=self.request.id, state='RUNNING', name='Upload assay data file', user=User.objects.filter(username=username)[0])
    tt.save()

    upload_assay_data_files_dir(filelist, username, mapping_l, assayid, create_assay_details, save_as_link, self)

    tt.result = reverse('assayfile_summary', kwargs={'assayid': assayid})
    tt.state = 'SUCCESS'
    tt.save()


