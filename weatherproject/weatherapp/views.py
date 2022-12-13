from django.shortcuts import render, redirect
from .forms import EmailSubscriptionForm
from django.urls import reverse, reverse_lazy
from .models import EmailSubscription, Location
from django.views.generic import ListView, FormView
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
import urllib.request
import json

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        ''' api key might be expired use your own api_key
            place api_key in place of appid ="your_api_key_here "  '''
  
        # source contain JSON data from API
  
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c60c8827f547529fc966ef9e1b1f77ab').read()
  
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
      
        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "main": str(list_of_data['weather'][0]['main']),
            "description": str(list_of_data['weather'][0]['description']),
            "icon": list_of_data['weather'][0]['icon'],
            'city': city
        }
        print(data)
        
    else:
        data ={}
    return render(request, "weatherapp/index.html", data)


# def subscription(request):
#     form = EmailSubscriptionForm

#     if request.method == "POST":
#         form = EmailSubscriptionForm(request.POST)
#         if form.is_valid():
#             my_form =form.save(commit=False)

#             return redirect ("/")

#     else:
#         form= EmailSubscriptionForm()
#     context= {'form': form}
#     return render(request, 'weatherapp/subscription.html', context)


class EmailSubscriptionFormView(FormView):
    form_class = EmailSubscriptionForm
    template_name = 'weatherapp/subscription.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        super(EmailSubscriptionFormView, self).form_valid(form)
        if form.is_valid():
            email = form.cleaned_data['email']
            location= form.cleaned_data['location']
            if EmailSubscription.objects.filter(email=email).exists():
                messages.error(self.request, "You have an email with us")
                return redirect('index')
            else:
                location= Location.objects.create(location=location)
                subscribers= EmailSubscription.objects.create(email=email, location=location)
                subscribers.save()
                messages.success(self.request, "Your information has been saved")
                return redirect('index')


class SubscribeUnsubscribeView(View):
    def get(self, request, pk):
        email_subscribe= EmailSubscription.objects.get(pk=pk)
        context= {'emailsubscribe': email_subscribe}
        return render(request, 'weatherapp/unsubscribed.html', context)


    def post(self, request, pk):
        email_subscribe= EmailSubscription.objects.get(pk=pk)
        