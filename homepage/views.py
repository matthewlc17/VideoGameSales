from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
import json
import requests
import urllib
from decimal import Decimal

# Create your views here.
def landingpage(request):

    if request.method == 'POST':
        form = VideoGameForm(request.POST, request=request)
        if form.is_valid():
            form_data = form.cleaned_data
            platform = form_data['Platform']
            score = str(form_data['score'])
            month = form_data['release_month']
            data =  {

                "Inputs": {

                        "input1":
                        {
                            "ColumnNames": ["Global_Sales", "Platform", "score", "release_month"],
                            "Values": [ [ 0, platform, score, month ] ]
                        },        },
                    "GlobalParameters": {
                }
            }

            body = str.encode(json.dumps(data))
            url = 'https://ussouthcentral.services.azureml.net/workspaces/60d9ae6f14a8478e917edaf7323b8f9b/services/907f6ca8aa194aeba872b117b60aaf93/execute?api-version=2.0&details=true'
            api_key = 'SR8izCipUlM1tAkNM3ejqEaVNV4qso+Khy90lhlucy3XJWKEM28jSbFZlDHQmm4K44hsPfgTrDK6PI8qLweUig=='
            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
            req = urllib.request.Request(url, body, headers)
            try:
                response = urllib.request.urlopen(req)

                result = response.read()
                resultDict = json.loads(result)
                predicted_sales = round(Decimal(resultDict['Results']['output1']['value']['Values'][0][0]),2)

                predicted_sales = "{:,}".format(predicted_sales)

                print(resultDict)
                print(predicted_sales)

                # retweetCount = str(resultDict['Results']['output1']['value']['Values'][0][0])
                # count = round(float(retweetCount))
                # retweetCountRounded = count

                # print(retweetCount)

            except urllib.request.HTTPError as error:
                print("The request failed with status code: " + str(error.code))
                print(error.info())
                print(json.loads(error.read()))

            # return HttpResponseRedirect('/')
        else:
            predicted_sales = None
    else:
        form = VideoGameForm(request=request)
        predicted_sales = None
    context = {
        'form': form,
        'predicted_sales': predicted_sales,
    }

    return render(request, 'homepage/index.html', context)

class VideoGameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VideoGameForm, self).__init__(*args, **kwargs)

        PLATFORM_CHOICES = (
            ('XOne','Xbox One'),
            ('PS4','Playstation 4'),
            ('PC', 'PC'),
        )
        MONTH_CHOICES = (
            ('Jan', 'January'),
            ('Feb', 'February'),
            ('Mar', 'March'),
            ('Apr', 'April'),
            ('May', 'May'),
            ('Jun', 'June'),
            ('Jul', 'July'),
            ('Aug', 'August'),
            ('Sep', 'September'),
            ('Oct', 'October'),
            ('Nov', 'November'),
            ('Dec', 'December'),
        )

        self.fields['score'] = forms.DecimalField(label="Score", required=True, widget=forms.NumberInput(attrs={'placeholder':'Score', 'class':'form-control','style':'text-align:center;'}))
        self.fields['Platform'] = forms.ChoiceField(label="Platform", required=True, choices=PLATFORM_CHOICES, widget=forms.Select(attrs={'placeholder':'Score', 'class':'form-control','style':'text-align:center;'}))
        self.fields['release_month'] = forms.ChoiceField(label="Release Month", required=True, choices=MONTH_CHOICES, widget=forms.Select(attrs={'placeholder':'Score', 'class':'form-control','style':'text-align:center;'}))

    def clean(self):
        cleaned_data = super().clean()

        if Decimal(self.cleaned_data.get('score')) > 10:
            self._errors['score'] = self.error_class(['Score must not be greater than 10'])
        elif Decimal(self.cleaned_data.get('score')) < 0:
            self._errors['score'] = self.error_class(['Score must not be less than 0'])
