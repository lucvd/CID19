from django.contrib import admin

from .models import Conversation, ConversationParticipation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


class ParticipatorsInline(admin.TabularInline):
    model = ConversationParticipation
    extra = 0


class ConversationAdmin(admin.ModelAdmin):
    model = Conversation

    inlines = [
        ParticipatorsInline,
        MessageInline
    ]


admin.site.register(Message)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationParticipation)
