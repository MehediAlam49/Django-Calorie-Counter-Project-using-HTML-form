from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from datetime import date
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CalorieCounter.models import *

def register_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if password==confirm_password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Register Successful')
            return redirect('login_page')


    return render(request, 'auth/register.html')


def login_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request,user)
            messages.success(request, 'Login Successful')
            return redirect('dashboard_page')

    return render(request, 'auth/login.html')


@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('login_page')


@login_required
def dashboard_page(request):
    try:
        current_user = request.user
        bmr = round(request.user.user_info.bmr, 2)
    except:
        current_user = None
        bmr = 0

    today = date.today()
    today_consumed_data = ConsumedCalories.objects.filter(
        consumed_by=current_user,
        created_at=today
    )
    total_consumed_calories = today_consumed_data.aggregate(
        total_caloire=Sum('calorie'),
        total_count=Count('calorie')
    )
    total_caloire = total_consumed_calories['total_caloire']

    try:
        less_more = bmr - total_caloire
    except:
        less_more=0
    try:
        if bmr > total_caloire:
            suggestion = 'Eat more'
        else:
            suggestion = 'Eat less'
    except:
        bmr=0
        total_caloire=0
        suggestion=''

    context = {
        'required_calories': bmr,
        'today_consumed_data': today_consumed_data,
        'consumed_calories': total_caloire,
        'total_count': total_consumed_calories['total_count'],
        'less_more': less_more,
        'suggestion': suggestion,

    }

    return render(request, 'dashboard.html', context)

@login_required
def profile_page(request):

    return render(request, 'profile/profile.html')


@login_required
def update_profile(request):
    try:
        current_user = request.user
    except:
        current_user = None

    profile_data,created=BasicInfoModel.objects.get_or_create(user=current_user)
    if request.method == 'POST':
        name=request.POST.get('name')
        age=int(request.POST.get('age'))
        gender=request.POST.get('gender')
        height=float(request.POST.get('height'))
        weight=float(request.POST.get('weight'))
        if gender == 'Male':
            # BMR= 66.47+(13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)
            bmr_calculate = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        else:
            # BMR=655.1+(9.563 x weight in kg)+(1.850 xheight in cm) - (4.676 x age in years)
            bmr_calculate = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

        profile_data.name=name
        profile_data.age=age
        profile_data.gender=gender
        profile_data.height=height
        profile_data.weight=weight
        profile_data.bmr=bmr_calculate
        profile_data.user=current_user
        profile_data.save()
        messages.success(request, 'Profile Update Successfully')
        return redirect('profile_page')

    context={
        'profile_data':profile_data
    }
    return render(request, 'profile/profile-form.html', context)


@login_required
def consumed_calories_list(request):
    consumed_data = ConsumedCalories.objects.filter(consumed_by=request.user)

    context = {
        'consumed_data': consumed_data
    }

    return render(request, 'calories/calorie-list.html', context)

@login_required
def add_calorie(request):
    if request.method == 'POST':
        item_name=request.POST.get('item_name')
        calorie=float(request.POST.get('calorie'))

        ConsumedCalories.objects.create(
            item_name=item_name,
            calorie=calorie,
            consumed_by=request.user,
        )
        messages.success(request, 'Item added Successfully')
        return redirect('consumed_calories_list')

    context={
        'form_title':'Add Calorie',
        'form_btn':'Add'
    }
    return render(request, 'calories/calorie-form.html',context)

@login_required
def update_calorie(request, id):
    calorie_data = ConsumedCalories.objects.get(id=id)

    if request.method == 'POST':
        item_name=request.POST.get('item_name')
        calorie=float(request.POST.get('calorie'))

        calorie_data.item_name=item_name
        calorie_data.calorie=calorie
        calorie_data.save()
        messages.success(request, 'Item updated Successfully')
        return redirect('consumed_calories_list')

    context = {
        'calorie_data':calorie_data,
        'form_title':'Update Calorie',
        'form_btn':'Update'
    }
    return render(request, 'calories/calorie-form.html', context)

@login_required
def delete_calorie(request, id):
    try:
        data = ConsumedCalories.objects.get(id=id)
        data.delete()
        messages.success(request, 'Successfully')
    except:
        data = None
        messages.success(request, 'Not Successful')
    return redirect('consumed_calories_list')