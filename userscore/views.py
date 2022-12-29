from .models import User, Levels
from rest_framework.response import Response
from .serializers import UserSerializer, LevelSerializer
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
        level = request.data.get('level', None)
        if username and level:
            level = Levels.objects.filter(level_id=level).order_by('-level_score')
            if level:
                serializer = LevelSerializer(level, many=True)
                return Response(serializer.data)
            else:
                user = User.objects.all().order_by('-score')
                serializer = UserSerializer(user, many=True)
                return Response(serializer.data)
        elif username:
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

        level = request.data.get('level', None)

        new_score = float(score)

        user = User.objects.filter(name=username).first()
        if user:
            level_table = Levels.objects.filter(
                user=user,
                level_id=level,
            ).first()
            if level_table:
                old_score = float(level_table.level_score)
                if new_score > old_score:
                    level_table.level_score = new_score
                    user.score += new_score
                level_table.save()
                user.games_played += 1
                user.save()
            else:
                level_table = Levels(user=user, level_score=new_score, level_id=level)
                user.score += new_score
                user.games_played += 1
                user.save()
                level_table.save()

            saveserializer = LevelSerializer(level_table)

            # if serializer.is_valid():
            #     serializer.save()
            return Response(saveserializer.data)
            # else:
            #     return Response("old score is greater than new")
        else:
            return Response("User Doesnt Exist")

    except Exception as e:
        return Response("Something Went Wrong")
        print("abc")
    return Response("Something Went Wrong")
