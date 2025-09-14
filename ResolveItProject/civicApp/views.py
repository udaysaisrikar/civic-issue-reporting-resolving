from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Complaints, Municipality, Department
from geopy.geocoders import Nominatim

# Create your views here.
def get_same_loc_municipality(lat, lon):
    geolocator = Nominatim(user_agent="complaint_app")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        city = location.raw.get('address', {}).get('city') \
                or location.raw.get('address', {}).get('town') \
                or location.raw.get('address', {}).get('village')
        if city:
            return city.strip().lower()
    return None



def index(request):
    municipality = Municipality.objects.get(mun_id=1) 
    complaints = Complaints.objects.filter(municipality=municipality)
    return render(request, 'admin.html', {'complaints':complaints})

def home(request):
    complaints = Complaints.objects.all()
    return render(request, 'civilian.html',{"complaints":complaints})

def report_complaint(request):
    if request.method == "POST":
        description = request.POST.get("description")
        image = request.FILES.get("image")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        
        if image:
            if not latitude or not longitude:
                messages.error(request, "❌ Location is required")
                return redirect('report_complaint')
            Complaints.objects.create(
                description=description,
                image=image,
                latitude=latitude,
                longitude=longitude,
                status="PENDING",
            )

            #success message
            messages.success(request, "✅ Your report has been submitted successfully!")
            return redirect('home')

    return render(request,'civilian_report.html')



def assign_worker(request):
    complaint = Complaints.objects.order_by('-c_id').first()
    if not complaint:
        return redirect('index')
    
    if request.method == 'POST':
        worker_name = request.POST.get('worker_name')
        worker_num = request.POST.get('worker_contact')
        if worker_name and worker_num:
            complaint.worker_name = worker_name
            complaint.worker_num = worker_num
            complaint.status = 'IN_PROGRESS'
            complaint.save()

            return redirect('admin_track')
        else:
            error = "Please provide worker name and contact."
            return render(request, 'adminPentoProg.html', {'complaint': complaint, 'error': error})
        
    return render(request, 'adminPentoProg.html', {'complaint':complaint})
    

def resolve_complaint(request):
    complaint = Complaints.objects.order_by('-c_id').first()
    if not complaint:
        return redirect('index')
    
    if request.method == "POST":
        if request.FILES.get('resolved_image'):
            complaint.resolved_image = request.FILES['resolved_image']
            complaint.status = 'RESOLVED'
            complaint.save()

            return redirect('admin_track')
        else:
            error = "Please provide resolved image"
            return render(request, 'adminProgtoRes.html', {'complaint': complaint, 'error': error})
    
    return render(request, 'adminProgtoRes.html', {'complaint':complaint})
    

def connect_complaint(request):
    if request.method == 'POST':
        lat = float(request.POST.get('latitude'))
        lon = float(request.POST.get('longitude'))
        description = request.POST.get('description')

        city_name = get_same_loc_municipality(lat, lon)

        # Find matching municipality
        municipality = Municipality.objects.filter(location__iexact=city_name).first()

        # Create complaint
        Complaints.objects.create(
            description=description,
            latitude = lat,
            longitude = lon,
            municipality = municipality,
            status = 'PENDING'
        )

        return redirect('index')


def departments(request):
    return render(request, 'depts.html')


def add_department(request):

    if request.method == 'POST':
        dept_name = request.POST.get('deptName')
        person_name = request.POST.get('deptHead')
        phone = request.POST.get('phonenumber')

        if dept_name and person_name:
            Department.objects.create(     
                dept_name=dept_name,
                head_name=person_name,
                phone=phone
            )
            messages.success(request, "✅ Department added successfully!")
            return redirect('show_departments')
    return render(request, 'add_depts.html')



# Trackingss

def dept_track(request):
    complaints = Complaints.objects.all()
    return render(request, 'dept_tracking.html', {"complaints":complaints})


def civilian_track(request):
    complaints = Complaints.objects.all()
    return render(request, 'civilian_tracking.html', {"complaints":complaints})


def admin_track(request):
    complaints = Complaints.objects.all()
    return render(request, 'admin_tracking.html', {"complaints":complaints}) 


def sub_dept(request):
    return render(request, 'subDept.html')


def show_departments(request):
    departments = Department.objects.all()
    return render(request, 'depts.html',{"departments":departments})