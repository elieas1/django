from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from .models import Job, Resume, GeneralResume
import datetime

import urllib.request
import json
from django.conf import settings



def jobs(request):
    if request.method == 'GET':
        data = Job.objects.filter(active=True)

        return render(request, 'index/jobs.html', {
            'data': data
        })

    elif request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if file:
                fileEnd = ('.pdf', '.docx')
                if not file.name.lower().endswith(fileEnd):

                    return redirect(request.path)
                elif file.size > 1000000:

                    return redirect(request.path)
                else:
                    # clear to save
                    save = GeneralResume.objects.create(file=file)
                    save.save()


                    return redirect(request.path)
            else:
                response = HttpResponseBadRequest('')
                return response
        except:
            # file not found

            return redirect(request.path)

    else:
        # method is neither get nor post
        return redirect(request.path)


def jobListing(request, id):
    if request.method == 'GET':
        try:
            job = Job.objects.get(id=id)
            for res in job.jobResume.all():
                print(res)
            return render(request, 'index/listing.html', {'job': job})
        except:
            raise Http404()

    elif request.method == 'POST':
        # user is uploading his resume
        try:
            file = request.FILES.get('file')
            fileEnd = ('.pdf', '.docx')
            if not file.name.lower().endswith(fileEnd):
                
                return redirect(request.path)
            elif file.size > 1000000:
                
                return redirect(request.path)
            else:
                # clear to save file
                resume = Resume.objects.create(file=file)
                resume.job = Job.objects.get(id=id)
                resume.save()
                
                return redirect(request.path)

        except:
            # no file available
            try:
                
                return redirect(request.path)
            except:
                # rare case where listing is deleted while user is uploading file
                return HttpResponseRedirect(reverse('jobs'))
    else:
        # not post nor get
        return HttpResponseNotAllowed('')
