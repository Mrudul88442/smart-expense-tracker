from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Income
from home.models import TransactionHistory


# 🧾 View all income entries (user-specific)
@login_required(login_url='login_user')
def income(request):
    incomes = Income.objects.filter(user=request.user)  # Only current user's incomes

    # Get filter values from query params
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    time_filter = request.GET.get('time_filter')

    # 🗓️ Date range filter
    if start_date and end_date:
        incomes = incomes.filter(date__range=[start_date, end_date])

    # 💰 Min/max filter
    if min_amount:
        incomes = incomes.filter(amount__gte=min_amount)
    if max_amount:
        incomes = incomes.filter(amount__lte=max_amount)

    # ⏰ Time period filter
    today = timezone.now().date()
    if time_filter == 'day':
        incomes = incomes.filter(date=today)
    elif time_filter == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        incomes = incomes.filter(date__range=[week_start, week_end])
    elif time_filter == 'month':
        incomes = incomes.filter(date__month=today.month, date__year=today.year)
    elif time_filter == 'year':
        incomes = incomes.filter(date__year=today.year)

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'income.html', {
        'incomes': incomes,
        'total_income': total_income,
    })


# ➕ Add new income (user-specific)
@login_required(login_url='login_user')
def add_income(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        category = request.POST.get('category')

        # ✅ Create income linked to current user
        Income.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            date=date,
            category=category
        )

        # 💾 Save transaction history
        TransactionHistory.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            transaction_type='Income',
            date=date
        )

        messages.success(request, "✅ Income added successfully!")
        return redirect('income')

    return render(request, 'addincome.html')


# ✏️ Edit existing income
@login_required(login_url='login_user')
def edit_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)  # User-restricted

    if request.method == 'POST':
        income.title = request.POST.get('title')
        income.amount = request.POST.get('amount')
        income.category = request.POST.get('category')
        income.date = request.POST.get('date')
        income.save()
        messages.success(request, "✏️ Income updated successfully!")
        return redirect('income')

    return render(request, 'editincome.html', {'income': income})


# 🗑️ Delete income
@login_required(login_url='login_user')
def delete_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    income.delete()
    messages.success(request, "🗑️ Income deleted successfully!")
    return redirect('income')
