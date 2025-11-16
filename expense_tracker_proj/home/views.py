from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, date
import calendar
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from income.models import Income
from app.models import Expense
from savings.models import Saving
from home.models import TransactionHistory
from todos.models import Todo


# 🏠 Home Dashboard — Each user sees only their own data
@login_required(login_url='login_user')
def home(request):
    user = request.user

    # ✅ User-specific totals
    total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_saving = Saving.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    current_balance = total_income - total_expense - total_saving

    # ✅ Last 30 days
    last_30_days = timezone.now().date() - timedelta(days=30)
    income_30 = Income.objects.filter(user=user, date__gte=last_30_days).aggregate(total=Sum('amount'))['total'] or 0
    expense_30 = Expense.objects.filter(user=user, date__gte=last_30_days).aggregate(total=Sum('amount'))['total'] or 0

    # ✅ Previous month calculation
    today = date.today()
    first_day_this_month = date(today.year, today.month, 1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = date(last_day_last_month.year, last_day_last_month.month, 1)
    last_month_name = calendar.month_name[last_day_last_month.month].upper()

    last_month_income = Income.objects.filter(
        user=user, date__gte=first_day_last_month, date__lte=last_day_last_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    last_month_expense = Expense.objects.filter(
        user=user, date__gte=first_day_last_month, date__lte=last_day_last_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    last_month_saving = Saving.objects.filter(
        user=user, date__gte=first_day_last_month, date__lte=last_day_last_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # ✅ Week calculations
    start_of_this_week = today - timedelta(days=today.weekday())  # Monday
    start_of_last_week = start_of_this_week - timedelta(days=7)
    end_of_last_week = start_of_this_week - timedelta(days=1)

    income_this_week = Income.objects.filter(user=user, date__gte=start_of_this_week).aggregate(total=Sum('amount'))['total'] or 0
    expense_this_week = Expense.objects.filter(user=user, date__gte=start_of_this_week).aggregate(total=Sum('amount'))['total'] or 0
    saving_this_week = Saving.objects.filter(user=user, date__gte=start_of_this_week).aggregate(total=Sum('amount'))['total'] or 0

    income_last_week = Income.objects.filter(user=user, date__gte=start_of_last_week, date__lte=end_of_last_week).aggregate(total=Sum('amount'))['total'] or 0
    expense_last_week = Expense.objects.filter(user=user, date__gte=start_of_last_week, date__lte=end_of_last_week).aggregate(total=Sum('amount'))['total'] or 0
    saving_last_week = Saving.objects.filter(user=user, date__gte=start_of_last_week, date__lte=end_of_last_week).aggregate(total=Sum('amount'))['total'] or 0

    # ✅ This month and year
    income_this_month = Income.objects.filter(user=user, date__gte=first_day_this_month).aggregate(total=Sum('amount'))['total'] or 0
    expense_this_month = Expense.objects.filter(user=user, date__gte=first_day_this_month).aggregate(total=Sum('amount'))['total'] or 0
    saving_this_month = Saving.objects.filter(user=user, date__gte=first_day_this_month).aggregate(total=Sum('amount'))['total'] or 0

    start_of_year = date(today.year, 1, 1)
    income_this_year = Income.objects.filter(user=user, date__gte=start_of_year).aggregate(total=Sum('amount'))['total'] or 0
    expense_this_year = Expense.objects.filter(user=user, date__gte=start_of_year).aggregate(total=Sum('amount'))['total'] or 0
    saving_this_year = Saving.objects.filter(user=user, date__gte=start_of_year).aggregate(total=Sum('amount'))['total'] or 0

    # ✅ Recent transactions and todos (user-specific)
    transactions = TransactionHistory.objects.filter(user=user).order_by('-date')[:5]
    todos = Todo.objects.filter(user=user).order_by('-date', 'is_done')

    # ✅ Context
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_saving': total_saving,
        'current_balance': current_balance,

        'income_30': income_30,
        'expense_30': expense_30,
        'last_month_name': last_month_name,
        'last_month_income': last_month_income,
        'last_month_expense': last_month_expense,
        'last_month_saving': last_month_saving,

        'income_this_week': income_this_week,
        'expense_this_week': expense_this_week,
        'saving_this_week': saving_this_week,
        'income_last_week': income_last_week,
        'expense_last_week': expense_last_week,
        'saving_last_week': saving_last_week,

        'income_this_month': income_this_month,
        'expense_this_month': expense_this_month,
        'saving_this_month': saving_this_month,

        'income_this_year': income_this_year,
        'expense_this_year': expense_this_year,
        'saving_this_year': saving_this_year,

        'transactions': transactions,
        'todos': todos,
    }

    return render(request, 'home.html', context)


# 📜 Transaction History (user-specific)
@login_required(login_url='login_user')
def transaction_history(request):
    transactions = TransactionHistory.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction_history.html', {'transactions': transactions})


# 📊 Chart Data (user-specific)
@login_required(login_url='login_user')
def chart_data(request):
    user = request.user
    range_key = request.GET.get('range', 'today')

    today = timezone.now().date()
    start_date = today

    if range_key == 'last_week':
        start_date = today - timedelta(days=7)
    elif range_key == 'last_month':
        start_date = today - timedelta(days=30)
    elif range_key == 'last_year':
        start_date = today - timedelta(days=365)

    income_total = Income.objects.filter(user=user, date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = Expense.objects.filter(user=user, date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0
    saving_total = Saving.objects.filter(user=user, date__gte=start_date).aggregate(Sum('amount'))['amount__sum'] or 0

    data = {
        'labels': ['Income', 'Expense', 'Savings'],
        'values': [income_total, expense_total, saving_total],
    }

    return JsonResponse(data)
