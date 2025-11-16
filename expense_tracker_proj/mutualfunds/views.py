import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Investment
from django.shortcuts import get_object_or_404

BASE_URL = "https://api.mfapi.in/mf"

@login_required(login_url='login_user')
def mutualfunds_dashboard(request):
    query = request.GET.get('q', '').strip()
    funds = []

    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            all_funds = response.json()

            # 🔍 Search filter
            if query:
                all_funds = [
                    f for f in all_funds
                    if query.lower() in f['schemeName'].lower()
                ]

            # ⚡ Create top 20 dynamic entries
            funds = []
            for i, f in enumerate(all_funds[:20]):
                funds.append({
                    'name': f['schemeName'],
                    'scheme_code': f.get('schemeCode'),
                    'fund_size': round(500 + i * 20, 2),   # dummy
                    'return_pa': round(7 + i * 0.6, 2),    # dummy
                    'icon': 'fund.png'
                })

    except Exception as e:
        print("Error fetching funds:", e)

    return render(request, 'mutualfunds.html', {
        'funds': funds,
        'query': query
    })

from .models import Investment
import requests


@login_required
def add_to_portfolio(request, scheme_code):
    # Fetch fund name (for showing on form)
    response = requests.get(f"{BASE_URL}/{scheme_code}")
    data = response.json()
    scheme_name = data["meta"]["scheme_name"]

    if request.method == "POST":

        units = float(request.POST.get("units"))
        price = float(request.POST.get("purchase_price"))
        purchase_date = request.POST.get("purchase_date")

        Investment.objects.create(
            user=request.user,
            scheme_code=scheme_code,
            scheme_name=scheme_name,
            units=units,
            purchase_price=price,
            purchase_date=purchase_date
        )

        return redirect("my_portfolio")

    return render(request, "add_to_portfolio.html", {
        "scheme_code": scheme_code,
        "scheme_name": scheme_name
    })

@login_required(login_url='login_user')
def search_funds(request):
    query = request.GET.get('q', '')
    funds = []

    if query:
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                all_funds = response.json()
                funds = [
                    f for f in all_funds
                    if query.lower() in f['schemeName'].lower()
                ]
        except:
            pass

    return render(request, 'search_funds.html', {
        'funds': funds,
        'query': query
    })


@login_required(login_url='login_user')
def fund_detail(request, scheme_code):
    try:
        response = requests.get(f"{BASE_URL}/{scheme_code}")
        if response.status_code == 200:
            data = response.json()
            scheme_info = data.get("meta", {})
            latest_nav = data.get("data", [])[0] if data.get("data") else None
        else:
            scheme_info, latest_nav = {}, None
    except:
        scheme_info, latest_nav = {}, None

    return render(request, 'fund_detail.html', {
        'scheme_info': scheme_info,
        'latest_nav': latest_nav
    })

@login_required
def my_portfolio(request):
    investments = Investment.objects.filter(user=request.user)

    portfolio_data = []

    for inv in investments:
        # Fetch current NAV
        nav_api = f"https://api.mfapi.in/mf/{inv.scheme_code}"
        response = requests.get(nav_api).json()

        latest_nav_data = response.get("data", [{}])[0]
        current_nav = float(latest_nav_data.get("nav", 0))

        current_value = round(inv.units * current_nav, 2)
        invested_value = inv.invested_value
        profit_loss = round(current_value - invested_value, 2)

        portfolio_data.append({
            "investment": inv,
            "current_nav": current_nav,
            "current_value": current_value,
            "profit_loss": profit_loss,
        })

    return render(request, "my_portfolio.html", {
        "portfolio_data": portfolio_data
    })

@login_required
def delete_investment(request, investment_id):
    investment = get_object_or_404(Investment, id=investment_id, user=request.user)

    if request.method == "POST":
        investment.delete()
        return redirect("my_portfolio")   # Redirect back to portfolio page

    return redirect("my_portfolio")