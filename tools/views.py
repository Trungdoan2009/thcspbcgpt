# chat_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

import requests

#Asssign your API key below
#Get it from here:
#https://platform.openai.com/api-keys
apiKey = "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"


def chat(request):
    return render(request, 'tools/chatgpt.html')
# ...
@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        try:
            # Make an HTTP request to the OpenAI API
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": "Bearer "+str(apiKey)+""},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        },
                        {
                            "role": "system",
                            "content": "How can I help you?"
                        }
                    ]
                }
            )

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Get the response from the OpenAI API
            response_json = response.json()
            
            # Access the 'content' field
            content = response_json['choices'][0]['message']['content']

            # Return the assistant response
            return JsonResponse({'response': content})
        
        except requests.exceptions.RequestException as e:
            # Handle API request errors
            return JsonResponse({'error': f'Error making OpenAI API request: {str(e)}'})

    else:
        return JsonResponse({'error': 'Invalid request method'})
