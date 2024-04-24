# Django
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render

def badRequest(request: WSGIRequest, exception):
    status = 400
    context = {
        'titleName': 'Bad Request',
        'statusCode': status,
        'description': 'Oops! Your Request Invalid',
    }
    return HttpResponseBadRequest(render(request, "error/template.html", context))

def permissionDenied(request: WSGIRequest, exception):
    status = 403
    context = {
        'titleName': 'Permission Denied',
        'statusCode': status,
        'description': 'Oops! Access Not Granted',
    }
    return HttpResponseForbidden(render(request, "error/template.html", context))

def pageNotFound(request: WSGIRequest, exception):
    status = 404
    context = {
        'titleName': 'Page Not Found',
        'statusCode': status,
        'description': 'Oops! Nothing Was Found',
    }
    return HttpResponseNotFound(render(request, "error/template.html", context))

def serverError(request: WSGIRequest):
    status = 500
    context = {
        'titleName': 'Server Error (500)',
        'statusCode': status,
        'description': 'Oops! Internal Server Error',
    }
    return HttpResponseServerError(render(request, "error/template.html", context))