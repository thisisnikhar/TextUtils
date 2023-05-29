from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request,'index.html')


def analyze(request):
    #Get the text
    djtext = request.POST.get('text', 'default')


    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')

    purpose = ''
    analyzed = ""
    #Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        purpose = 'Removed Punctuations'

    if fullcaps == "on":
        if removepunc == "on":
            djtext = analyzed
        analyzed = ""
        for char in djtext:
            if char == ' ' or char == "\n":
                analyzed = analyzed + char
            else:
                analyzed = analyzed + char.upper()

        if len(purpose) != 0:
            purpose = purpose + " and change to all caps"
        else:
            purpose = "Change to all caps"

    if extraspaceremover == "on":
        if removepunc == "on" or fullcaps == "on":
            djtext = analyzed
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1] == " "):
                analyzed = analyzed + char

        if len(purpose) != 0:
            purpose = purpose + " and Remove Extra Space"
        else:
            purpose = "Remove Extra Space"

    if newlineremover == "on":
        if removepunc == "on" or fullcaps == "on" or extraspaceremover == "on":
            djtext = analyzed

        analyzed = djtext.replace('\n', '')
        analyzed = analyzed.replace('\r', '')

        if len(purpose) != 0:
            purpose = purpose + " and Remove New Lines"
        else:
            purpose = "Remove New Lines"

    if removepunc == "on" or fullcaps == "on" or extraspaceremover == "on" or newlineremover == "on":
        params = {'purpose': purpose, 'analyzed_text': analyzed}
        return render(request, 'analyze.html', params)
    else:
        params = {'purpose': "No purpose", 'analyzed_text': analyzed}
        return render(request, 'analyze.html', params)
