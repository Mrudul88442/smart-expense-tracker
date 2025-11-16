from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .gemini_service import get_ai_response   # import working API function
from django.contrib.auth.decorators import login_required

@login_required
def ai_chat(request):
    if request.method == "POST":
        prompt = request.POST.get("message", "")
        reply = get_ai_response(prompt)
        return JsonResponse({"response": reply})
    return JsonResponse({"response": "Invalid request method"}, status=400)


@login_required
def chat_page(request):
    return render(request, "chat.html")
