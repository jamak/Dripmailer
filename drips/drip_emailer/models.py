from django.db import models
from django.core.mail import send_mail
from django.utils.timezone import now

# Create your models here.
class Email(models.Model):
    level = models.CharField(max_length=10)
    body = models.CharField(max_length=10000)
    subject = models.CharField(max_length=300)
    campaign = models.ForeignKey('Campaign', null=True, default=None)
    next_email = models.OneToOneField('Email', null=True, default=None)
    days_to_wait = models.IntegerField()

    def send_email(self, prospect):
        return send_mail(self.subject, self.body, 'company@notreal.com',
                  [prospect.email_address], fail_silently=False)

    def __unicode__(self):
        return "Email:{0},{1},{2}".format(self.level, self.subject, self.campaign)


class Prospect(models.Model):
    email_address = models.EmailField()
    signup_date = models.DateTimeField('date signed_up', default=now())
    responded = models.BooleanField()
    type = models.CharField(max_length=10)
    last_email_clicked = models.BooleanField()
    recent_email = models.ForeignKey(Email, related_name='emailLastSeen',
            default=None)
    recent_email_sent = models.DateTimeField('date last emailed')

    def __unicode__(self):
        return "Prospect:({0},{1})".format(self.email_address, self.responded)

class Campaign(models.Model):
    type  = models.CharField(max_length=10)
    first = models.ForeignKey(Email, related_name='first campaign email')

    def __unicode__(self):
        return "Campaign:({0},{1})".format(self.type, self.first)


class ProspectEmail(models.Model):
    prospect = models.ForeignKey('Prospect', default=None)
    email = models.ForeignKey('Email', default=None)
    clicked = models.BooleanField()




def send_email(prospect):
    '''sends an email to a prospective customer, updates the customer if so.'''
    if not prospect.responded:
        if prospect.last_email.next_email.days_to_wait < prospect.recent_email_sent - now():
            prospect.last_email.next_email.send_email(prospect)
            prospect.last_email = prospect.last_email.next_email
            return True
        else :
            #email not sent!
            print "Not quite yet..."
            return False


from random import randint
def make_emails(n):
    seq = []
    for i in xrange(n):
        email = Email()
        if i == 0:
            email.level = "final"
        elif i == n - 1:
            email.level = "intro"
        else:
            email.level = "middle"
        email.subject = "subject{0}".format(n-i)
        email.body = "body{0}".format(n-i)
        email.days_to_wait = randint(1, 15)
        seq.append(email)
        if i > 0:
            email.next_email = seq[i-1]
            email.next_email_id = email.next_email.id
    return seq[::-1]


def best_email(lvl, camp):
    """finds the best email for the given level and campaign."""
    scores = {}
    all_emails = Email.objects.filter(level__iexact=lvl, campaign__iexact=camp)
    def count_clicks(eml):
        prospect_emails = ProspectEmail.objects.filter(email=eml)
        positive = filter(lambda email:email.clicked, prospect_emails)
        return len(positive)
    for email in all_emails:
        scores.setdefault(count_clicks(email), email)

