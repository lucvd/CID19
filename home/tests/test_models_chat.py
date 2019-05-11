from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

from home.models import Project
from chat.models import Message, ConversationParticipation, Conversation
from chat.models import get_or_create_participation, conversation_exists, get_unread_message_count


class ChatTestCase(TestCase):
    user1 = None
    user2 = None
    user3 = None
    project1 = None

    def setUp(self):
        self.user1 = User.objects.create_user(username="Testermans", first_name="Jos", last_name="Van Den Eersten", password="123456789")
        self.user2 = User.objects.create_user(username="Testher", first_name="Loewie", last_name="Ter Tweeden",password="123456789")
        self.user3 = User.objects.create_user(username="Test",first_name="Marjan", last_name="Derderlijk", password="123456789")
        self.user1.profile.bio = "mlksj"
        self.user1.profile.headline = "mlksj"
        self.user1.profile.save()
        self.user2.profile.bio = "mlksj"
        self.user2.profile.headline = "mlksj"
        self.user2.profile.save()
        self.user3.profile.bio = "mlksj"
        self.user3.profile.headline = "mlksj"
        self.user3.profile.save()
        self.project1 = Project.objects.create(owner=self.user1, title="First Project", abstract="Abstract",
                                               description="description", created=datetime.now() - timedelta(days=10),
                                               anonymity=False, visible=True)

    def test_get_unread_message_count(self):
        correctparticipation = get_or_create_participation(self.user1, self.user2)
        othercorrectparticipation = get_or_create_participation(self.user1, self.user3)
        wrongparticipation = get_or_create_participation(self.user2, self.user3)
        Message.objects.create(conversation=correctparticipation.conversation, content="test", sender=self.user1,
                               sent_at=datetime.now())
        Message.objects.create(conversation=correctparticipation.conversation, content="test", sender=self.user2,
                               sent_at=datetime.now())
        Message.objects.create(conversation=correctparticipation.conversation, content="test", sender=self.user2,
                               sent_at=datetime.now())
        Message.objects.create(conversation=othercorrectparticipation.conversation, content="test", sender=self.user3,
                               sent_at=datetime.now())
        Message.objects.create(conversation=wrongparticipation.conversation, content="test", sender=self.user2,
                               sent_at=datetime.now())
        Message.objects.create(conversation=wrongparticipation.conversation, content="test", sender=self.user3,
                               sent_at=datetime.now())

        self.assertEqual(get_unread_message_count(self.user1), 3, "All messages of this user should be unread")
        self.assertEqual(get_unread_message_count(self.user2), 2, "All messages of this user should be unread")
        self.assertEqual(get_unread_message_count(self.user3), 1, "All messages of this user should be unread")

        user4 = User.objects.create_user(username="Tes54t", password="123456789")
        user4.profile.bio = "mlksj"
        user4.profile.headline = "mlksj"
        user4.profile.save()
        self.assertEqual(get_unread_message_count(user4), 0,
                         "A user with no conversations should not have any unread messages")

        ''' Read all messages from one conversation. This happens in the overview.html trough javascript and the updateLastRead function in chat/views.py'''
        correctparticipation.amount_unread = 0
        correctparticipation.save()
        self.assertEqual(get_unread_message_count(self.user1), 1,
                         "Two messages should be marked as read, there is one unread left in the other conversation")

    def test_conversation_exists(self):
        get_or_create_participation(self.user1, self.user2)
        self.assertTrue(conversation_exists(self.user1, self.user2), "The conversation between user1 and user2 should exist")
        self.assertFalse(conversation_exists(self.user1, self.user3), "The conversation between user1 and user3 should not exist")

    def test_get_or_create_participation(self):
        self.assertEqual(Conversation.objects.all().count(), 0, "There should not be any conversations at the start")
        self.assertEqual(ConversationParticipation.objects.all().count(), 0, "There should not be any participations at the start")

        conv12 = get_or_create_participation(self.user1, self.user2, otherAnonymous=False, projectID=None)
        self.assertEqual(ConversationParticipation.objects.all().count(), 2, "There should be created 2 participation objects")
        self.assertEqual(get_or_create_participation(self.user2, self.user1).conversation_id, conv12.conversation_id, "The other person should have the same conversation")

        conv23 = get_or_create_participation(self.user2, self.user3)
        self.assertEqual(Conversation.objects.all().count(), 2, "There should be created 2 conversation objects")
        self.assertEqual(ConversationParticipation.objects.all().count(), 4, "There should be created 4 participation objects")

        ''' Create an new, anonymous conversation'''
        get_or_create_participation(self.user1, self.user2, otherAnonymous=True)
        self.assertEqual(Conversation.objects.all().count(), 3, "There should be created 3 conversation objects")
        self.assertEqual(ConversationParticipation.objects.all().count(), 6, "There should be created 6 participation objects")

        ''' Create a project conversation'''
        get_or_create_participation(self.user1, self.user3, projectID=self.project1.id)
        self.assertEqual(Conversation.objects.all().count(), 4, "There should be created 4 conversation objects")
        self.assertEqual(ConversationParticipation.objects.all().count(), 8, "There should be created 8 participation objects")

    def test_conversation_string(self):
        part = get_or_create_participation(self.user1, self.user2)
        self.assertEqual(str(part.conversation), "Jos Van Den Eersten, Loewie Ter Tweeden", "UI components rely on ths string format")

    def test_conversation_last_message(self):
        conversation = get_or_create_participation(self.user1, self.user2).conversation
        Message.objects.create(conversation=conversation, content="Hallo", sender=self.user1, sent_at=datetime.now()-timedelta(days=10))
        Message.objects.create(conversation=conversation, content="Hey!", sender=self.user2, sent_at=datetime.now()-timedelta(days=9))
        Message.objects.create(conversation=conversation, content="Vraag?", sender=self.user1, sent_at=datetime.now()-timedelta(days=5))
        correctID = Message.objects.create(conversation=conversation, content="Antwoord!", sender=self.user2, sent_at=datetime.now()-timedelta(days=2)).id

        otherconv = get_or_create_participation(self.user2, self.user3).conversation
        Message.objects.create(conversation=otherconv, content="Hello!", sender=self.user2, sent_at=datetime.now()-timedelta(days=1))
        Message.objects.create(conversation=otherconv, content="Jow!", sender=self.user3, sent_at=datetime.now())

        self.assertEqual(conversation.last_message_id, correctID, "The last message should be updated in the conversation (to use in UI components)")

    def test_conversationparticipation_string(self):
        participation = get_or_create_participation(self.user1, self.user2)
        self.assertEqual(str(participation), "Jos Van Den Eersten in conversation between: Jos Van Den Eersten, Loewie Ter Tweeden", "UI components rely on this string format")

    def test_conversationparticipation_get_messages(self):
        participation = get_or_create_participation(self.user1, self.user2)
        Message.objects.create(conversation=participation.conversation, content="Hallo", sender=self.user1, sent_at=datetime.now()-timedelta(days=10))
        Message.objects.create(conversation=participation.conversation, content="Hey!", sender=self.user2, sent_at=datetime.now()-timedelta(days=9))
        Message.objects.create(conversation=participation.conversation, content="Vraag?", sender=self.user1, sent_at=datetime.now()-timedelta(days=5))
        Message.objects.create(conversation=participation.conversation, content="Antwoord!", sender=self.user2, sent_at=datetime.now()-timedelta(days=2))
        otherparticipation = get_or_create_participation(self.user2, self.user3)
        Message.objects.create(conversation=otherparticipation.conversation, content="Hello!", sender=self.user2, sent_at=datetime.now()-timedelta(days=1))
        Message.objects.create(conversation=otherparticipation.conversation, content="Jow!", sender=self.user3, sent_at=datetime.now())

        messages = participation.get_messages()
        self.assertEqual(messages.count(), 4, "Only the messages connected to this conversation should be returned")

        for message in messages:
            self.assertEqual(message.conversation_id, participation.conversation_id, "Make sure the messages are from the correct conversation")

    def test_conversationparticipation_get_conversation_name(self):
        participation = get_or_create_participation(self.user1, self.user2)
        projectParticipation = get_or_create_participation(self.user1, self.user3, projectID=self.project1.id, otherAnonymous=True)

        self.assertEqual(participation.get_conversation_name(), self.user2.get_full_name(), "UI components rely on this name format")
        self.assertEqual(projectParticipation.get_conversation_name(), str(self.project1),"UI components rely on this name format")

    def test_conversationparticipation_get_other_participants_string(self):
        participation = get_or_create_participation(self.user1, self.user2)
        self.assertEqual(participation.get_other_participants_string(), self.user2.get_full_name(), "The self should be excludet from this string")

    def test_conversationparticipation_get_other_participants(self):
        participation = get_or_create_participation(self.user1, self.user2)
        get_or_create_participation(self.user2, self.user3)
        get_or_create_participation(self.user1, self.user3)

        other_participants = participation.get_other_participants()
        self.assertEqual(other_participants.count(), 1, "Should only be one")
        self.assertEqual(other_participants.first().get_full_name(), self.user2.get_full_name(), "Should be the correct user")

    def test_message_save(self):
        participation = get_or_create_participation(self.user1, self.user2)
        conversation = participation.conversation
        self.assertEqual(participation.amount_unread, 0, "No unread messages should exist")
        message = Message.objects.create(conversation=conversation, content="Hallo", sender=self.user1, sent_at=datetime.now())

        self.assertEqual(conversation.last_message_id, message.id, "The last message should be updated in a conversation")
        otherparticipation = get_or_create_participation(self.user2, self.user1)
        self.assertEqual(otherparticipation.amount_unread, 1, "A new message should +1 the amount unread")
        self.assertEqual(participation.amount_unread, 0, "The own participation should not increase the unread count")


    def test_message_ordering(self):
        participation = get_or_create_participation(self.user1, self.user2)
        oldest = Message.objects.create(conversation=participation.conversation, content="Hallo", sender=self.user1, sent_at=datetime.now()-timedelta(days=10))
        Message.objects.create(conversation=participation.conversation, content="Hey!", sender=self.user2, sent_at=datetime.now()-timedelta(days=9))
        Message.objects.create(conversation=participation.conversation, content="Vraag?", sender=self.user1, sent_at=datetime.now()-timedelta(days=5))
        newest = Message.objects.create(conversation=participation.conversation, content="Antwoord!", sender=self.user2, sent_at=datetime.now()-timedelta(days=2))

        messages = participation.get_messages()

        self.assertEqual(messages.first().id, oldest.id, 'ORDERING in tests does not always seem to work. Just make sure it is ordered at ["sent_at"]')
        self.assertEqual(messages.last().id, newest.id, 'ORDERING in tests does not always seem to work. Just make sure it is ordered at ["sent_at"]')
            

    def test_conversation_gets_deleted_when_user_is_deleted(self):
        participation1 = get_or_create_participation(self.user1, self.user2)
        participation2 = get_or_create_participation(self.user2, self.user1)
        conversation1 = participation1.conversation
        message1 = Message.objects.create(conversation=conversation1, content="Jow", sender=self.user1, sent_at=datetime.now())
        message2 = Message.objects.create(conversation=conversation1, content="Hi!", sender=self.user2, sent_at=datetime.now())

        participation3 = get_or_create_participation(self.user2, self.user3)
        participation4 = get_or_create_participation(self.user3, self.user2)
        conversation2 = participation3.conversation
        message3 = Message.objects.create(conversation=conversation2, content="Jow", sender=self.user2, sent_at=datetime.now())
        message4 = Message.objects.create(conversation=conversation2, content="Hi!", sender=self.user3, sent_at=datetime.now())


        self.user1.delete()

        self.assertFalse(Message.objects.filter(id=message1.id).exists(), "When a profile is removed, all corresponging conversations, participations and messages should be deleted")
        self.assertFalse(Message.objects.filter(id=message2.id).exists(), "When a profile is removed, all corresponging conversations, participations and messages should be deleted")
        self.assertFalse(ConversationParticipation.objects.filter(id=participation1.id).exists(), "When a profile is removed, all corresponging conversations, participations and messages should be deleted")
        self.assertFalse(ConversationParticipation.objects.filter(id=participation2.id).exists(), "When a profile is removed, all corresponging conversations, participations and messages should be deleted")
        self.assertFalse(Conversation.objects.filter(id=conversation1.id).exists(), "When a profile is removed, all corresponging conversations, participations and messages should be deleted")

        self.assertTrue(Message.objects.filter(id=message3.id).exists(), "Other conversations, participations and messages should not be deleted")
        self.assertTrue(Message.objects.filter(id=message4.id).exists(), "Other conversations, participations and messages should not be deleted")
        self.assertTrue(ConversationParticipation.objects.filter(id=participation3.id).exists(), "Other conversations, participations and messages should not be deleted")
        self.assertTrue(ConversationParticipation.objects.filter(id=participation4.id).exists(), "Other conversations, participations and messages should not be deleted")
        self.assertTrue(Conversation.objects.filter(id=conversation2.id).exists(), "Other conversations, participations and messages should not be deleted")