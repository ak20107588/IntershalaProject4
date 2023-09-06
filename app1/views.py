from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import*
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pytz
from .calendar_api import create_calendar_event
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from google.oauth2 import service_account
from django.contrib.auth.decorators import login_required



# Create your views here.

def dashboard(request):
    if request.session.has_key('is_logged'):
        return render(request,'dashboard.html')
    messages.warning(request,'Please Login!')
    return redirect('/')


def doctor(request):
    if request.session.has_key('is_logged'): 
        return render(request,'doctor.html')
    messages.warning(request,'Please Login!')
    return redirect('/')

def messages1(request):
    return render(request,'messages.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def signup(request):
    data=User.objects.all()
    return render(request,'login.html')

def login(request):
    return render(request,'login.html')

def navbar(request):
    if request.session.has_key('is_logged'):
        data=User.objects.all()
        return render(request,'navbar.html',{'Result':data})
    messages.warning(request,'Please Login!')
    return redirect('/')


def blog(request):
    if request.session.has_key('is_logged'):
        return render(request,'blog.html')
    messages.warning(request,'Please Login!')
    return redirect('/')

def nodata(request):
    if request.session.has_key('is_logged'):
        return render(request,'nodata.html')
    messages.warning(request,'Please Login!')
    return redirect('/')

def blogdata(request):
    if request.session.has_key('is_logged'):
        data=Blog.objects.all()
        return render(request,'blog.html')
    messages.warning(request,'Please Login!')
    return redirect('/')
    

def blogdetail(request,id):
    if request.session.has_key('is_logged'):
        data=Blog.objects.filter(id=id)
        return render(request,'blogdetail.html',{'Data':data})
    messages.warning(request,'Please Login!')
    return redirect('/')
    

def allblogs(request):
    if request.session.has_key('is_logged'):

        data=Blog.objects.filter(IsDraft=False)

        return render(request,'allblogs.html',{'Data':data})
        # if Blog.objects.all(IsDraft='No'):
        #     return render(request,'allblogs.html',{'Data':data})
        # else:
        #     return render(request,'nodata.html')

        # if data is None :
        #     return render(request,'nodata.html')
            
        # else:
        #     return render(request,'allblogs.html',{'Data':data})
    messages.warning(request,'Please Login!')
    return redirect('/')



def draftblog(request):
    if request.session.has_key('is_logged'):
        
        data=Blog.objects.filter(IsDraft=True)
        return render(request,'draftblog.html',{'Data':data})
    
    messages.warning(request,'Please Login!')
    return redirect('/')


def drlist(request):
    if request.session.has_key('is_logged'):
        data=User.objects.filter(UserType='Doctor')
        data1=User.objects.all()

        return render(request,'drlist.html',{'Result':data,'Data':data1})
    messages.warning(request,'Please Login!')
    return redirect('/') 


def patientdetail(request):
    if request.session.has_key('is_logged'):
        data=User.objects.filter(UserType='Patient')
        return render(request,'patientdetail.html',{'Result':data})
    messages.warning(request,'Please Login!')
    return redirect('/')  

def base(request):
    return render(request,'base.html')

def signup_detail(request):
    FirstName=(request.POST['firstname'])
    LastName=(request.POST['lastname'])
    ProfilePicture=(request.FILES['profilepicture'])
    UserName=(request.POST['username'])
    Email=(request.POST['email'])
    Address=(request.POST['address'])+","+(request.POST['city'])+","+(request.POST['state'])+","+(request.POST['pincode'])
    UserType=(request.POST['usertype'])
    Password=(request.POST['password'])
    ConfirmPassword=(request.POST['confirmpassword'])

    lower_email=Email.lower()

    print("Email value: ",Email)


    if Password==ConfirmPassword:

        data={
            "FirstName":FirstName,
            "LastName":LastName,
            "ProfilePicture":ProfilePicture,
            "UserName":UserName,
            "Email":lower_email,
            "Address":Address,
            "UserType":UserType,
            "Password":Password,
            "ConfirmPassword":ConfirmPassword,
        }

        a=User(FirstName=FirstName,LastName=LastName,ProfilePicture=ProfilePicture,UserName=UserName,Email=lower_email,Address=Address,UserType=UserType,Password=Password,ConfirmPassword=ConfirmPassword)

        if User.objects.filter(Email=lower_email).exists():

            messages.error(request,'Email Already Exist!')
            return redirect('/')
        
        if User.objects.filter(UserName=UserName).exists():
            messages.error(request,'Username Already Exist!')
            return redirect('/')
        
        
        else:
            
            a.save()
            request.session['is_logged']=True


            user_type=a.UserType=='Doctor'
            user_type1=a.UserType=='Patient'
            request.session['FirstName']=a.FirstName
            request.session['LastName']=a.LastName
            request.session['ProfilePicture']=a.ProfilePicture
            request.session['UserName']=a.UserName
            request.session['Email']=a.Email
            request.session['Address']=a.Address
            request.session['UserType']=a.UserType
            request.session['Password']=a.Password
            request.session['UserID']=a.UserID
            request.session['user_type']=user_type
            request.session['user_type1']=user_type1


            if a.UserType=='Doctor':
                user_type=a.UserType=='Doctor'
                request.session['user_type']=user_type
                messages.success(request,'Signup Success.')
                return render(request,'doctor.html',{'Result':a})
            else:
                
                return render(request,'dashboard.html',{'Result':a})
    else:
        messages.error(request,'Password & Confirm Password Not Match!')
        return redirect('/')
    
   

def login_detail(request):
    Email=(request.POST['email'])
    Password=(request.POST['password'])
    lower_email=Email.lower()
    print("Email Login & Password:",Email,Password)
    print(Email)

    try:
        context=User.objects.get(Email=lower_email)

        if User.objects.get(Email=lower_email):
            print("New Email:",Email)
            if (Password==context.Password):
                print("password new:",Password)
                print("usertype:",context.UserType)

                user_type=context.UserType=='Doctor'
                user_type1=context.UserType=='Patient'
                print("user_type:",user_type)
                request.session['FirstName']=context.FirstName
                request.session['LastName']=context.LastName
                request.session['ProfilePicture']=context.ProfilePicture
                request.session['UserName']=context.UserName
                request.session['Email']=context.Email
                request.session['Address']=context.Address
                request.session['UserType']=context.UserType
                request.session['Password']=context.Password
                request.session['UserID']=context.UserID
                request.session['user_type']=user_type
                request.session['user_type1']=user_type1
               
                
                if context.UserType=='Doctor':
                    request.session['is_logged']=True
                    
                    return render(request,'doctor.html',{'Result':context})
                else:
                    print("new:",Password)                   
                    request.session['is_logged']=True
                    return render(request,'dashboard.html',{'Result':context})
                
            else:
                messages.error(request,'Invalid Password !')
                return redirect('/')
            
    except:

        messages.error(request,'Invalid Email !')
        return redirect('/')
    

def NewBlog(request):
    if request.session.has_key('is_logged'):
        Title=(request.POST['title'])
        BlogImages=(request.FILES['blogimg'])
        Category=(request.POST['category'])
        Summary=(request.POST['summary'])
        Content=(request.POST['content'])
        IsDraft=(request.POST['isdraft'])


        data={
            "Title":Title,
            "BlogImages":BlogImages,
            "Category":Category,
            "Summary":Summary,
            "Content":Content,
            "IsDraft":IsDraft
        }

        a=Blog(Title=Title,BlogImages=BlogImages,Category=Category,Summary=Summary,Content=Content,IsDraft=IsDraft)
        a.save()

        

        request.session['Title']=a.Title
        request.session['BlogImages']=a.BlogImages
        request.session['Category']=a.Category
        request.session['Summary']=a.Summary
        request.session['Content']=a.Content
       


        return render(request,'doctor.html')
    messages.warning(request,"Please Login!")
    return redirect('/')




def post_list(request):
    categories = Blog.objects.all()
    selected_category_id = request.GET.get('category')
    

    if selected_category_id:
        posts = categories.filter(Category=selected_category_id)

    context = {
        'categories': categories,
        'selected_category_id': int(selected_category_id) if selected_category_id else None,
        'posts': posts,
    }

    return render(request, 'allblogs.html', context)


def blogcategory(request,category):
    data=Blog.objects.filter(Category=category)
    return render(request,'allblogs.html')


def get_items(request):
    if request.is_ajax() and request.method == "GET":
        category = request.GET.get['category']
        items = Blog.objects.filter(Category=category)
        return render(request,'allblogs.html')
    #     item_list_html = ""
        
    #     for item in items:
    #         item_list_html += f"<li>{item.name}</li>"
        
    #     return JsonResponse({'items': item_list_html})
    
    # return JsonResponse({'error': 'Invalid request'}, status=400)


def filter_items(request):
    category = request.GET.get('category')
    
    if category:
        items = Blog.objects.filter(Category=category).filter(IsDraft=False)
    else:
        items = Blog.objects.filter(IsDraft=False)
    
    return render(request, 'allblogs.html', {'Data': items})

def errormsg(request):
    return render(request,'errormsg.html')

def bookappoint(request,UserID):
    if request.session.has_key('is_logged'):
        data=User.objects.get(UserID=UserID)
        return render(request,'bookappoint.html',{'Result':data}) 
    messages.warning(request,"Please Login!")
    return redirect('/')   


def appointmentdetail(request,UserID):
    if request.session.has_key('is_logged'):
        data=User.objects.get(UserID=UserID)
        data3=(request.session.get('UserID'))
        # data1= Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data.UserID).exists()

        # if Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data.UserID).exists():
        if Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data3):
            user2=(request.session.get('UserID'))
            
            data3=User.objects.all()
            data1=Appointment.objects.filter(PatientID=user2)
        
            messages.error(request,'Already Appointment Booked !')
            return render(request,'errormsg.html',{'Data':data1})
        else:
            user=User.objects.get(UserID=UserID)
            user3=Appointment.objects.filter(DoctorID_id=user.UserID)
            print("UserID id:",user)
            print("Apoint UserId:", user3)
            user2=(request.session.get('UserID'))
            print("session UserId:", user2)

            Speciality=request.POST['speciality']
            AppointDate=datetime.strptime(request.POST['appointdate'], '%Y-%m-%d').date()
            AppointStart=request.POST['appointstart']
            

            data={
                'Speciality':Speciality,
                'AppointDate':AppointDate,
                'AppointStart':AppointStart
            }

            #Appoint Start Time working
            start_time_str = AppointStart
            start_time = datetime.strptime(start_time_str, '%H:%M',).time()



            #Appoint End Time
            # end_datetime = datetime.combine(AppointDate, start_time) + timedelta(minutes=45)
            # AppointEnd = end_datetime.time()
            start_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = start_datetime + timedelta(minutes=45)
            end_time = end_datetime.time().strftime('%I:%M %p')
            AppointEnd=end_time

            firstname=(request.session.get('FirstName'))
            lastname=(request.session.get('LastName'))

            a=Appointment(Speciality=Speciality,DoctorName=user.FirstName + " "+ user.LastName,PatientName=firstname + " "+ lastname, AppointDate=AppointDate,AppointStart=start_time,AppointEnd=AppointEnd,DoctorID_id=user.UserID,PatientID=user2)   

            a.save()

            b=Appointment.objects.filter(PatientID=user.UserID)

            request.session['PatientID']=a.PatientID
            request.session['Speciality']=a.Speciality
            request.session['AppointDate']=a.AppointDate
            request.session['AppointStart']=a.AppointStart

            request.session['formatstart']=AppointStart

            request.session['drfname']=user.FirstName
            request.session['drlname']=user.LastName

            request.session['endtime']=a.AppointEnd


            user2=(request.session.get('UserID'))
            data3=User.objects.all()
            data1=Appointment.objects.filter(PatientID=user2)
            

            event_id = create_calendar_event(user.FirstName + " "+ user.LastName,a.AppointDate, a.AppointStart, a.AppointEnd)
            
            # value={create_calendar_event}
            # value['Name']=a.DoctorName
            # value['AppointDate']=a.AppointDate
            # value['AppointStart']=a.AppointStart
            # value['AppointEnd']=a.AppointEnd
            # value['PatientName']=a.PatientName

            # val=json.dumps(a,default=str)
            # print("json val: ",val)

            return render (request,'appointment_confirmation.html', {'event_id': event_id, 'appointment': a})
    messages.warning(request,"Please Login!")
    return redirect('/')


# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def get_google_calendar_service(credentials):
#     flow = InstalledAppFlow.from_client_config(settings.GOOGLE_CALENDAR_CLIENT_SECRET, SCOPES)
#     creds = flow.credentials

#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#         return build('calendar', 'v3', credentials=creds)
#     return None




# def book_appointment(request,UserID):

#     if request.session.has_key('is_logged'):
#         data=User.objects.get(UserID=UserID)
#         data3=(request.session.get('UserID'))
#         # data1= Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data.UserID).exists()
#         # if Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data.UserID).exists():
#         if Appointment.objects.filter(DoctorID_id=data.UserID).filter(PatientID=data3):
#             user2=(request.session.get('UserID'))
            
# #             data3=User.objects.all()
#             data1=Appointment.objects.filter(PatientID=user2)
        
#             messages.error(request,'Already Appointment Booked !')
#             return render(request,'errormsg.html',{'Data':data1})

#         if request.method == 'POST':

#             doctor = User.objects.get(UserID=UserID)

#             firstname=(request.session.get('FirstName'))
#             lastname=(request.session.get('LastName'))
#             data3=(request.session.get('UserID'))

#             Speciality=request.POST['speciality']
#             AppointDate = datetime.strptime(request.POST['appointdate'], '%Y-%m-%d').date()
#             AppointStart = datetime.strptime(request.POST['appointstart'], '%H:%M').time()

#             # start_time = datetime.combine(AppointDate, AppointStart )
#             # end_time = start_time + timedelta(minutes=45)

            
#             start_time = datetime.combine(datetime.today(), AppointStart)
#             end_datetime = start_time + timedelta(minutes=45)
#             end_time = end_datetime.time().strftime('%I:%M %p')
            

#             # Create an appointment
#             appointment = Appointment.objects.create (
#                 DoctorName=doctor.FirstName+" "+doctor.LastName,
#                 DoctorID_id=doctor.UserID,
#                 Speciality=Speciality,
#                 AppointDate=AppointDate,
#                 AppointStart=AppointStart,
#                 AppointEnd=end_time,
#                 PatientName=firstname+" "+lastname,
#                 PatientID=data3,
#             )
#             # Create Google Calendar event
#             service = get_google_calendar_service(doctor.calendar_credentials)
#             if service:
#                 event = {
#                     'summary': f'Appointment with {Appointment.DoctorName}',
#                     'start': {'dateTime': start_time.isoformat()},
#                     'end': {'dateTime': end_time.isoformat()},
#                 }
#                 created_event = service.events().insert(calendarId='primary', body=event).execute()
#                 appointment.google_event_id = created_event['id']
#                 appointment.save()

#             return render(request, 'appointment_confirmation.html', {'appointment': appointment})
#         else:
#             doctors = User.objects.all()
#             return render(request, 'book_appointment.html', {'doctors': doctors})
        
#     messages.warning(request,"Please Login!")
#     return redirect('/')
        

def detailapoint(request):
    if request.session.has_key('is_logged'):
        return render(request,'appointdetail.html')
    messages.warning(request,"Please Login!")
    return redirect('/')

def appointdetail(request):
    if request.session.has_key('is_logged'):
        user2=(request.session.get('UserID'))
        data3=User.objects.all()
        data1=Appointment.objects.filter(PatientID=user2)

        return render(request,'appointdetail.html',{'Data':data1})
    
    messages.warning(request,"Please Login!")
    return redirect('/')

def drappoint(request):
    if request.session.has_key('is_logged'):
        user2=(request.session.get('UserID'))
        data=User.objects.all()
        data1=Appointment.objects.filter(DoctorID_id=user2)

        return render(request,'drappoint.html',{'Data':data1})
    messages.warning(request,"Please Login!")
    return redirect('/') 


# def chat(request, recipient_id):
#     recipient = User.objects.get(UserID=recipient_id)
#     userID=(request.session.get('UserID'))
#     fname=(request.session.get('FirstName'))
#     lname=(request.session.get('LastName'))

#     # data1=Message.objects.all()
#     # data=User.objects.filter(UserID=data1.sender)
    
    
#     if request.method == 'POST':
#         content = request.POST.get('message_content')
#         message = Message(sender=recipient, recipient=recipient, content=content,DoctorID=recipient.UserID,PatientID=userID,SenderName=fname+" "+lname,ReceiverName=recipient.FirstName+" "+recipient.LastName)
#         message.save()

#     if Message.objects.filter(DoctorID=recipient.UserID).exists() and Message.objects.filter(PatientID=userID).exists():
#         messages = Message.objects.filter(
#             (models.Q(sender=recipient) & models.Q(recipient=recipient)) |
#             (models.Q(sender=recipient) & models.Q(recipient=recipient))
#         )
        
        

#         return render(request, 'chat.html', {'recipient': recipient, 'messages': messages})

#     return render(request, 'chat.html', {'recipient': recipient})



def room(request,RoomName):
    username = (request.session.get('UserName'))
    # data=(request.session.get('UserName'))
    RoomId = Room.objects.get(RoomName=RoomName)
    # print("room name details",RoomName1.id)
    # room_details = Room.objects.filter(DrUser=data3,PtUser=data2)
    # print("username data1:",data3)
    return render(request, 'room.html', {
        'username': username,
        'room': RoomName,
        # 'room1':data,
        'room_id': RoomId.id
    })

def checkview(request,UserName):
    # data1=User.objects.get(UserName=ChatName)
    # data=Room.objects.filter(DrUser=data1.UserName)
    LoginName=(request.session.get('UserName'))
    LoginUserRole=(request.session.get('UserType'))
    # print("username data:",data2)
    # data3=data.
    if(LoginUserRole=="Doctor"):
        RoomName=LoginName + "_"+UserName
    if(LoginUserRole=="Patient") :
        RoomName=UserName+"_"+LoginName

    if Room.objects.filter(RoomName=RoomName).exists():
        # return redirect('/''?username='+data'/?username='+data2)
            return redirect('/'+RoomName+'/?username='+UserName)
    else:
        new_room = Room.objects.create(RoomName=RoomName) 
        new_room.save()
        # return redirect('/''?username='+data'/?username='+data2)
        return redirect('/'+RoomName+'/?username='+UserName)
    
        
        

def send(request):
    message = request.POST['message']
    username = request.POST['username']

    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, room=room_id,user=username)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(RoomName=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})



        


