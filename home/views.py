import datetime
import json

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.db.models import Q
from requests.exceptions import MissingSchema
from rules.contrib.views import objectgetter, permission_required
from tellme.models import Feedback
import bugsnag

from .forms import ProfileForm, ProfilePictureForm, ProjectForm
from .models import Profile, Project, User, SuccessStory, FeedbackProject

from ConnectID.choices import *


@never_cache
def index(request):

    '''
        This is the view when browsing to the root of the website.
        If the user is logged in, redirect to the landing page with login information
        Otherwise, (user not logged in), redirect him to basic landing
    '''

    if request.user.is_authenticated:
        if request.user.profile.profilePicture :
            context = {
                'loggedin': True,
                'user': request.user,
                'currentYear': datetime.datetime.now().year,
                'successtories': SuccessStory.objects.all(),
            }
            return render(request, 'home/landing.html', context)
        else:
            return redirect('profile/edit/picture')
    else:
        context = {
            'currentYear': datetime.datetime.now().year,
            'loggedin': False,
            'successtories': SuccessStory.objects.all(),
        }
        return render(request, 'home/landing.html', context)


def loginSuccess(request):
    '''
        This view gets called after logging in, to redirect to the home page (ommitting the landing page)
        If his profile picture is not set, it should redirect to the edit profile picture page
    '''
    bugsnag.notify(Exception("Testing bugsnag :)"))
    if request.user.is_authenticated:
        if request.user.profile.profilePicture:
            return redirect('/projects')
        else:
            return redirect('profile/edit/picture')
    else:
        return redirect('/')


def login(request):
    return redirect('social:begin', backend='linkedin-oauth2')


@login_required(login_url='/login')
def logout(request):
    # LOGOUT should be post request. https://stackoverflow.com/questions/3521290/logout-get-or-post
    if request.method == 'POST':
        auth_logout(request)
        return redirect('/')
    else:
        return render(request, 'home/logout_confirmation.html')

@never_cache
@login_required(login_url='/login')
def projects(request):
    projects = Project.objects.all()
    favorites = request.user.profile.favorites.values_list('id', flat=True)

    '''
    #code for primitive search function, not used anymore because too slow
    
    query = request.GET.get("q")
    if query:
        projects = projects.filter(  #Q encapsulates a single LIKE query
            Q(title__icontains=query) |
            Q(abstract__icontains=query) |
            Q(keywords__icontains=query) |
            Q(description__icontains=query)).distinct()
            '''

    context = {
        'projects': projects,
        'favorites': favorites,
    }
    
    return render(request, 'home/home.html', context)  # TODO customscript aanpassen

@never_cache
@login_required(login_url='/login')
def profilepage(request, userID, slugName):
    user = get_object_or_404(User, pk=userID)
    profile = user.profile
    projects = Project.objects.filter(owner=user, visible=True, anonymity=False)

    context = {
        'profile': profile,
        'projects': projects,
        'userID': userID,
    }
    return render(request, 'home/profile.html', context)

@login_required(login_url='/login')
def ownprofilepage(request):
    return redirect('home:profile', userID=request.user.id, slugName=request.user.get_full_name().replace(" ","_"))


@login_required(
    login_url="/login")  # no further permissions needed, form is filled out with the logged-in users's data
def editprofilepage(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile.save()
            return redirect('home:ownProfile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'home/edit_profile.html', {'form': form, 'profile': profile})

@login_required(login_url="/login")
def editprofilepicturepage(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    errorOnUploadedPicture = False
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home:ownProfile')
        else:
            for e in form.errors:
                print(e)
                # TODO log error (but also that is is non fatal!)
            errorOnUploadedPicture = True

    linkedinNotOk = True
    # check if image from linkedin is still accessable
    # TODO if linkedin profile pictures are fixed, try to get it from the 'Python Social Auth' - 'User Social Auth' model's extra data
    # See the issue on Github and the comment in edit_profile_picture.html arround line 35
    try:
        # It used to be that the link broke after awhile.
        # Make sure to check if the link exists (is not none)  and it is still reachable
        ''' 
        # It used to be this:
        result = requests.get(profile.linkedInProfilePictureURL) 
        if result.status_code is 200:
        '''
        if True: # Temporary, as long as the linkedin picture is not working
            linkedinNotOk = True
    except MissingSchema:
        # TODO log
        linkedinNotOk = True

    form = ProfilePictureForm(instance=profile)
    context = {'form': form,
               'profile': profile,
               'linkedinNotOk': linkedinNotOk,
               'error': errorOnUploadedPicture
               }
    return render(request, 'home/edit_profile_picture.html', context )


@login_required(login_url="/login")
def users(request):
    context = {
        'profiles': Profile.objects.order_by('-id'),
    }
    return render(request, 'home/users.html', context)

@never_cache
@login_required(login_url='/login')
@permission_required('projects.can_view', fn=objectgetter(Project, 'projectID'))
def projectpage(request, projectID, slugTitle):
    bugsnag.notify(Exception("Testing bugsnag :)"))
    project = get_object_or_404(Project, id=projectID)

    context = {
        'project': project,
    }

    if request.user.profile.favorites.filter(id=projectID).exists():
        context.update({'favorite': 'true'})

    return render(request, 'home/project.html', context)


@login_required(login_url='/login')
def newprojectpage(request, projectID="newproject"):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'submit_form' in request.POST:
            # create a form instance and populate it with data from the request:
            if projectID == "newproject":
                form = ProjectForm(request.POST)
            else:
                project = get_object_or_404(Project, id=projectID)
                form = ProjectForm(request.POST, instance=project)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required

                project = form.save(commit=False)
                project.owner = request.user
                # project.projectType = request.POST.get('type')
                # get all values from the 5 buttons, if text is empty ignore.
                project.save()

                return redirect('home:projects')
        elif 'add_keyword' in request.POST:
            formset = ProjectForm(request.POST)
            if formset.is_valid():
                for form in formset:
                    # only save if name is present
                    if form.cleaned_data.get('name'):
                        form.save()
            return redirect('home:newproject')

    # if a GET (or any other method) we'll create a blank form
    else:
        if projectID == "newproject":
            form = ProjectForm()
        else:
            project = get_object_or_404(Project, id=projectID)
            form = ProjectForm(instance=project)

    return render(request, 'home/new_project.html', {'form': form})


@login_required(login_url='/login')
@permission_required('projects.edit_project', fn=objectgetter(Project, 'projectID'))
def editprojectpage(request, projectID):
    project = get_object_or_404(Project, id=projectID)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save()

            return redirect('home:projects')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm(instance=project)

    return render(request, 'home/new_project.html', {'form': form})


@login_required(login_url='/login')
def togglefavorite(request):
    data = json.loads(request.body)
    projectID = data["projectID"]
    project = Project.objects.get(id=projectID)
    profile = request.user.profile

    if profile.favorites.filter(id=projectID).exists():
        profile.favorites.remove(project)
    else:
        profile.favorites.add(project)

    return JsonResponse({
        'projectID': projectID,
    })


@permission_required('common.is_staff')
@login_required(login_url='/login')
def feedback(request):
    context = {
        'feedbacks': Feedback.objects.all(),
    }
    return render(request, 'home/feedback.html', context)

@permission_required('projects.is_owner', fn=objectgetter(Project, 'projectID'))
@login_required(login_url='/login')
def deleteproject(request, projectID):
    print(request.body)
    data = json.loads(request.body)
    projectNameGuess = data['projectNameGuess']
    feedback = data['feedback']

    actualProject = get_object_or_404(Project, pk=projectID)

    if projectNameGuess == actualProject.title:
        Project.objects.filter(pk=projectID).delete()
        response = {'removed': True}
        feedbackmodel = FeedbackProject()
        feedbackmodel.feedback = feedback
        feedbackmodel.save()

    else:
        response = {'removed': False}

    return JsonResponse(response)


def bad_request(request):
    return render(request, 'home/error_pages/400.html')

def permission_denied(request):
    return render(request, 'home/error_pages/403.html')

def not_found(request):
    return render(request, 'home/error_pages/404.html')

def server_error(request):
    return render(request, 'home/error_pages/500.html')