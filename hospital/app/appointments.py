from django.shortcuts import render
from django.views import View
from .models import Directory
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
import json


bookedAppoints = [ _.date.time() for _ in Directory.objects.filter(date__date=datetime.now().date())]
format = '%A %d %B %Y %H:%M'


class BookedAppoints(View):

    def get(self, request):
        # print(request.user.first_name, request.user.last_name)
        if request.user.is_staff:
            bookings = []
            date = request.GET.get('date') if request.GET.get('date') else datetime.today().date().day
            [bookings.append({
                'name': _.name,
                'age': _.age,
                'date': f'{str(_.date.strftime(format))}',
                'book_by': _.booked_by
                })
            for _ in Directory.objects.filter(date__day=date)]
            # print("staff",request.POST, *bookings, sep='\n')       
            return render(request, 'app/Bookings.html', {'bookings': bookings, 'staff': True})

        else:
            bookings = []
            [bookings.append({
                'name': _.name,
                'age': _.age,
                'date': f'{str(_.date.strftime(format))}',
                'book_by': _.booked_by
                }) for _ in Directory.objects.filter(booked_by=f'{request.user.first_name} {request.user.last_name}') ]
            
            # print("user---", request.POST, *bookings, sep='\n')       
            return render(request, 'app/Bookings.html', {'bookings': bookings, 'user': f'{request.user.first_name} {request.user.last_name}'})





# Making slots appoinments. 
class MakingAppoints(View):

    def get(self, request):
        bookings=[]
        
        delta = timedelta(minutes=30)
        now  = datetime.now().replace(microsecond=0, second=0)
        till = datetime(day=now.day+1, month=now.month, year=now.year)
        now = now.replace(minute=30) if now.minute < 30 else now.replace(hour=now.hour+1, minute=0)
        
        while(True):
            data={}
            # print("-> ", now.strftime(format))
            if now.day == till.day:
                # print('next day')
                break
            elif now.hour < 10:
                # print('less then 10')
                now+=delta
                continue
            elif now.hour == 12 or 15 <= now.hour <= 17:
                # print('12')
                now+=delta
                continue
            else:

                data={"date": now.strftime(format),
                "available": False if now.time() in bookedAppoints else True,
                }
                now+=delta

            # print(" ", now.strftime(format))
            bookings.append(data)

        ctx = {'bookings': bookings, 'user': f'{request.user.first_name} {request.user.last_name}'}
        # print("Making appoints", request.user.username, *bookings, sep='\n')
        # print('bookedappoints', *bookedAppoints, sep='\n')
        return render(request, 'app/makebookings.html', context=ctx)



class MakingBookings(View):
    def post(self, request):

        global bookedAppoints
        user = request.user
        date = datetime.strptime(request.POST.get('date'), format)
        now = datetime.now()
        till = now + timedelta(days=1)
        
    

        print(bookedAppoints)
        if   not now.day == date.day < till.day and not date.hour >= now.hour:
            return HttpResponse("Time Error please try again. <a href='/'>Go back to home page.</a>", status=404)

        elif user.is_authenticated:

            Directory.objects.create(name=request.POST.get('name'),
            age=request.POST.get('age'), date=date, booked_by=f'{user.first_name} {user.last_name}').save()
            return HttpResponse('Succesfully created.  Click to see appointments<a href="\\appointments">&xlarr;</a>')

        else:
            return HttpResponse('Unsuccesful creating bookings.')

        

        
        