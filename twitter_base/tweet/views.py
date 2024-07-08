from django.shortcuts import render
from django.urls import path
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets':tweets})


# ways of serving forms are pretty standardised
# there are 3 ways: 
# 1. serve an empty form
# 2. there is a req from a form and we're handling the req
# 3. we already have the form data and we'll just render the form


def tweet_create(request):
    if(request.method == "POST"):
       form = TweetForm(request.POST, request.FILES)
       if form.isvalid():
           tweet = form.save(commit=False)
           tweet.user = request.user
           tweet.save()
           return redirect('tweet_list')  
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form':form}) #form has the data of TweetForm

def tweet_edit(request, tweet_id):
    # tweet data is required cause obvbiusly some data is required such as model or structure so that we can edit the tweet
    # thats why we use object or 404, as either we'll get the object/data or we'll get status 404
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user )
    #pk is primary key, and request.user coz we only want the user to edit and not anyone else 
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance = tweet)
        if form.is_valid(): #takes care of securities like csrf protection an all
            tweet = form.save(commit=False)
            # we'll save the tweet but make the commit false because we have to add user to it too
            tweet.user = request.user
            tweet.save() #saved the user
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet) #since ther is some data in a tweet that we might want to edit, we are using instance and passing off tweet to it
    return render(request, 'tweet_form.html', {'form':form}) #form has the data of TweetForm


def tweet_delete(request, tweet_id): #to delete or edit we need a tweet id
    tweet = get_object_or_404(Tweet, pk =tweet_id, user = request.user) #we have to find out which tweet it is, check in model Tweet, primary key is tweet id, and user must be the owner of the account
    if(request.method == 'POST'): #checking if the method being called is post
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet':tweet})
# something has to be rendered even before post request is recieved before deletion