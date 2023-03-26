from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import openai

API_KEY = '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'
openai.api_key = API_KEY

model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by",
        symmetrical=False, blank=True
    )
    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    user = models.ForeignKey(
        User, related_name="messages", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        conversation = []
        conversation.append({'role': 'user', 'content': 'reply with a "yes" or a "no" to this question: is this sentence hate speech: "' + models.CharField(max_length=140) + '"'})
        conversation = ChatGPT_conversation(conversation)
        answer = str('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d}): "
            f"{self.body[:30]}..."
            f" Possible hate speech: " + answer
        )

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

    