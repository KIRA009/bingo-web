from django.shortcuts import render, redirect
from django.views import View
from app.models import *
from passlib.hash import pbkdf2_sha256
import secrets
import random
from django.http import JsonResponse
import cloudinary
import cloudinary.uploader
import cloudinary.api
from bingo.settings import api_key, api_secret


def index(request):
    if is_logged_in(request):
        return redirect('home')
    return render(request, 'index.html')


class Register(View):
    def get(self, request):
        if is_logged_in(request):
            return redirect('home')
        return render(request, 'register.html')

    def post(self, request):
        response_data = {}
        messages = ['Email already registered', 'Username already taken']
        user = Users(email=request.POST['email'], name=request.POST['name'], password=pbkdf2_sha256.encrypt(request.POST['password'], rounds=12000, salt_size=32), secret=secrets.token_hex(5), reset=secrets.token_hex(4))
        if user.is_not_registered() == 3:
            message = f"""\
            <html>
                <head></head>
                <body style="text-align:left;">
                    <header><img src="https://i.imgur.com/gIpGJRb.png" height="200px" width="200px"></header><br><br>
                    <div style="text-align:left; font-size:20px;">
                        Hi {user.name},<br><br>
                        Greetings from Bingo Creator!<br><br>
                        You are just a step away from accessing your Bingo account.<br><br>
                        To complete your sign up,<br>
                        please verify your email<br><br>
                    </div>
                    <a style="font-size:20px; background-color:#007bff; text-decoration:none; padding-top:5px; padding-bottom:10px; padding-left:10px; padding-right:10px; color:#fff; margin:auto auto;" href="http://{request.get_host()}/app/validate/{user.secret}" type="button"> Click here to validate </a><br><br>
                    <p style="font-size:20px;">
                        Thank you,<br>
                        Bingo Creator
                    </p><br><br>
                    If you face any problems, feel free to send your queries at creator.bingo@gmail.com
                </body>
            </html>
            """
            send_email(user, message)
            record = Records(name=user.name)
            user.record = record
            record.save()
            user.save()
            response_data['url'] = 'login'
            return JsonResponse(response_data)
        else:
            response_data['url'] = 'register'
            response_data['message'] = messages[user.is_not_registered() - 1]
            return JsonResponse(response_data)


def update_img(request):
    cloudinary.config(
        cloud_name="bingoproject",
        api_key=api_key,
        api_secret=api_secret
    )
    user = get_user(request=request)
    user.image = cloudinary.uploader.upload(request.FILES['image'])['secure_url']
    user.save()
    return redirect('home')


class Login(View):
    def get(self, request):
        if is_logged_in(request):
            return redirect('home')
        return render(request, 'login.html')

    def post(self, request):
        response_data = {}
        messages = ['Username not registered', 'Password incorrect', 'Email not verified', 'Email verified. You can now login with your credentials', 'Password reset. You can now login with your new password', 'Email not registered', 'Check email for verification link']
        try:
            user = Users.objects.get(name=request.POST['name'])
            if user.is_authenticated(request.POST['password']) == 0:
                user.login(request)
                response_data['url'] = 'home'
                return JsonResponse(response_data)
            response_data['url'] = 'login'
            response_data['message'] = messages[user.is_authenticated(request.POST['password']) - 1]
            return JsonResponse(response_data)
        except:
            response_data['url'] = 'login'
            response_data['message'] = messages[0]
            return JsonResponse(response_data)


def log_out(request):
    logout(request)
    return redirect('login')


def validate(request, secret):
    try:
        user = Users.objects.get(secret=secret)
        user.validated = True
        user.save()
        return redirect('login')
    except:
        return redirect('login')


class Forgot(View):
    def get(self, request):
        return render(request, 'forgot.html')

    def post(self, request):
        data = {}
        try:
            user = Users.objects.get(email=request.POST['email'])
            message = f"""\
            <html>
                <head></head>
                <body style="text-align:left;">
                    <header><img src="https://i.imgur.com/gIpGJRb.png" height="200px" width="200px"></header><br><br>
                    <div style="text-align:left; font-size:20px;">
                        Hi {user.name},<br><br>
                        Greetings from Bingo Creator!<br><br>
                        This email has been sent after your request to change the account password<br><br>
                        If it wasn't requested by you,<br>
                        no need to worry<br><br>
                    </div>
                    <a style="font-size:20px; background-color:#007bff; text-decoration:none; padding-top:5px; padding-bottom:10px; padding-left:10px; padding-right:10px; color:#fff; margin:auto auto;" href="http://{request.get_host()}/app/reset/{user.reset}" type="button"> Click here to reset password </a><br><br>
                    <p style="font-size:20px;">
                        Thank you,<br>
                        Bingo Creator
                    </p><br><br>
                    If you face any problems, feel free to send your queries at creator.bingo@gmail.com
                </body>
            </html>
            """
            send_email(user, message)
            data['url'] = 'login'
            return JsonResponse(data)
        except:
            data['url'] = 'asjh'
            data['message'] = 'Email not registered'
            return JsonResponse(data)


class Reset(View):
    def get(self, request, reset):
        return render(request, 'reset.html', {'reset': reset})

    def post(self, request, reset):
        try:
            user = Users.objects.get(reset=reset)
            if user.reset:
                message = f"""\
                            <html>
                                <head></head>
                                <body style="text-align:left;">
                                    <header><img src="https://i.imgur.com/gIpGJRb.png" height="200px" width="200px"></header><br><br>
                                    <div style="text-align:left; font-size:20px;">
                                        Hi {user.name},<br><br>
                                        Greetings from Bingo Creator!<br><br>
                                        This email has been sent because you just changed your password<br><br>
                                        If it wasn't done by you,<br>
                                        contact us immediately at creator.bingo@gmail.com<br><br>
                                    </div>
                                    <p style="font-size:20px;">
                                        Thank you,<br>
                                        Bingo Creator
                                    </p><br><br>
                                    If you face any problems, feel free to send your queries at creator.bingo@gmail.com
                                </body>
                            </html>
                            """
                send_email(user, message)
                user.password = pbkdf2_sha256.encrypt(request.POST['password'], rounds=12000, salt_size=32)
                user.reset = secrets.token_hex(4)
                user.save()
            return redirect('login')
        except:
            return redirect('login')


class Home(View):
    def get(self, request):
        error = ' '.join(request.GET.get('e', '').split('_'))
        if not is_logged_in(request):
            return redirect('login')
        return render(request, 'homepage.html', {'user': get_user(request=request), 'random': secrets.token_hex(5), 'record': Records.objects.get(name=get_user(request=request).name), 'error': error})


def records(request):
    if not is_logged_in(request):
        return redirect('login')
    user = get_user(request=request)
    record = Records.objects.get(name=user.name)
    print(record.last_p1)
    return render(request, 'records.html', {'user': user, 'record': record})


class Invites(View):
    def get(self, request):
        if not is_logged_in(request):
            return redirect('login')
        user = get_user(request=request)
        sent_invites = Invite.objects.all().filter(from_user=user)
        received_invites = Invite.objects.filter(to_user=user, accepted=False)
        friends = Friends.objects.all().filter(from_user=user)
        return render(request, 'invites.html', {'sent_invites': sent_invites, 'received_invites': received_invites,
                                                'user': user, 'friends': friends, 'lf': len(friends),
                                                'ls': len(sent_invites), 'lr': len(received_invites)})

    def post(self, request):
        key = request.POST['key']
        friend = get_user(name=request.POST['friend'])
        user = get_user(request=request)
        try:
            game = Game.objects.get(key=key)
        except Game.DoesNotExist:
            try:
                Invite.objects.get(key=key)
            except Invite.DoesNotExist:
                Invite.objects.create(key=key, from_user=user, to_user=friend)
        return redirect('invites')


class Requests(View):
    def get(self, request):
        if not is_logged_in(request):
            return redirect('login')
        user = get_user(request=request)
        users = Users.objects.filter(validated=True).exclude(name=user.name)
        try:
            friend_reqs = FriendRequest.objects.all().filter(to_user=user)
        except:
            friend_reqs = ''
        friends = Friends.objects.all().filter(from_user=user)
        to_friends = set(user.to_user for user in friends)
        users = set(users).difference(to_friends)
        return render(request, 'requests.html', {'user': user, 'users': users, 'friend_reqs': friend_reqs,
                                                 'l': len(friend_reqs), 'friends': friends, 'lu': len(users),
                                                 'lf': len(friends)})


def send_request(request):
    if not is_logged_in(request):
        return redirect('login')
    user = get_user(request=request)
    friend = get_user(name=request.POST['friend'])
    try:
        Friends.objects.get(from_user=user, to_user=friend)
    except:
        try:
            FriendRequest.objects.get(from_user=friend, to_user=user)
        except:
            FriendRequest.objects.get_or_create(from_user=user, to_user=friend)
    return redirect('requests')


def decline_request(request, friend):
    user = get_user(request=request)
    friend = get_user(name=friend)
    req = FriendRequest.objects.get(from_user=friend, to_user=user)
    req.delete()
    return JsonResponse({'response': 'success'})


def accept_request(request, friend):
    user = get_user(request=request)
    friend = get_user(name=friend)
    Friends.objects.create(from_user=user, to_user=friend)
    Friends.objects.create(from_user=friend, to_user=user)
    FriendRequest.objects.get(from_user=friend, to_user=user).delete()
    return redirect('invites')


def random_num(request):
    data = {'random': secrets.token_hex(5)}
    return JsonResponse(data)


def game_check(request):
    key = request.POST['key']
    user = get_user(request=request)
    try:
        game = Game.objects.get(key=key)
        if game.p1 == user:
            return redirect('/app/startGame?k=' + str(key))
        elif game.p2 == user or game.p2 is None:
            return redirect('/app/startGame?k=' + str(key))
        else:
            return redirect('/app/home/?e=Already_taken')
    except:
        Game.objects.create(key=key, p1=user)
        return redirect('/app/startGame?k=' + str(key))


def accept_invite(request):
    key = request.POST['key']
    invite = Invite.objects.get(key=key)
    invite.accepted = True
    invite.save()
    Game.objects.create(key=key, p1=invite.from_user, p2=invite.to_user)
    return redirect('/app/startGame?k=' + str(key))


def remove_game(request, key):
    game = Game.objects.get(key=key)
    game.delete()
    Invite.objects.get(key=key).delete()
    return JsonResponse({'result': 'success'})


def start_game(request):
    if not is_logged_in(request):
        return redirect('login')
    user = get_user(request=request)
    try:
        key = str(request.POST['key'])
    except:
        key = str(request.GET.get('k'))
    try:
        game = Game.objects.get(key=key)
        if game.complete:
            return redirect('home')
        if user == game.p1:
            if game.p2 is None:
                opponent = ''
            else:
                opponent = get_user(name=game.p2.name).name
        elif game.p2 is None:
            game.p2 = user
            game.save()
            opponent = get_user(name=game.p1.name).name
        elif user == game.p2:
            opponent = get_user(name=game.p1.name).name
        else:
            return redirect('home')
    except:
        Game.objects.create(key=key, p1=user)
        opponent = ''
    return render(request, 'game_init.html', {'opponent': opponent, 'key': key})


def get_opp(request):
    key = request.POST['key']
    user = get_user(request=request)
    game = Game.objects.get(key=key)
    if game.p1.name == user.name:
        if game.p2 is not None:
            return JsonResponse({'opponent': game.p2.name})
        else:
            return JsonResponse({'opponent': None})
    else:
        return JsonResponse({'opponent': game.p1.name})


def data(request, key):
    if not is_logged_in(request):
        return redirect('login')
    game = Game.objects.get(key=key)
    model = request.POST['data'].split('+')[: -1]
    model = [model[i: i + 5] for i in range(0, len(model), 5)]
    if game.p1.name == request.POST['opponent']:
        model = game.p2_model = f'{model}'
    else:
        model = game.p1_model = f'{model}'
    random.seed(datetime.datetime.now())
    if game.cur_player == '':
        game.cur_player = random.choice([game.p1.name, game.p2.name])
    game.save()
    return render(request, 'game_play.html', {'opponent': request.POST['opponent'], 'data': eval(model), 'key': key, 'cur_player': game.cur_player})


def game_play(request, key):
    if not is_logged_in(request):
        return redirect('login')
    game = Game.objects.get(key=key)
    num = str(request.POST['data'])
    model1 = eval(game.p1_model)
    model2 = eval(game.p2_model)
    game.c1 = update_model(model1, num)
    game.c2 = update_model(model2, num)
    if game.c2 >= 5:
        if game.c1 < 5:
            winner = game.p2.name
        elif game.c2 >= 5:
            winner = 'both'
        else:
            winner = 'none'
    elif game.c2 < 5:
        if game.c1 >= 5:
            winner = game.p1.name
        else:
            winner = 'none'
    else:
        winner = 'none'
    game.p1_model = f'{model1}'
    game.p2_model = f'{model2}'
    game.cur_num = int(num)
    game.cur_player = request.POST['opponent']
    game.save()
    record = Records.objects.get(name=game.p1.name)
    if winner == record.name:
        record.wins += 1
        record.win_streak += 1
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p2.name
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'WIN'
        record.save()
    elif winner == 'both':
        record.draws += 1
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p2.name
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'DRAW'
        record.save()
    elif winner != 'none':
        record.losses += 1
        if record.win_streak > record.h_win_streak:
            record.h_win_streak = record.win_streak
        record.win_streak = 0
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p2
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'LOSS'
        record.save()
    record = Records.objects.get(name=game.p2.name)
    if winner == record.name:
        record.wins += 1
        record.win_streak += 1
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p1
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'WIN'
        record.save()
    elif winner == 'both':
        record.draws += 1
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p1
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'DRAW'
        record.save()
    elif winner != 'none':
        record.losses += 1
        if record.win_streak > record.h_win_streak:
            record.h_win_streak = record.win_streak
        record.win_streak = 0
        record.last_p3 = record.last_p2
        record.last_p2 = record.last_p1
        record.last_p1 = game.p1
        record.res_p3 = record.res_p2
        record.res_p2 = record.res_p1
        record.last_match = record.res_p1 = 'LOSS'
        record.save()
    return redirect('update', key=key, opponent=request.POST['opponent'], winner=winner)


def update_game(request, key, opponent, winner=None):
    if not is_logged_in(request):
        return redirect('login')
    game = Game.objects.get(key=key)
    if winner is None:
        if game.c2 >= 5:
            if game.c1 < 5:
                winner = game.p2.name
            elif game.c2 >= 5:
                winner = 'both'
            else:
                winner = 'none'
        elif game.c2 < 5:
            if game.c1 >= 5:
                winner = game.p1.name
            else:
                winner = 'none'
        else:
            winner = 'none'
    if opponent == game.p1.name:
        return JsonResponse({'cur_num': game.cur_num, 'count': game.c2, 'cur_player': game.cur_player, 'winner': winner})
    else:
        return JsonResponse({'cur_num': game.cur_num, 'count': game.c1, 'cur_player': game.cur_player, 'winner': winner})
