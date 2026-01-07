import math
import time
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from .models import Brankas
from .forms import BrankasForm

def posts_list(request):
    return render(request, 'posts/posts_list.html')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else :
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        fail_key = f'login_fail_{username}'
        block_key = f"login_blocked_{username}"
        unblock_timestamp = cache.get(block_key)
        if unblock_timestamp:
            sisa_detik = unblock_timestamp - time.time()
            if sisa_detik > 0 :
                menit = math.ceil(sisa_detik/60)
                messages.error(request, f"Akun terkunci. silahkan coba lagi dalam {menit} menit")
                return render(request, "login.html", {"form": form})
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            cache.delete(fail_key)
            cache.delete(block_key)
            return redirect('dashboard')
        else:
            try:
                fails = cache.incr(fail_key)
            except ValueError:
                cache.set(fail_key, 1, 86400)
                fails = 1
        if fails >= 5:
            timeout = 15*60
            waktu_bebas = time.time() + timeout
            cache.set(block_key, waktu_bebas, timeout)
            messages.error(request, "Gagal 5x. Akun di kunci selama 15 menit")
        else:
            sisa = 5 - fails
            messages.error(request, f"Username atau Password Salah. Sisa percobaan adalah : {sisa}")
    
    else :
        form = AuthenticationForm()
    return render (request, 'login.html', {'form':form})

def logout_view(request):
        logout(request)
        return redirect('login')

@never_cache
@login_required(login_url='login')
def dashboard_view(request):
    if request.method == "POST":
        form = BrankasForm(request.POST, request.FILES)
        if form.is_valid():
            brankas_baru=form.save(commit=False)
            brankas_baru.user=request.user
            brankas_baru.save()
            messages.success(request, "Data berhasil di simpan")
            return redirect('dashboard')
        else :
            messages.error(request, "Gagal Upload, Periksa Format anda")
    else :
        form = BrankasForm()
    
    data_brankas = Brankas.objects.filter(user=request.user).order_by('-waktu_dibuat')[:10]
    context = {
        'form' : form,
        "files" : data_brankas
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def download_brankas(request, brankas_id):
    item = get_object_or_404(Brankas, pk=brankas_id)
    if item.user != request.user:
        raise PermissionDenied("Akses ditolak")
    if item.file_rahasia:
        try:
            ext = os.path.splitext(item.file_rahasia.name)[1]
            safe_filename = f"{slugify(item.judul)}{ext}"
            return FileResponse(
                item.file_rahasia.open(),
                as_attachment=True,
                filename = safe_filename)
        except FileNotFoundError:
            raise Http404("File tidak ada")
    elif item.catatan:
        response = HttpResponse(item.catatan, content_type='text/plain')
        name_clean = slugify(item.judul) if item.judul else "catatan"
        safe_filename = f"{name_clean}.txt"
        response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
        return response
    else :
        messages.error(request, "Item tidak ada")
        return redirect("dashboard")

@login_required(login_url='login')
def delete_brankas(request, brankas_id):
    if request.method == 'POST':
        item = get_object_or_404(Brankas, pk=brankas_id)
        if item.user != request.user:
            raise PermissionDenied 
        password_input = request.POST.get("password_confirm")
        if request.user.check_password(password_input):
            item.delete()
            messages.success(request, "Data berhasil dihapus")
        else:
            messages.error(request, "Password salah")
    return redirect("dashboard")

@never_cache
@login_required(login_url='login')
def brankas_list_view(request):
    semua_data = Brankas.objects.filter(user=request.user).order_by('-waktu_dibuat')
    context = {
        'files': semua_data
    }
    return render(request, 'brankas_list.html', context)
