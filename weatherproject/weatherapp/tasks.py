from django.conf import settings
import requests
from django.shortcuts import render
from weatherproject.celery import app
from django.core.mail import send_mail
from .models import EmailSubscription

# @app.task
# def send_mail_task():
#    print("Mail sending.......")
#    subject = 'welcome to Celery world'
#    message = 'Hi thank you for using celery'
#    email_from = 'adebusolayeye@gmail.com'
#    recipient_list = ['aadeyeye@afexnigeria.com', ]
#    send_mail( subject, message, email_from, recipient_list )
#    return "yes"

@app.task(bind=True, ignore_result=True)
def send_mail_task(self):
   email_from = settings.EMAIL_HOST_USER
   email_subscriber = EmailSubscription.objects.all()                                          
   for subscriber in email_subscriber:
      try:
         data = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + str(subscriber.location) + '&appid=c60c8827f547529fc966ef9e1b1f77ab').json()
      except Exception as e:
         return e
      weather_city = data['name']
      weather_temp = data['main']['temp']
      weather_desc = data['weather'][0]['description']
      subject = f'Current Weather Information in {weather_city}'
      message = f'Hi, Currently temperature is {weather_temp} and description is {weather_desc}. Click on the link to stop the notification..http://127.0.0.1:8000/user/{subscriber.id}'
      if subscriber.location:
         if subscriber.is_subscribed:
            send_mail(subject, message, email_from, recipient_list=[subscriber.email, ],)



