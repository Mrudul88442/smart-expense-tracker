from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum
from savings.models import Saving
from income.models import Income
from datetime import date, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from home.models import TransactionHistory
from django.contrib.auth.decorators import login_required

# Dashboard View
@login_required(login_url='login_user')
def expenses(request):
    expenses = Expense.objects.filter(user=request.user)

    # Get filter values
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    time_filter = request.GET.get('time_filter')

    # Filter by date range
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    # Filter by min/max amount
    if min_amount:
        expenses = expenses.filter(amount__gte=min_amount)
    if max_amount:
        expenses = expenses.filter(amount__lte=max_amount)

    # Time filter (day, week, month, year)
    today = timezone.now().date()
    if time_filter == 'day':
        expenses = expenses.filter(date=today)
    elif time_filter == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        expenses = expenses.filter(date__range=[week_start, week_end])
    elif time_filter == 'month':
        expenses = expenses.filter(date__month=today.month, date__year=today.year)
    elif time_filter == 'year':
        expenses = expenses.filter(date__year=today.year)

    total = sum(exp.amount for exp in expenses)
    return render(request, 'expenses.html', {'expenses': expenses, 'total': total})





from django.contrib import messages
from app.models import Expense
from income.models import Income

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from app.models import Expense
from income.models import Income
from home.models import TransactionHistory
from django.contrib.auth.decorators import login_required

# 🧾 Add Expense
@login_required(login_url='login_user')
def add_expense(request):
    if request.method == "POST":
        title = request.POST['title']
        amount = float(request.POST['amount'])
        category = request.POST['category']
        date = request.POST['date']

        # 🧮 Calculate current user's balance
        total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        current_balance = total_income - total_expense

        # 🚨 Prevent spending beyond balance
        if amount > current_balance:
            messages.warning(
                request,
                f"⚠️ Expense amount ({amount}) cannot exceed your current balance ({current_balance})!"
            )
            return redirect('add_expense')

        # ✅ Save expense for current user
        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            date=date
        )
        messages.success(request, "✅ Expense added successfully!")

        # 🧾 Record in transaction history
        TransactionHistory.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            transaction_type='Expense',
            date=date
        )

        return redirect('expenses')

    return render(request, 'addexpencse.html')



# 🗑️ Delete Expense
@login_required(login_url='login_user')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, pk=id, user=request.user)  # only current user's expense
    expense.delete()
    messages.success(request, "🗑️ Expense deleted successfully!")
    return redirect('expenses')



# ✏️ Edit Expense
@login_required(login_url='login_user')
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.category = request.POST.get('category')
        expense.save()
        messages.success(request, "✏️ Expense updated successfully!")
        return redirect('expenses')

    return render(request, 'editexpence.html', {'expense': expense})



# 📋 Show All Expenses for Current User
@login_required(login_url='login_user')
def expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expense = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': balance,
    }
    return render(request, 'expenses.html', context)
