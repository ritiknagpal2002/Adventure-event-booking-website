import datetime
import uuid
import re
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .forms import ClientForm, CreateEventForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # add this
from django.template import RequestContext
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from myapp.forms import ClientForm
from myapp.models import Client, PasswordReset, AdventureType, Adventure, CreateEvent


# Create your views here.


def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in :)")
                return redirect('myapp1:homepage')
            else:
                return HttpResponse('Your account is disabled.')
        else:
            messages.error(request, "Wrong Username OR Passwords ")
            return redirect('myapp1:login')
    else:
        form1 = authenticate()
        form2 = ClientForm()
        return render(request, 'myapp/login.html', {'form1': form1, 'form2': form2})



@login_required
def homepage(request):
    msg = "Welcome to Adventures"
    types = AdventureType.objects.all()
    events = CreateEvent.objects.all()
    return render(request=request, template_name="myapp/homepage.html", context={"msg": msg, 'types': types})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reversed(('login')))


def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        # if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Username already exists.')
            messages.error(request, "Username Not Available")
            return redirect('myapp1:login')

        elif password != confirmpassword:
            form.add_error('confirmpassword', 'Passwords do not match.')
            messages.error(request, "Passwords do not match")
            return redirect('myapp1:login')

        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            form.add_error('email', 'Invalid email address')
            messages.error(request, "Invalid email address")
            return redirect('myapp1:login')

        else:
            client = form.save(commit=False)
            client.set_password(password)
            client.save()
            messages.success(request, "Signup Successful!")
            return redirect('myapp1:login')
        # else:
        #     # Handle form validation errors
        #     messages.warning(request, "Form validation error")
        #     return render(request, 'myapp/login.html')

    else:
        form2 = ClientForm()
        return render(request, 'myapp/login.html', {'form2': form2})


def forgotpassword(request):
    return render(request, 'myapp/forgotpassword.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        print(user)
        if user is not None:
            while True:
                token = uuid.uuid4().hex
                if not PasswordReset.objects.filter(token=token).exists():
                    break
            password_reset = PasswordReset.objects.create(user=user, token=token)
            print(password_reset)
            password_reset.send_reset_email()
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('myapp1:login')

        messages.error(request, 'There is no account with that email.')
    return render(request, 'myapp/forgotpassword.html')


def reset_password(request, token):
    reset_token = PasswordReset.objects.filter(token=token).first()

    if reset_token is None or reset_token.created_at < timezone.now() - timezone.timedelta(hours=1):
        messages.error(request, 'This link is no longer valid. Please try resetting your password again.')
        return redirect('myapp1:forgotpassword')

    if request.method == 'POST':
        password = request.POST['password']
        reset_token.user.set_password(password)
        reset_token.user.save()
        reset_token.delete()
        messages.success(request, 'Your password has been reset. Please log in with your new password.')
        return redirect('myapp1:login')

    return render(request, 'myapp/resetpassword.html')


@login_required
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        event_date_str = request.POST['event_date']
        event_date = datetime.datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
        form.instance.client = request.user.client
        if event_date > datetime.datetime.now():
            if form.is_valid():
                event = form.save(commit=False)
                event.client = request.user.client
                event.save()
                messages.success(request, 'Event created successfully.')
                return redirect('myapp1:homepage')
        else:
            messages.error(request, '-----invalid EventDate-----')
            return redirect('myapp1:createevent')
    else:
        form = CreateEventForm()
    return render(request, 'myapp/createevent.html', {'form': form})


def adventures_by_type(request, type_id):
    type = get_object_or_404(AdventureType, pk=type_id)
    adventures = Adventure.objects.filter(type=type)
    events = {}
    print()
    for adventure in adventures:
        events[adventure.name] = CreateEvent.objects.filter(advanture=adventure)
        temp = CreateEvent.objects.filter(advanture=adventure)

        for ev in temp:
            # ev.img = request.build_absolute_uri(ev.img)
            ev.img = ' http://127.0.0.1:8000/' + str(ev.img)
            print(ev.img)
        events[adventure.name] = temp

        # events = CreateEvent.objects.filter(advanture__in=adventures)
    return render(request, 'myapp/advanturedetail.html', {'adventures': adventures, 'events': events})


#######################################################################################################################

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from decimal import Decimal
from .forms import EventBookingForm
from .models import CreateEvent, EventBooking


# def book_event(request, event_id):
#     event = CreateEvent.objects.get(id=event_id)
#     print(request.method)
#     if request.method == 'POST':
#         form = EventBookingForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.event = event
#             booking.user = request.user
#             booking.total_amount_paid = Decimal(booking.number_of_people) * event.price
#             booking.save()
#             # return render(request, 'myapp/bookingconfirmation.html',{'event': event, 'booking': booking})
#             # Generate PDF file
#             return render(request, 'myapp/bookingconfirmation.html', {'event': event, 'booking': booking})
#             template = get_template('myapp/bookingconfirmation.html')
#             context = {'event': event, 'booking': booking}
#             html = template.render(context)
#             pdf_file = open(f'booking_confirmation_{booking.id}.pdf', 'wb')
#             pdf_file.write(html.encode('utf-16'))
#             pdf_file.close()
#             print(pdf_file)
#             # Save the PDF file to the storage
#             filename = default_storage.save(pdf_file.name, ContentFile(open(pdf_file.name, 'rb').read()))
#             print(filename)
#             # Download the PDF file
#             response = FileResponse(open(pdf_file.name, 'rb'), content_type='Downloads/pdf')
#             print(response)
#             response['Content-Disposition'] = f'attachment; filename="{pdf_file.name}"'
#             return response
#     else:
#         form = EventBookingForm()
#     return render(request, 'myapp/book_event.html', {'event': event, 'form': form})
#

def bookevent(request, event_id):
    event = CreateEvent.objects.get(id=event_id)
    print("Method: , ", request.method)
    if request.method == 'POST':
        form = EventBookingForm(request.POST)
        print(form.errors)
        booking_id = ''
        print(event)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.user = request.user
            booking.total_amount_paid = Decimal(booking.number_of_people) * event.price
            booking_id = booking.save()
            # booking_id = {booking.id}
            event_id = event.id
            name = event.name
            user = event.client.username
            ticket_size = int(request.POST['number_of_people'])
            total_amount_paid = int(ticket_size) * event.price
            return render(request, 'myapp/payment.html',
                          {'event_id': event.id, 'booking_id': booking_id, 'name': name, 'user': user,
                           'ticket_size': ticket_size, 'amount': total_amount_paid})
    else:
        form = EventBookingForm()
    return render(request, 'myapp/book_event.html', {'event': event, 'form': form})


from PIL import Image, ImageFilter


def generatepdf(request, event_id):
    event = CreateEvent.objects.get(id=event_id)
    booking = EventBooking.objects.latest('booked_at')
    print(request.method)
    if request.method == 'GET':
        # Generate PDF file
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Add background image
        img_path = 'static/myapp/img/pdf2.jpeg'  # replace with actual path to image
        img = Image.open(img_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=10))
        p.drawImage(ImageReader(blurred_img), 0, 0, width=p._pagesize[0], height=p._pagesize[1],
                    preserveAspectRatio=True)

        # Add text content
        p.setFont('Helvetica', 14)
        p.setFillColorRGB(0, 0, 0)
        p.drawCentredString(p._pagesize[0] / 2, 800, "THE TREK-TIX")
        p.drawString(100, 750, "Booking Confirmation")
        p.drawString(100, 725, f"Event Name: {event.name}")
        p.drawString(100, 700, f"Event Date: {event.event_date}")
        p.drawString(100, 675, f"Location: {event.location}")
        p.drawString(100, 650, f"Number of People: {booking.number_of_people}")
        p.drawString(100, 625, f"Total Amount Paid: {booking.total_amount_paid}")
        p.drawString(100, 600, f"Booked By: {booking.user.username}")
        p.drawString(100, 575, f"Booked at: {booking.booked_at}")
        p.save()
        buffer.seek(0)
        # Return the PDF file as a response
        return FileResponse(buffer, filename=f'booking_confirmation_{booking.id}.pdf', as_attachment=True)
    else:
        messages.error(request, "Payment Error")
    return redirect('myapp1:bookevent', {event_id})


def mainpg(request):
    user = request.user
    adventures = ["Registered Events"]
    user_events = EventBooking.objects.filter(user_id=request.user.pk)
    if len(user_events):
        user_events = map(lambda x: x.event, user_events)
    print(user_events)
    # user = request.user.client
    return render(request, 'myapp/user_profile.html', {'user': user, 'adventures': adventures, 'events': user_events})


def search(request):
    query = request.GET.get('query') or ""
    print(query)
    msg = "Welcome to Adventures"
    types = AdventureType.objects.all()
    events = CreateEvent.objects.filter(advanture__name__icontains=query)
    if len(events) > 4:
        events = events[:4]
    return render(request=request, template_name="myapp/homepage.html",
                  context={"msg": msg, 'types': types, 'query': query, 'events': events })


def clientprofilepg(request):
    user = request.user
    adventures = ["Created Events"]
    user_events = CreateEvent.objects.filter(client_id=request.user.pk)
    # if len(user_events):
    #     user_events = map(lambda x: x.name, user_events)
    # print(user_events)
    # user = request.user.client
    return render(request, 'myapp/organiser_profile.html', {'user': user, 'adventures': adventures, 'events': user_events})
