from django.http import HttpResponse

def get_portfolio(request):
    if request.POST:
        stocks = request.POST['stocks']
        stocks = stocks.split(',')
        day = request.POST['days']
        alpha = request.POST['alpha']

