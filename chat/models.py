from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, F, Sum

from home.models import Project


def get_unread_message_count(user):
    result = ConversationParticipation.objects.filter(user=user).aggregate(Sum('amount_unread'))['amount_unread__sum']
    if result is None:
        return 0
    return result


def conversation_exists(userSelf, userOther, otherAnonymous=False):
    # if adding more users, also change the number of particpants variable
    numberOfParticipants = 2
    return Conversation.objects.annotate(partCount=Count('participants')).filter(partCount=numberOfParticipants).filter(conversationparticipation__user_id__in=[userOther.id], conversationparticipation__anonymous=otherAnonymous).filter(conversationparticipation__user_id__in=[userSelf.id]).exists()


def get_or_create_participation(userSelf, userOther, otherAnonymous=False, projectID=None):
    if not conversation_exists(userSelf, userOther, otherAnonymous):
        if projectID:
            conversation = Conversation.objects.create(project=Project.objects.get(pk=projectID), anonymous=otherAnonymous)
        else:
            conversation = Conversation.objects.create()
        partOther = ConversationParticipation.objects.create(conversation=conversation, user=userOther, anonymous=otherAnonymous)
        partSelf = ConversationParticipation.objects.create(conversation=conversation, user=userSelf)
        return partSelf
    else:
        # if adding more users, also change the number of particpants variable
        numberOfParticipants = 2
        conversation = Conversation.objects.annotate(partCount=Count('participants')).filter(partCount=numberOfParticipants).filter(conversationparticipation__user_id__in=[userOther.id], conversationparticipation__anonymous=otherAnonymous).filter(conversationparticipation__user_id__in=[userSelf.id]).first()
        return ConversationParticipation.objects.get(user=userSelf, conversation=conversation)


class Conversation(models.Model):
    participants = models.ManyToManyField(User, through='ConversationParticipation')
    last_message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name="last_message", null=True,
                                     blank=True)
    anonymous = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return ', '.join(p.get_full_name() for p in self.participants.all())


# ManyToMany field with intermediate model
class ConversationParticipation(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)
    amount_unread = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() + " in conversation between: " + str(self.conversation)

    def get_messages(self):
        return self.conversation.message_set.all()

    def get_conversation_name(self):
        if self.conversation.anonymous:
            return self.conversation.project.title
        else:
            return self.get_other_participants_string()

    def get_other_participants_string(self):
        users = []
        for p in self.conversation.participants.all():
            if p.id is not self.user_id:
                users.append(p.get_full_name())
        return ', '.join(users)

    def get_other_participants(self):
        return User.objects.filter(pk__in=self.conversation.conversationparticipation_set.exclude(pk=self.id).values_list('user_id'))

    class Meta:
        verbose_name_plural = "Participants"
        unique_together = ('conversation', 'user')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender) + ": " + self.content[:50]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conversation.last_message = self
        self.conversation.save()
        # increace the amount_unread for all ConvPeraticipations except from this user.
        self.conversation.conversationparticipation_set.exclude(user=self.sender).update(amount_unread=F('amount_unread')+1)

    class Meta:
        ordering = ["sent_at"]
