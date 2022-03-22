from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.python.eager.context import context
from .predict_model import respond
# from .forms import chatbox_footer
def home(request):
    return render(request, 'templates/rhchatbot/index.html')

def chat(request):
    inp=""
    response_data = {}

    if request.method == 'POST':
        inp = request.POST.get('inp')
        if (inp.lower() == 'signaler mon absence' or inp.lower() == 'dmander un congé' or inp.lower() == "déclarer de l'harcelement"):
            answer="Votre demande est prise en charge. Vous avez besoin d'autres choses?"
        else:
            answer=respond(inp)
        response_data['answer'] = answer
        response_data['inp'] = inp
        return JsonResponse(response_data)
    return render(request, 'templates/rhchatbot/index.html') 
    
  
