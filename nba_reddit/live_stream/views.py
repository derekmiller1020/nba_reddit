from django.shortcuts import render
import praw
from django.http import HttpResponseRedirect
from models import InsertCommentForm
from django.template import loader, Context, RequestContext
import webbrowser
from variables import *

r.set_oauth_app_info(CLIENT_ID, SECRET_ID, REDIRECT_URI)

def retrieve_threads(request):

    #submissions = r.get_subreddit('python').get_new(limit=200)
    game_threads = []
    the_text = []

    if r.is_oauth_session():
        woo = r.get_me()
        zoo = woo.name
    else:
        woo = "aaahahahahahaha"
        zoo = "asdfjhasdkjhakldf"
    #for submission in submissions:
        #if "GAME THREAD" in str(submission):
            #game_threads.append(submission.id)
            #the_text.append(submission)

    return render(request, 'game_threads.html', {
        'game_threads': game_threads,
        'the_text': the_text,
        'zoo': zoo,
    })

def retrieve_comments(request):

    if 'id' in request.GET:
        threads = request.GET['id']
        r = praw.Reddit(user_agent='r_nba_live_stream')
        submission = r.get_submission(submission_id=threads)
        the_comments = submission.comments

    else:
        return HttpResponseRedirect('/threads/')

    return render(request, 'comments.html', {
        'the_comments': the_comments,
    })

def redirect_url(request):

    if 'code' in request.GET:
        access_information = r.get_access_information(request.GET['code'])
        r.set_access_credentials(**access_information)
        id = request.GET['code']
        request.session['code'] = id

    return HttpResponseRedirect('/threads/')

def submit_comment(request):

    link_no_refresh = r.get_authorize_url('uniqueKey', 'identity', True)

    text = "First Link. Not Refreshable  <br>"

    return render(request, 'submit_comment.html', {
        'text': text,
        'link': link_no_refresh,
    })