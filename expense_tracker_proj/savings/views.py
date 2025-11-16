from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .models import Saving
from income.models import Income
from app.models import Expense
from home.models import TransactionHistory


# 📊 All Savings (user-specific)
@login_required(login_url='login_user')
def savings(request):
    user = request.user
    savings = Saving.objects.filter(user=user).order_by('-date')
    total_savings = sum(s.amount for s in savings)

    return render(request, 'savings.html', {
        'savings': savings,
        'total_savings': total_savings
    })


# ➕ Add Saving (user-specific)
@login_required(login_url='login_user')
def add_saving(request):
    user = request.user

    if request.method == "POST":
        title = request.POST.get('title')
        amount_str = request.POST.get('amount')
        date = request.POST.get('date')
        category = request.POST.get('category')

        # ⚠️ Validate required fields
        if not all([title, amount_str, date, category]):
            messages.error(request, "⚠️ All fields are required!")
            return redirect('add_saving')

        # Convert amount safely
        try:
            amount = float(amount_str)
        except (TypeError, ValueError):
            messages.error(request, "⚠️ Please enter a valid amount!")
            return redirect('add_saving')

        # 🧮 Calculate *user-specific* current balance
        total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_saving = Saving.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        current_balance = total_income - total_expense - total_saving

        # 🚨 Prevent saving more than available balance
        if amount > current_balance:
            messages.warning(
                request,
                f"⚠️ Saving amount ({amount}) cannot exceed your current balance ({current_balance})!"
            )
            return redirect('add_saving')

        # ✅ Check valid category
        valid_categories = [choice[0] for choice in Saving.CATEGORY_CHOICES]
        if category not in valid_categories:
            messages.error(request, "⚠️ Please select a valid category!")
            return redirect('add_saving')

        # ✅ Save saving entry linked to the user
        Saving.objects.create(
            user=user,
            title=title,
            amount=amount,
            date=date,
            category=category
        )

        # 🪣 Log in transaction history
        TransactionHistory.objects.create(
            user=user,
            title=title,
            amount=amount,
            transaction_type='Saving',
            date=date
        )

        messages.success(request, "✅ Saving added successfully!")
        return redirect('savings')

    return render(request, 'addsaving.html')


# ✏️ Edit Saving (user-specific)
@login_required(login_url='login_user')
def edit_saving(request, id):
    user = request.user
    saving = get_object_or_404(Saving, id=id, user=user)  # prevent editing others’ data

    if request.method == 'POST':
        saving.title = request.POST.get('title')
        saving.amount = request.POST.get('amount')
        saving.category = request.POST.get('category')
        saving.date = request.POST.get('date')
        saving.save()
        messages.success(request, "✅ Saving updated successfully!")
        return redirect('savings')

    return render(request, 'editsaving.html', {'saving': saving})


# ❌ Delete Saving (user-specific)
@login_required(login_url='login_user')
def delete_saving(request, id):
    user = request.user
    saving = get_object_or_404(Saving, id=id, user=user)
    saving.delete()

    # 🧮 Update user’s current balance in session
    total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_saving = Saving.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    current_balance = total_income - total_expense - total_saving

    request.session['current_balance'] = float(current_balance)
    messages.success(request, "🗑️ Saving deleted successfully!")

    return redirect('savings')
