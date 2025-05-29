from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from .decorators import login_required_custom
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

@login_required_custom
def gender_list(request):
    try:
        genders = Genders.objects.all()
        data = {
            'genders': genders
        }
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during loads genders: {e}')

@login_required_custom
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            Genders.objects.create(gender=gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during add gender: {e}')

@login_required_custom
def edit_gender(request, genderId):
    try:
        genderObj = Genders.objects.get(pk=genderId)
        if request.method == 'POST':
            gender = request.POST.get('gender')
            genderObj.gender = gender
            genderObj.save()
            messages.success(request, 'Gender updated successfully!')
            return redirect('/gender/list')
        data = {
            'gender': genderObj
        }
        return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during edit gender: {e}')

@login_required_custom
def delete_gender(request, genderId):
    try:
        genderObj = Genders.objects.get(pk=genderId)
        if request.method == 'POST':
            genderObj.delete()
            messages.success(request, 'Gender deleted successfully')
            return redirect('/gender/list')
        data = {
            'gender': genderObj
        }
        return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during delete gender: {e}')

@login_required_custom
def user_list(request):
    try:
        query = request.GET.get('q', '')
        userObj = Users.objects.select_related('gender').all().order_by('user_id')
        if query:
            userObj = userObj.filter(
                Q(full_name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(address__icontains=query) |
                Q(contact_number__icontains=query)
            )
        paginator = Paginator(userObj, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {
            'page_obj': page_obj,
            'query': query
        }
        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during loads users: {e}')       

@login_required_custom
def add_user(request):
    try:
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birthdate')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Password and confirm password do not match!')
                return redirect('/user/add')

            # Check if username already exists
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'This username is already used by another user. Please choose a different username.')
                return redirect('/user/add')

            # Check if password already exists in the database
            for user in Users.objects.all():
                if check_password(password, user.password):
                    messages.error(request, 'This password is already used by another user. Please choose a different password.')
                    return redirect('/user/add')

            Users.objects.create(
                full_name=fullname,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthdate,
                address=address,
                contact_number=contact_number,
                email=email,
                username=username,
                password=make_password(password)
            )
            messages.success(request, 'User added successfully!')
            return redirect('/user/add')
        else:
            genderObj = Genders.objects.all()
            data = {
                'genders': genderObj
            }
            return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f"Error occurred during add user: {e}")
    
@login_required_custom
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            gender_id = request.POST.get('gender')
            birthdate = request.POST.get('birthdate')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if username is already used by another user
            if Users.objects.filter(username=username).exclude(pk=userId).exists():
                messages.error(request, 'This username is already used by another user. Please choose a different username.')
                return redirect(f'/user/edit/{userId}')

            # Check if password is already used by another user
            if password:
                if password != confirm_password:
                    messages.error(request, 'Password and confirm password do not match!')
                    return redirect(f'/user/edit/{userId}')
                for user in Users.objects.exclude(pk=userId):
                    if check_password(password, user.password):
                        messages.error(request, 'This password is already used by another user. Please choose a different password.')
                        return redirect(f'/user/edit/{userId}')
                userObj.password = make_password(password)

            userObj.full_name = fullname
            userObj.gender = Genders.objects.get(pk=gender_id)
            userObj.birth_date = birthdate
            userObj.address = address
            userObj.contact_number = contact_number
            userObj.email = email
            userObj.username = username

            userObj.save()
            messages.success(request, 'User updated successfully!')
            return redirect('/user/list')
        else:
            genderObj = Genders.objects.all()
            data = {
                'genders': genderObj,
                'user': userObj
            }
            return render(request, 'user/EditUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')
    
@login_required_custom
def delete_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)
        if request.method == 'POST':
            userObj.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')
        data = {
            'user': userObj,
            'genders': Genders.objects.all()
        }
        return render(request, 'user/DeleteUser.html', data)
    except Users.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('/user/list')
    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                messages.success(request, 'Login successful!')
                return redirect('/user/list')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('/login')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login')
    return render(request, 'login/Login.html')

def user_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return render(request, 'login/Logout.html')


