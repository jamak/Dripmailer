from django.template import Context, loader
from django.http import HttpResponse
from drip_emailer.models import Campaign, Email, Prospect
from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.
def campaign_index(request):
    latest_campaign_list = Campaign.objects.all()[:5]
    t = loader.get_template('campaigns/index.html')
    c = Context({
        'latest_campaign_list': latest_campaign_list,
    })
    return HttpResponse(t.render(c))

def campaign_detail(request, campaign_id):
    p = get_object_or_404(Campaign, pk=campaign_id)
    return render_to_response('campaigns/detail.html', {'campaign': p})

def email_index(request):
    latest_email_list = Email.objects.all()[:5]
    t = loader.get_template('emails/index.html')
    c = Context({
        'latest_email_list': latest_email_list,
    })
    return HttpResponse(t.render(c))

def email_detail(request, email_id):
    p = get_object_or_404(Email, pk=email_id)
    return render_to_response('emails/detail.html', {'email': p})

def prospect_index(request):
    latest_prospect_list = Prospect.objects.all()[:5]
    t = loader.get_template('prospects/index.html')
    c = Context({
        'latest_prospect_list': latest_prospect_list,
    })
    return HttpResponse(t.render(c))

def prospect_detail(request, prospect_id):
    p = get_object_or_404(Prospect, pk=prospect_id)
    return render_to_response('prospects/detail.html', {'prospect': p})
