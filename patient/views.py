from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PatientUpdateForm
from personnel.models import Personnel

# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('home')  # Redirige vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur lors de la saisie. Veuillez réessayer.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Home page view
def home(request):
    doctors = Personnel.objects.filter(fonction__startswith="Médecin")
    return render(request, 'index.html', {'doctors': doctors})

# About us view
def about_us(request):
    return render(request, 'about_us.html')

# Contact us view
def contact_us(request):
    return render(request, 'contact_us.html')

# Update patient information view
@login_required
def update_patient(request):
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('update_patient')
    else:
        form = PatientUpdateForm(instance=request.user)
    return render(request, 'modif_patient.html', {'form': form})

# Delete patient account view
@login_required
def delete_patient(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect('home')
    return render(request, 'delete_patient.html')

# Custom dashboard view for staff members
@staff_member_required
def custom_dashboard(request):
    return HttpResponse("<h1>Welcome to the Custom Dashboard</h1>")

# Forgot password view
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send email with reset link
            reset_url = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            subject = 'Reset Your Password'
            message = f'Click the following link to reset your password: {reset_url}'
            send_mail(subject, message, 'noreply@hospital.com', [email])
            
            messages.success(request, 'Password reset email sent successfully.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'forgot_password.html')

# Reset password view
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        
        return render(request, 'reset_password.html')
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('login')

# Face login view
def face_login(request):
    # Placeholder for face recognition login functionality
    messages.info(request, 'Face recognition login feature is not implemented yet.')
    return redirect('login')

# Model results view
def model_results_view(request):
    # Placeholder for model results functionality
    return render(request, 'model_results.html')

# Download report view
def download_report(request):
    # Placeholder for report download functionality
    messages.info(request, 'Report download feature is not implemented yet.')
    return redirect('home')
