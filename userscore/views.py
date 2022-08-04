from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
def users(request):
    """
    Fetch All users from global/local leaderboard
    :param request:
    :return:
    """
    try:
        username = request.data.get('username', None)

        if username:
            user_data = User.objects.all().order_by('-score')
            rank = 1
            user = User.objects.filter(name=username).first()

            if user:
                for q in user_data:
                    if q.name != user.name:
                        rank = rank + 1
                    else:
                        break

                serializer = UserSerializer(user_data, many=True)
                current_user = [rank, user.name, user.score]

                params = {'data': serializer.data, 'user': current_user}
                return Response(params)
            else:
                user = User.objects.all().order_by('-score')
                serializer = UserSerializer(user, many=True)
                return Response(serializer.data)
        else:
            user = User.objects.all().order_by('-score')
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
    except:
        return Response("Something went wrong")


@api_view(['POST'])
def create_user(request):
    """
    Create user based on username, score
    :param request:
    :return:
    """
    try:

        username = request.data.get('username', None)

        score = request.data.get('score', 0.0)
        print("score", score)
        user = User.objects.filter(name=username).first()

        if user:
            return Response("User Already exists")

        if not user:  # create user
            user = User(name=username, score=score)
            user.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)

    except:
        return Response("Something Went Wrong")


@api_view(['POST'])
def update_user(request):
    """
    Update user based on score in case of highest score
    :param request:
    :return:
    """
    try:
        username = request.data.get('username', None)

        score = request.data.get('score', None)

        new_score = float(score)

        user = User.objects.filter(name=username).first()
        if user:

            old_score = float(user.score)
            if new_score > old_score:
                user.score = new_score

            user.games_played += 1
            user.save()

            saveserializer = UserSerializer(user)

            # if serializer.is_valid():
            #     serializer.save()
            return Response(saveserializer.data)
            # else:
            #     return Response("old score is greater than new")
        else:
            return Response("User Doesnt Exist")

    except Exception as e:
        return Response("Something Went Wrong")

    return Response("Something Went Wrong")
