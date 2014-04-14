from django.shortcuts import render
import praw
from django.http import HttpResponseRedirect
from models import InsertCommentForm
from django.template import loader, Context, RequestContext

def retrieve_threads(request):

    r = praw.Reddit(user_agent='r_nba_live_stream')
    submissions = r.get_subreddit('nba').get_top(limit=25)
    game_threads = []
    the_text = []

    for submission in submissions:
        if "GAME THREAD" in str(submission):
            game_threads.append(submission.id)
            the_text.append(submission)

    return render(request, 'game_threads.html', {
        'game_threads': game_threads,
        'the_text': the_text,
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