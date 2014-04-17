from django.shortcuts import render
import praw
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from models import InsertCommentForm
from django.template import loader, Context, RequestContext
import webbrowser
from variables import *
from the_long_poll import the_long_poll

#Oauth global
r.set_oauth_app_info(CLIENT_ID, SECRET_ID, REDIRECT_URI)

def retrieve_threads(request):

    #check the r/nba submissions
    submissions = r.get_subreddit('nba').get_new(limit=200)

    #append game_threads(too much logic for a comprehension)
    game_threads = []

    #Check to see if they are game threads
    for submission in submissions:
        if "GAME THREAD" in str(submission):
            game_threads.append(submission)

    #render it
    return render(request, 'game_threads.html', {
        'game_threads': game_threads,
    })


def retrieve_comments(request):

    #Is the user logged in and has accepted me stealing all of their info??
    #JK!
    if r.is_oauth_session():
        get_em = r.get_me()

        #show my username
        username = get_em.name

        #A variable that is going to be used as a boolean.. huh?
        can_comment = "correct"

        link_no_refresh = ""

    else:

        #set an oauth link where users can sign in to reddit
        link_no_refresh = r.get_authorize_url('uniqueKey', 'identity', True)
        username = ""
        can_comment = ""

    #if and 'id' is specified in request.GET, do these things
    if 'id' in request.GET:
        threads = request.GET['id']
        submission = r.get_submission(submission_id=threads, comment_sort="new")
        the_comments = submission.comments

    else:

        #GET OUT OF HERE!
        return HttpResponseRedirect('/threads/')

    return render(request, 'comments.html', {
        'the_comments': the_comments,
        'username': username,
        'can_comment': can_comment,
        'link': link_no_refresh,
        'threads': threads,
    })


def redirect_url(request):

    #Check to see if 'code' is set in the get
    if 'code' in request.GET:

        #get access information from code
        access_information = r.get_access_information(request.GET['code'])

        #set that puppy
        r.set_access_credentials(**access_information)

    return HttpResponseRedirect('/threads/')

#I didn't feel like setting up a websocket app for this app. ajax polling it is. It is really bad practice, I know.
#also, I didn't like how praw was retrieving data, so I am parsing the api directly.
def retrieve(request):

    #ajax is requesting a post
    if request.method == "POST":
        thread = request.POST.get('id')
        the_inst = the_long_poll(thread)
        full_json = the_inst.the_post()

        return HttpResponse(full_json, content_type="application/json")

    else:
        return HttpResponseRedirect("/threads/")
