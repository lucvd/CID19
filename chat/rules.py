import rules


@rules.predicate
def user_is_conversation_participant(user, conversationParticipation):
    return conversationParticipation.user == user


rules.add_perm('chat.conversation_participation_belongs_to_me', user_is_conversation_participant)
