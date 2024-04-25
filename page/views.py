import subprocess

from django.shortcuts import redirect, render
from django.http import HttpResponse

from bot.bot import LeyDeOhmBot

LeyDeOhmBot().init()

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    return render(request, 'home.html')

def startServer(request, game):
    try:
        res = subprocess.check_output(['tmux', 'new-session', '-d', '-s', game])
        subprocess.check_output(['tmux', 'send-keys', '-t', game , game, 'ENTER'])
    except:
        pass
    return redirect('/')


def stopServer(request, game):
    try:
        res = subprocess.check_output(['tmux', 'kill-session', '-t', game])
    except:
        pass
    return redirect('/')

def startBot(request):
    return redirect('/')

def stopBot(request):
    return redirect('/')

def serverStatus(request):
    return redirect('/')
