from django.shortcuts import render,redirect
from .models import User, Email_otp, SellerRequest
from .services.otp_service import generate_otp, send_email_otp
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
MAX_DAILY_OTP = 10
def email_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        today = timezone.now().date()
        daily_count = Email_otp.objects.filter(
            email=email,
            created_at__date=today
        ).count()

        if daily_count >= MAX_DAILY_OTP:
            return render(request, 'accounts/login.html', {
                'error': 'OTP limit reached. Try again tomorrow.'
            })
        Email_otp.objects.filter(email=email).delete()
        otp = generate_otp()
        Email_otp.objects.create(email=email , otp=otp)
        send_email_otp(email, otp)
        request.session['email'] = email
        return redirect('verify_otp')
    return render(request, 'accounts/login.html')

MAX_VERIFY_ATTEMPTS = 5

def verify_otp(request):
    
    email = request.session.get('email')
    if not email:
        return redirect('login')
    
    if request.method == 'POST':
        otp = request.POST['otp']   
        otp_obj = Email_otp.objects.filter(email=email).first()

        if not otp_obj:
            return render(request, 'accounts/verify_otp.html', {'error':'OTP not found. Please request new one'})
        if otp_obj.is_expired():
            otp_obj.delete()
            return render(request, 'accounts/verify_otp.html', {'error':'OTP expired'})
        if otp_obj.attempts >= MAX_VERIFY_ATTEMPTS:
            otp_obj.delete()
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Too many wrong attempts. Request new OTP.'
            })

        if otp_obj.otp != otp:
            otp_obj.attempts += 1
            otp_obj.save(update_fields=['attempts'])
            return render(request, 'accounts/verify_otp.html', {
                'error': 'Invalid OTP'
            })
        
        user, created = User.objects.get_or_create(
            email = email,
            defaults= {'username' : email.split('@')[0]}
        )
        user.is_email_verified = True
        user.save()

        user = authenticate(request, email=email)
        login(request,user)
        otp_obj.delete()
        request.session.pop('email', None)
        messages.success(request, "Login Successful! Welcome to Trendism.")
        return redirect('home')
    return render(request, 'accounts/verify_otp.html')

MAX_RESEND_LIMIT = 3
def resend_otp(request):
    email = request.session.get("email")
    if not email:
        return redirect("login")
    
    otp_obj = Email_otp.objects.filter(email=email).first()
    if otp_obj and otp_obj.resend_count >= MAX_RESEND_LIMIT:
        return render(request, 'accounts/verify_otp.html', {'error' : 'Resend limit reached. wait 10 minutes'})
    Email_otp.objects.filter(email=email).delete()
    otp = generate_otp()
    Email_otp.objects.create(
        email=email, 
        otp=otp, 
        resend_count=(otp_obj.resend_count + 1) if otp_obj else 1
    )
    send_email_otp(email, otp)

    return redirect("verify_otp")

@login_required
def become_seller(request):
    if request.method == 'POST':
        
        try:
            SellerRequest.objects.create(
            user = request.user,
            shop_name = request.POST['shop_name'],
            gst_number = request.POST['gst_number'],
            address = request.POST['address']
            )
            return redirect('seller_submitted')
        except IntegrityError:
            messages.error(request,'You have already submitted a request!')
            return redirect('become_seller')
    return render(request, 'accounts/seller.html')
def seller_submitted(request):
    return render(request, 'accounts/seller_submitted.html')