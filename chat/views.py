import json

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from rules.contrib.views import objectgetter, permission_required

from django.core.mail import send_mail

from chat.forms import MessageForm
from home.models import Project

from .models import (ConversationParticipation, Message, conversation_exists,
                     get_or_create_participation, get_unread_message_count)


@login_required(login_url='/login')
def index(request):
    # TODO redirect to correct conversation
    mostRecentParticipation = ConversationParticipation.objects.filter(user=request.user).order_by(
        '-conversation__last_message').first()  # TODO custom manager maken voor deze volgorde
    if mostRecentParticipation is None:
        return render(request, 'chat/no_messages.html')
    return redirect('chat:detail', participationID=mostRecentParticipation.id,
                    conversationname=slugify(mostRecentParticipation.get_conversation_name()))


@login_required(login_url='/login')
@permission_required('chat.conversation_participation_belongs_to_me',
                     fn=objectgetter(ConversationParticipation, 'participationID'), raise_exception=True)
def detail(request, participationID, conversationname=None):
    participations = ConversationParticipation.objects.filter(user=request.user).order_by(
        '-conversation__last_message')  # TODO custom manager maken voor deze volgorde
    activeConversation = ConversationParticipation.objects.get(pk=participationID)

    anonymousUserIDs = []
    for part in activeConversation.conversation.conversationparticipation_set.all():
        if part.anonymous and part.user_id is not request.user.id:
            anonymousUserIDs.append(part.user_id)

    context = {
        'participations': participations,
        'messages': activeConversation.get_messages(),
        'participants': activeConversation.get_other_participants(),
        'participation': activeConversation,
        'userid': request.user.id,
        'messageForm': MessageForm(),
        'anonymousUserIDs': anonymousUserIDs,
    }
    return render(request, "chat/overview.html", context)


@login_required(login_url='/login')
def newMessage(request, userID=None, projectID=None):
    # if projectID is none, a new message to a user is requested
    user = request.user
    if userID:
        anonymous = False
        otherUser = get_object_or_404(User, pk=userID)
    # if userID is none, a conversation about a project is requested where the project owner is anonymous
    else:
        anonymous = True
        otherUser = get_object_or_404(Project, pk=projectID).owner

    if request.method == "POST":  # a message is been send
        form = MessageForm(request.POST)
        if form.is_valid():
            messagetext = form.cleaned_data['message']
            participation = get_or_create_participation(user, otherUser, anonymous, projectID)
            Message.objects.create(conversation=participation.conversation, content=messagetext, sender=user)
            return redirect('chat:detail', participationID=participation.id,
                            conversationname=slugify(participation.get_conversation_name()))

    else:  # the page is loaded, ready to send a new message
        # if the conversation already exists, move to that conversation
        if conversation_exists(user, otherUser, anonymous):
            participation = get_or_create_participation(user, otherUser, anonymous)
            return redirect('chat:detail', participationID=participation.id,
                            conversationname=slugify(participation.get_conversation_name()))
        else:  # otherwise, prepare to receive a new message
            context = {
                'messageForm': MessageForm(),
            }
            if userID:
                context['otherUser'] = get_object_or_404(User, pk=userID)
            else:
                context['project'] = get_object_or_404(Project, pk=projectID)

            return render(request, "chat/new_message.html", context)


@login_required(login_url='/login')
def sendMessage(request, participationID=None):
    # send message and redirect to the conversation
    form = MessageForm(request.POST)
    if form.is_valid():
        messagetext = form.cleaned_data['message']

        subject = 'Test email when new message is sent'
        message = 'This is the message content, if you read this the test has worked! Daijoubu!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to_list, fail_silently=False)

        if participationID:
            participation = ConversationParticipation.objects.get(pk=participationID)
            if request.user == participation.user:
                Message(conversation=participation.conversation, content=messagetext, sender=request.user).save()
        return redirect('chat:detail', participationID=participationID, conversationname=slugify(
            participation.get_conversation_name()))  # TODO participation is niet altijd geinitialisseerd


@login_required(login_url='/account/login')
def getNumberOfUnreadChats(request):
    return JsonResponse({'unread': get_unread_message_count(request.user)})


@login_required(login_url='/login')
def updateLastRead(request):
    data = json.loads(request.body)
    participationID = data['participationID']
    participation = ConversationParticipation.objects.get(pk=participationID)
    if participation.user == request.user:
        participation.amount_unread = 0
        participation.save()
    return JsonResponse({'total_unread': get_unread_message_count(request.user)})
