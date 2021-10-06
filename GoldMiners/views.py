from django.shortcuts import render
import base64
from GoldMiners.Portfolio import display_simulated_ef_with_random

def decode_plot(buffer):
    plot_data = buffer.getvalue()
    imb=base64.b64encode(plot_data)
    ims=imb.decode()
    imd="data:image/png;base64," + ims
    return imd

def portfolio(request):
    port = 'AAPL,AMZN,FB,WMT'
    days = 10
    vol = 30
    conf = 0.05
    w0 = 1000
    ws = '0.25,0.25,0.25,0.25'
    num_sim = 300

    # Get symbol list from web page
    if request.method == 'GET':
        if 'port' in request.GET:
            port = request.GET.get('port')
        if 'days' in request.GET:
            days = int(request.GET.get('days'))
        if 'conf' in request.GET:
            conf = float(request.GET.get('conf'))
        if 'vol' in request.GET:
            vol = int(request.GET.get('vol'))
        if 'w0' in request.GET:
            w0 = int(request.GET.get('w0'))
        if 'weights' in request.GET:
            ws = request.GET.get('weights')
        if 'num_sim' in request.GET:
            num_sim = int(request.GET.get('num_sim'))
    else:
        if 'port' in request.POST:
            port = request.POST.get('port')
        if 'days' in request.POST:
            days = int(request.POST.get('days'))
        if 'conf' in request.POST:
            conf = float(request.POST.get('conf'))
        if 'vol' in request.POST:
            vol = int(request.POST.get('vol'))
        if 'w0' in request.POST:
            w0 = int(request.POST.get('w0'))
        if 'weights' in request.POST:
            ws = request.POST.get('weights')
        if 'num_sim' in request.POST:
            num_sim = int(request.POST.get('num_sim'))
    
    buf_ef, min_vol_allocation, max_sharpe_allocation, buf_min, VaR_min, AR_min, MMD_min, buf_max, VaR_max, AR_max, MMD_max, buf_mc, VaR_mc, AR_mc, MMD_mc = display_simulated_ef_with_random(port,ws,days,vol,conf,w0,num_sim)

    imd_ef = decode_plot(buf_ef)
    imd_min = decode_plot(buf_min)
    imd_max = decode_plot(buf_max)
    imd_mc = decode_plot(buf_mc)

    min = [min_vol_allocation.columns.tolist()[i]+': '+str(min_vol_allocation.loc['allocation'].values[i])+'%' for i in range(len(min_vol_allocation.columns))]
    minvol = ', '.join(min)
    max = [max_sharpe_allocation.columns.tolist()[i]+': '+str(max_sharpe_allocation.loc['allocation'].values[i])+'%' for i in range(len(max_sharpe_allocation.columns))]
    maxshp = ', '.join(max)


    context = {
        'port': port,
        'days': days,
        'vol': vol,
        'conf': conf,
        'w0': w0,
        'num_sim': num_sim,
        'ws': ws,
        'img_ef': imd_ef,
        'img_min': imd_min,
        'img_max': imd_max,
        'img_mc': imd_mc,
        'minvol': minvol,
        'VaR_min': VaR_min,
        'AR_min': AR_min,
        'MMD_min': MMD_min,
        'maxshp': maxshp,
        'VaR_max': VaR_max,
        'AR_max': AR_max,
        'MMD_max': MMD_max,
        'VaR_mc': VaR_mc,
        'AR_mc': AR_mc,
        'MMD_mc': MMD_mc,
    }

    return render(request, 'portfolio.html', context)