from django.shortcuts import render
from django.http import JsonResponse
from .models import Level, KryptosUser, User
from django.views.decorators.csrf import csrf_exempt


from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.


def test(request):
    response = {'success': True}
    return JsonResponse(response)

@api_view(['GET'])
def ask(request):
    
    # TODO: Fetch user level from DB
    user_level = 1
    level = Level.objects.filter(level=user_level)[0]
    response = {
        'level': user_level,
        'source_hint': level.source_hint
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['POST'])
def answer(request):
    user_id = request.data['user_id']
    answer = request.data['answer']
    try:
        user = User.objects.get(user_id=user_id)
        kuser = KryptosUser.objects.get(user_id=user)
        level = Level.objects.get(level=kuser.level)
        if answer == level.answer:
            print(user, " answered level ", kuser.level, " correctly.")
            kuser.level += 1
            kuser.save()
            response = {'answer': 'Correct'}
        else:
            response = {'answer': 'Wrong'}
    except Exception as e:
        print (e)
        response = {'error': 'User not found'}
    finally:  
        return JsonResponse(response)
