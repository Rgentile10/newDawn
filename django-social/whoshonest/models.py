# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import openai

# API_KEY = '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'
# openai.api_key = API_KEY

# model_id = 'gpt-3.5-turbo'

# def ChatGPT_conversation(conversation):
#     response = openai.ChatCompletion.create(
#         model=model_id,
#         messages=conversation
#     )
#     # api_usage = response['usage']
#     # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
#     # stop means complete
#     # print(response['choices'][0].finish_reason)
#     # print(response['choices'][0].index)
#     conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
#     return conversation

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     follows = models.ManyToManyField(
#         "self", related_name="followed_by",
#         symmetrical=False, blank=True
#     )
#     def __str__(self):
#         return self.user.username
    
# class Message(models.Model):
#     user = models.ForeignKey(
#         User, related_name="messages", on_delete=models.DO_NOTHING
#     )
#     body = models.CharField(max_length=140)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         conversation = []
#         conversation.append({'role': 'system', 'content': 'How may I help you?'})
#         conversation = ChatGPT_conversation(conversation)
#         #print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
#         prompt = 'Reply yes or no to the following question: is this sentence hate speech: "' + self.body[:100] + '"'
#         conversation.append({'role': 'user', 'content': prompt})
#         conversation = ChatGPT_conversation(conversation)
#         print('{1}\n'.format(conversation[-1]['content'].strip()))
#         gptoutput = '{1}\n'.format(conversation[-1]['content'].strip())
#         hatespeech = "No"
#         all_words = gptoutput.split()
#         first_word = all_words[0]
        
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

conversation = []
conversation.append({'role': 'system', 'content': 'How may I help you?'})
conversation = ChatGPT_conversation(conversation)
print("Please enter in a statement and we will return whether or not the statement is considered hate speech using AI/ML models")

while True:
    prompt = 'Reply yes or no to the following question: is this sentence considered hate speech: "' + input('User:') + '"'
    conversation.append({'role': 'user', 'content': prompt})
    conversation = ChatGPT_conversation(conversation)
    #print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
    returnanswer = "NO"
    gptoutput = '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
    print(gptoutput)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = Profile(user=instance)
#         user_profile.save()
#         user_profile.follows.set([instance.profile.id])
#         user_profile.save()

    