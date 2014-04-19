from django.shortcuts import render
import praw
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from models import InsertCommentForm
from django.template import loader, Context, RequestContext
from variables import *
from stream_wrapper import StreamWrapper
import redis

#Oauth global
r.set_oauth_app_info(CLIENT_ID, SECRET_ID, REDIRECT_URI)

#login
r.login(username=username, password=password)

def retrieve_threads(request):

    #custom function to clear cache
    clear_cache()

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


#comments
def retrieve_comments(request):

    message = ""

    #Is the user logged in and has accepted me stealing all of their info??
    #JK!
    if r.is_oauth_session():

        #custom clear function
        clear_cache()

        if request.method == 'POST':
            message = InsertCommentForm(request.POST)
        else:
            message = InsertCommentForm()
        get_em = r.get_me()

        #show my username
        username = get_em.name

        #A variable that is going to be used as a boolean.. huh?
        can_comment = "correct"

        link_no_refresh = ""

    else:
        #custom clear function
        clear_cache()
        scopes = ['submit', 'identity']
        #set an oauth link where users can sign in to reddit
        link_no_refresh = r.get_authorize_url('uniqueKey', scopes,  True)
        username = ""
        can_comment = ""

    #if and 'id' is specified in request.GET, do these things
    if 'id' in request.GET:
        threads = request.GET['id']

        if 'name' in request.GET:
            name = request.GET['name']
        else:
            name = ""

    else:
        #GET OUT OF HERE!
        return HttpResponseRedirect('/threads/')

    return render(request, 'comments.html', {
        'username': username,
        'can_comment': can_comment,
        'link': link_no_refresh,
        'threads': threads,
        'message': message,
        'name': name
    })


#reddit oauth redirect url for users that want to login
def redirect_url(request):

    #custom clear function
    clear_cache()

    #Check to see if 'code' is set in the get
    if 'code' in request.GET:

        #get access information from code
        access_information = r.get_access_information(request.GET['code'])

        #set that puppy
        r.set_access_credentials(**access_information)

    return HttpResponseRedirect('/threads/')


#I didn't feel like setting up a websocket app for this app. ajax polling it is. It isn't the best these day.
#also, I didn't like how praw was retrieving data, so built a small api wrapper.
def retrieve(request):

    #ajax is requesting a post
    if request.method == "POST":
        thread = request.POST.get('id')
        the_inst = StreamWrapper(thread)
        full_json = the_inst.the_post()

        return HttpResponse(full_json, content_type="application/json")
    else:

        return HttpResponseRedirect("/threads/")

def send_comment(request):

    #r.login(username=username, password=password)

    if request.method == "POST":

        if r.is_oauth_session():

            submissions = r.get_subreddit('nba').get_new(limit=200)

            id = request.POST.get('id')
            the_thread = []
            comment = request.POST.get('comment')

            for submission in submissions:
                if id in str(submission.id):
                    submission.add_comment(comment)
                    return HttpResponse("comment has been successfully submitted")
        else:
            return HttpResponse("this is some login bullshit")