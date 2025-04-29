from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_date
from.models import*
from .models import StudentRegistration, User_reg
# For PDF generation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import os
import csv
import random
from datetime import datetime
from django.db.models import Q


def home(request):
    return render(request, 'foresight_app/index.html')
def resources(request):
    posts=Post.objects.all()

    return render(request, 'foresight_app/resources.html',{
        'posts':posts

    })
from django.shortcuts import render, redirect
from .models import Contact

from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Contact

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        if first_name and last_name and email:
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                message=message
            )
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')  # Ensure 'contact' URL is correctly named

    return render(request, 'foresight_app/contact.html')



from django.http import JsonResponse
from .models import Contact

def toggle_replied(request):
    if request.method == 'POST':
        contact_id = request.POST.get('id')
        replied = request.POST.get('replied') == 'true'
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.replied = replied
            contact.save()
            return JsonResponse({'status': 'success'})
        except Contact.DoesNotExist:
            return JsonResponse({'status': 'not found'})
    return JsonResponse({'status': 'invalid'})


def our_team(request):
    return render(request, 'foresight_app/our_team.html')
def learning_modules(request):
    return render(request, 'foresight_app/learning_modules.html')



def student_registration_view(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('fullName')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            qualification = request.POST.get('qualification')
            course = request.POST.get('course')
            resume = request.FILES.get('resume')

            StudentRegistration.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                qualification=qualification,
                course=course,
                resume=resume
            )

            messages.success(request, 'Registration submitted successfully!')
            return redirect('home')  # 👈 change here

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('home')  # 👈 same change here

    return redirect('home')  # default fallback

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import StudentRegistration, Post, Contact
import csv
from io import StringIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required


def dashboard(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You must log in first.")
        return redirect('admin_login')

    # Get enquiry and student search parameters separately
    enquiry_query = request.GET.get('enquiry_q', '')
    enquiry_date_from = request.GET.get('enquiry_from', '')
    enquiry_date_to = request.GET.get('enquiry_to', '')

    student_query = request.GET.get('student_q', '')
    student_date_from = request.GET.get('student_from', '')
    student_date_to = request.GET.get('student_to', '')

    # Filter Students
    students = StudentRegistration.objects.all()
    if student_query:
        students = students.filter(full_name__icontains=student_query)
    if student_date_from and student_date_to:
        students = students.filter(created_at__date__range=[student_date_from, student_date_to])
    elif student_date_from:
        students = students.filter(created_at__date__gte=student_date_from)

    # Filter Enquiries
    enquiries = Contact.objects.all()
    if enquiry_query:
        enquiries = enquiries.filter(first_name__icontains=enquiry_query)
    if enquiry_date_from and enquiry_date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[enquiry_date_from, enquiry_date_to])
    elif enquiry_date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=enquiry_date_from)

    posts=Post.objects.all()
    return render(request, 'foresight_app/dashboard.html', {
        'students': students,
        'query': student_query,
        'date_from': student_date_from,
        'date_to': student_date_to,
        'enquiries': enquiries,
        'enquiry_query': enquiry_query,
        'enquiry_date_from': enquiry_date_from,
        'enquiry_date_to': enquiry_date_to,
        'posts':posts
    })

import datetime

def export_enquiries_csv(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    enquiries = Contact.objects.all()

    if query:
        enquiries = enquiries.filter(first_name__icontains=query)

    if date_from and date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[date_from, date_to])
    elif date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=date_from)

    # Get today's date and format it as YYYY-MM-DD
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')

    # Prepare CSV response with dynamic filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Enquiry_{today_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Submitted At', 'First Name', 'Last Name', 'Email', 'Phone', 'Message', 'Replied'])

    for enquiry in enquiries:
        # Convert the 'replied' field to 'YES' or 'NO'
        replied_status = 'YES' if enquiry.replied else 'NO'
        
        writer.writerow([
            enquiry.submitted_at, 
            enquiry.first_name, 
            enquiry.last_name, 
            enquiry.email, 
            enquiry.phone, 
            enquiry.message, 
            replied_status
        ])

    return response

from textwrap import wrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from textwrap import wrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from textwrap import wrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from textwrap import wrap

def export_enquiries_pdf(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    enquiries = Contact.objects.all()

    if query:
        enquiries = enquiries.filter(first_name__icontains=query)

    if date_from and date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[date_from, date_to])
    elif date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=date_from)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enquiries.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Margin calculations
    left_margin = width * 0.02
    right_margin = width * 0.98
    usable_width = width * 0.96

    # Column widths based on % of usable width
    col_widths = [
        usable_width * 0.08,  # Date
        usable_width * 0.25,  # Name
        usable_width * 0.20,  # Email
        usable_width * 0.12,  # Phone
        usable_width * 0.28,  # Message
        usable_width * 0.03   # Replied
    ]

    # Column starting x-positions
    col_x_positions = [left_margin]
    for w in col_widths[:-1]:  # Ignore last because no gap after Replied
        col_x_positions.append(col_x_positions[-1] + w)

    # Draw Header Section with "Foresight"
    def draw_header_section():
        p.setFont("Helvetica-Bold", 14)
        p.drawString(width / 2 - 50, height - 30, "Foresight")

    # Draw the table header
    def draw_table_header():
        p.setFont("Helvetica-Bold", 9)
        headers = ["Date", "Name", "Email", "Phone", "Message", "Replied"]
        for i, header in enumerate(headers):
            p.drawString(col_x_positions[i], height - 50, header)

    # Draw the entire PDF
    draw_header_section()
    draw_table_header()

    y = height - 70
    p.setFont("Helvetica", 8)

    def draw_table_row(enquiry, y_position):
        name = f"{enquiry.first_name} {enquiry.last_name}".strip()
        replied_status = 'YES' if enquiry.replied else 'NO'
        formatted_date = enquiry.submitted_at.strftime('%Y-%m-%d')

        # Prepare field text and wrap according to column width
        fields = [
            (formatted_date, col_widths[0]),
            (name, col_widths[1]),
            (enquiry.email, col_widths[2]),
            (enquiry.phone, col_widths[3]),
            (enquiry.message, col_widths[4]),
            (replied_status, col_widths[5]),
        ]

        # Estimate chars per line roughly (approx 6 pts per character at font size 8)
        field_lines = []
        for text, width_value in fields:
            chars_per_line = int(width_value / 4.5)  # Adjust ratio for neatness
            wrapped = wrap(text or '', width=chars_per_line)
            field_lines.append(wrapped)

        # Find max number of lines needed
        max_lines = max(len(lines) for lines in field_lines)

        # Draw lines
        for line_num in range(max_lines):
            for i, lines in enumerate(field_lines):
                text = lines[line_num] if line_num < len(lines) else ''
                p.drawString(col_x_positions[i], y_position, text)
            y_position -= 12

        # Draw horizontal line
        p.line(left_margin, y_position + 6, right_margin, y_position + 6)

        return y_position - 5

    # Loop through enquiries to add each to the table
    for enquiry in enquiries:
        y = draw_table_row(enquiry, y)
        if y < 80:
            p.showPage()
            draw_header_section()
            draw_table_header()
            y = height - 70

    p.save()
    return response




def delete_student(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)
    
    # Delete resume file from the filesystem if it exists
    if student.resume and os.path.isfile(student.resume.path):
        os.remove(student.resume.path)
        
    student.delete()
    return redirect('dashboard')

def edit_student(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)
    
    if request.method == 'POST':
        for field in ['full_name', 'email', 'phone', 'address', 'qualification', 'course']:
            setattr(student, field, request.POST.get(field))

        if 'resume' in request.FILES:
            # Delete old resume if it exists
            if student.resume and os.path.isfile(student.resume.path):
                os.remove(student.resume.path)
            # Save new resume
            student.resume = request.FILES['resume']
        
        student.save()
        return redirect('dashboard')

    return render(request, 'edit_student.html', {'student': student})


def export_students_csv(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    students = StudentRegistration.objects.all()

    if query:
        students = students.filter(full_name__icontains=query)

    if date_from and date_to:
        students = students.filter(created_at__date__range=[date_from, date_to])
    elif date_from:
        students = students.filter(created_at__date__gte=date_from)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Phone', 'Address', 'Qualification', 'Course', 'Created At'])

    for s in students:
        writer.writerow([
            s.full_name, s.email, s.phone, s.address,
            s.qualification, s.course,
            s.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


def export_students_pdf(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    students = StudentRegistration.objects.all()

    if query:
        students = students.filter(full_name__icontains=query)

    if date_from and date_to:
        students = students.filter(created_at__date__range=[date_from, date_to])
    elif date_from:
        students = students.filter(created_at__date__gte=date_from)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    def draw_header():
        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, height - 50, "Registered Students")

        # Date range info
        p.setFont("Helvetica", 10)
        date_info = f"From: {date_from or 'All'}   To: {date_to or 'Latest'}"
        p.drawString(40, height - 65, date_info)

        # Column headings
        p.setFont("Helvetica-Bold", 10)
        p.drawString(40, height - 80, "Full Name")
        p.drawString(150, height - 80, "Email")
        p.drawString(280, height - 80, "Phone")
        p.drawString(350, height - 80, "Course")
        p.drawString(430, height - 80, "Date")

    draw_header()
    y = height - 100
    p.setFont("Helvetica", 10)

    for s in students:
        p.drawString(40, y, s.full_name)
        p.drawString(150, y, s.email)
        p.drawString(280, y, s.phone)
        p.drawString(350, y, s.course)
        p.drawString(430, y, s.created_at.strftime('%Y-%m-%d'))
        y -= 20

        if y < 50:
            p.showPage()
            draw_header()
            p.setFont("Helvetica", 10)
            y = height - 100

    p.save()
    return response




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User_reg
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User_reg
from django.contrib.auth.hashers import make_password, check_password
def register_user(request):
    if request.method == 'POST' and 'register' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User_reg.objects.exists():
            messages.error(request, "An admin is already registered. Only one admin allowed.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif User_reg.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif User_reg.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        else:
            hashed_password = make_password(password)
            User_reg.objects.create(username=username, email=email, password=hashed_password)
            messages.success(request, "Registration successful. You can now log in.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'login', 'form_type': 'login'})

    return render(request, 'foresight_app/reg&login.html')



def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User_reg.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except User_reg.DoesNotExist:
            messages.error(request, "Invalid email or password.")

        return render(request, 'foresight_app/reg&login.html', {'active_tab': 'login'})

    return render(request, 'foresight_app/reg&login.html')

def logout_user(request):
    request.session.flush()
    return redirect('admin_login')



import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User_reg

import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import User_reg
def admin_forget(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            user = User_reg.objects.first()  # Only ONE user (admin) is there
            email = user.email
        except User_reg.DoesNotExist:
            user = None
            email = None

        if action == 'send_otp':
            if user:
                otp = random.randint(100000, 999999)
                request.session['reset_email'] = email
                request.session['otp'] = str(otp)

                send_mail(
                    subject="Foresight Password Reset OTP",
                    message=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                messages.success(request, "OTP sent to your registered email.")
            else:
                messages.error(request, "No admin user found.")

        elif action == 'verify_otp':
            otp = request.POST.get('otp')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            elif otp != request.session.get('otp'):
                messages.error(request, "Invalid OTP.")
            else:
                try:
                    user = User_reg.objects.get(email=request.session.get('reset_email'))
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, "Password reset successful. You may now log in.")
                    del request.session['reset_email']
                    del request.session['otp']
                    return redirect('admin_login')
                except User_reg.DoesNotExist:
                    messages.error(request, "User not found.")

    return render(request, 'foresight_app/forget.html', {'otp_sent': True if request.session.get('otp') else False})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpResponse, HttpResponseBadRequest

# List all posts


# Create a new post
def post_create(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if not heading or not content or not image:
            return HttpResponseBadRequest("Missing required fields.")

        Post.objects.create(heading=heading, content=content, image=image)
        return redirect('dashboard')

    return render(request, 'foresight_app/dashboard.html')

import os
from django.conf import settings

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.heading = request.POST.get('heading')
        post.content = request.POST.get('content')

        new_image = request.FILES.get('image')
        if new_image:
            # Delete the old image if it exists
            if post.image and os.path.isfile(post.image.path):
                os.remove(post.image.path)

            post.image = new_image

        post.save()
        return redirect('dashboard')

    return render(request, 'foresight_app/dashboard.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # Delete the image file first
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)

        post.delete()
        return redirect('dashboard')

    return render(request, 'foresight_app/dashboard.html', {'post': post})



from django.shortcuts import render, redirect
from .models import Contact
from django.http import JsonResponse

def enquiry_dashboard(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')
    
    enquiries = Contact.objects.all()
    
    if query:
        enquiries = enquiries.filter(first_name__icontains=query) | enquiries.filter(last_name__icontains=query)
    
    if date_from:
        enquiries = enquiries.filter(submitted_at__gte=date_from)
    
    if date_to:
        enquiries = enquiries.filter(submitted_at__lte=date_to)
    
    return render(request, 'enquiry_dashboard.html', {
        'enquiries': enquiries,
        'query': query,
        'date_from': date_from,
        'date_to': date_to
    })

def toggle_replied(request):
    if request.method == 'POST':
        enquiry_id = request.POST.get('id')
        replied_status = request.POST.get('replied') == 'true'
        
        enquiry = Contact.objects.get(id=enquiry_id)
        enquiry.replied = replied_status
        enquiry.save()
        
        return JsonResponse({'status': 'success', 'replied': enquiry.replied})
    
    return JsonResponse({'status': 'fail'}, status=400)
