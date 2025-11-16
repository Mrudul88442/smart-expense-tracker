from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Target
from savings.models import Saving
from income.models import Income
from app.models import Expense


# 🎯 Add a new target (user-specific)
@login_required(login_url='login_user')
def add_target(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        target_type = request.POST.get('target_type')
        goal_amount = request.POST.get('goal_amount')
        target_date = request.POST.get('target_date')

        if not all([title, target_type, goal_amount, target_date]):
            messages.error(request, "⚠️ All fields are required!")
            return redirect('add_target')

        # ✅ Save the target with logged-in user
        Target.objects.create(
            user=request.user,
            title=title,
            target_type=target_type,
            goal_amount=goal_amount,
            target_date=target_date,
        )

        messages.success(request, "🎯 Target added successfully!")
        return redirect('target_dashboard')

    return render(request, 'addtarget.html')


# 📊 Dashboard – View all targets and their statuses (user-specific)
@login_required(login_url='login_user')
def target_dashboard(request):
    targets = Target.objects.filter(user=request.user)  # ✅ Only user’s targets

    for target in targets:
        # ✅ Filter only this user's savings within the target period
        savings_in_period = Saving.objects.filter(
            user=request.user,
            date__gte=target.created_at,
            date__lte=target.target_date
        )

        total_saved = sum(s.amount for s in savings_in_period)

        # ✅ Determine status
        if total_saved >= target.goal_amount:
            target.status = "Achieved"
        elif target.target_date < timezone.now().date():
            target.status = "Expired"
        else:
            target.status = "Pending"

        target.save()

    context = {
        'targets': targets,
    }
    return render(request, 'targets_dashboard.html', context)


# ✏️ Edit target (only user’s own)
@login_required(login_url='login_user')
def edit_target(request, id):
    target = get_object_or_404(Target, id=id, user=request.user)  # ✅ Ownership check

    if request.method == 'POST':
        # Read submitted values
        title = request.POST.get('title')
        target_type = request.POST.get('target_type')
        goal_amount = request.POST.get('goal_amount')
        target_date = request.POST.get('target_date')

        # Validate required fields
        if not title:
            messages.error(request, "⚠️ Title is required.")
            return render(request, 'edit_target.html', {'target': target})

        # Update and save
        target.title = title
        if target_type:
            target.target_type = target_type
        if goal_amount:
            target.goal_amount = goal_amount
        if target_date:
            target.target_date = target_date
        target.save()

        messages.success(request, "✏️ Target updated successfully!")
        return redirect('target_dashboard')

    return render(request, 'edit_target.html', {'target': target})


# 🗑 Delete target (only user’s own)
@login_required(login_url='login_user')
def delete_target(request, id):
    target = get_object_or_404(Target, id=id, user=request.user)  # ✅ Ownership check
    target.delete()
    messages.success(request, "🗑️ Target deleted successfully!")
    return redirect('target_dashboard')
