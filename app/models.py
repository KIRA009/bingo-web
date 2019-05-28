from django.db import models
from passlib.hash import pbkdf2_sha256
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bingo.settings import email_pass
import smtplib
import secrets


def update_model(model, num):
    found = False
    for row in range(5):
        for col in range(5):
            if not found:
                if model[row][col] == num:
                    model[row][col] = '0'  # for replacing number with 0
                    found = True
            else:
                break
    count = 0
    for row in model:
        if row.count('0') == 5:  # for checking rows
            count += 1

    temp_count = 0
    for row in range(5):
        for col in range(5):
            if model[row][col] == '0':
                inner_count = 0
                for inner in range(5):
                    if model[inner][col] == '0':  # for checking cols
                        inner_count += 1
                    else:
                        break
                if inner_count == 5:
                    temp_count += 1
    count += temp_count // 5

    if model[2][2] == '0':
        diag_count = 0

        for row in range(5):
            if model[row][row] == '0':  # for checking primary diagonal
                diag_count += 1
            else:
                break
        if diag_count == 5:
            count += 1
        diag_count = 0

        for row in range(5):
            if model[row][4 - row] == '0':  # for checking secondary diagonal
                diag_count += 1
            else:
                break
        if diag_count == 5:
            count += 1
    return count


def send_email(user, message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verify email for Bingo"
    msg['From'] = 'creator.bingo@gmail.com'
    msg['To'] = user.email
    part2 = MIMEText(message, 'html')
    msg.attach(part2)
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.starttls()
    mail.login(msg['From'], email_pass)
    mail.sendmail(msg['From'], msg['To'], msg.as_string())
    mail.quit()


def is_logged_in(request):
    try:
        if request.session['username'] is not None:
            if (datetime.datetime.now() - datetime.datetime.strptime(request.session[f'{request.session["username"]}'], '%m/%d/%y %H:%M:%S')).seconds < 86400:
                return True
            else:
                logout(request)
                return False
    except:
        return False


def logout(request):
    user = Users.objects.get(name=request.session['username'])
    user.is_active = False
    user.save()
    del request.session[f'{request.session["username"]}']
    del request.session['username']


def get_user(request=None, name=None):
    if request is not None:
        return Users.objects.get(name=request.session['username'])
    else:
        return Users.objects.get(name=name)


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField(unique=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.TextField()
    validated = models.BooleanField(default=False)
    secret = models.TextField(default='')
    reset = models.TextField(default='')
    is_active = models.BooleanField(default=False)
    image = models.URLField(default='')
    cur_session = models.TextField(default='')
    record = models.ForeignKey('Records', to_field='name', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def is_not_registered(self):
        try:
            user = Users.objects.get(email=self.email)
            return 1
        except:
            try:
                user = Users.objects.get(name=self.name)
                return 2
            except:
                return 3

    def is_authenticated(self, password):
        try:
            user = Users.objects.get(name=self.name)
            if pbkdf2_sha256.verify(password, user.password):
                if user.validated:
                    return 0
                else:
                    return 3
            else:
                return 2
        except:
            return 1

    def login(self, request):
        self.is_active = True
        self.save()
        request.session["username"] = self.name
        now = datetime.datetime.now()
        request.session[f'{self.name}'] = f'{now.month}/{now.day}/{str(now.year)[-2:]} {now.hour}:{now.minute}:{now.second}'
        self.cur_session = request.session['session'] = secrets.token_hex(5)


class Game(models.Model):
    key = models.TextField(unique=True)
    p1 = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='p1', null=True, default=None)
    p2 = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='p2', null=True, default=None)
    p1_model = models.TextField(default='')
    p2_model = models.TextField(default='')
    c1 = models.IntegerField(default=0)
    c2 = models.IntegerField(default=0)
    cur_num = models.IntegerField(default=0)
    cur_player = models.TextField(default='')
    complete = models.BooleanField(default=False)


class Records(models.Model):
    name = models.CharField(max_length=20, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    win_streak = models.IntegerField(default=0)
    h_win_streak = models.IntegerField(default=0)
    last_match = models.TextField(default='')
    last_p1 = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='lp1', null=True)
    last_p2 = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='lp2', null=True)
    last_p3 = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='lp3', null=True)
    res_p1 = models.TextField(default='')
    res_p2 = models.TextField(default='')
    res_p3 = models.TextField(default='')


class Invite(models.Model):
    from_user = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='from_user', null=True)
    to_user = models.ForeignKey(Users, to_field='name', on_delete=models.CASCADE, related_name='to_user', null=True)
    key = models.TextField()
    accepted = models.BooleanField(default=False)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Users, to_field='name', related_name='from_request', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(Users, to_field='name', related_name='to_request', on_delete=models.CASCADE, null=True)


class Friends(models.Model):
    from_user = models.ForeignKey(Users, to_field='name', related_name='from_friend', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(Users, to_field='name', related_name='to_friend', on_delete=models.CASCADE, null=True)
