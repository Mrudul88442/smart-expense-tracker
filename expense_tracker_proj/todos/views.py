from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 🏠 Show all todos for the logged-in user
@login_required(login_url='login_user')
def todos_home(request):
    todos = Todo.objects.filter(user=request.user).order_by('-date', 'is_done')  # ✅ Only user's todos
    return render(request, 'home.html', {'todos': todos})


# ✅ Toggle checkbox (mark complete/incomplete)
@login_required(login_url='login_user')
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)  # ✅ Only allow user’s own todo
    todo.is_done = not todo.is_done
    todo.save()
    return redirect('todos_home')


# ➕ Add new todo (only for the logged-in user)
@login_required(login_url='login_user')
def add_todo(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        date = request.POST.get('date') or timezone.now().date()

        if not description:
            messages.warning(request, "⚠️ Description cannot be empty!")
            return redirect('add_todo')

        # ✅ Assign todo to logged-in user
        Todo.objects.create(
            user=request.user,
            description=description,
            date=date
        )
        messages.success(request, "✅ Todo added successfully!")
        return redirect('todos_home')

    return render(request, 'addtodo.html')


# ❌ Delete todo (only user's own)
@login_required(login_url='login_user')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)  # ✅ Only allow user’s own todo
    todo.delete()
    messages.success(request, "🗑️ Todo deleted successfully!")
    return redirect('todos_home')
