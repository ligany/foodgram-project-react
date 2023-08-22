from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Follow
from .paginator import CustomPaginator
from .serializers import CustomUserSerializer, ShowFollowSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticated)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        author = get_object_or_404(User, pk=pk)
        user = request.user

        if author == user:
            return Response(
                {'errors': 'Нельзя фолловить себя'},
                status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(author=author, user=user).exists():
            return Response(
                {'errors': 'Уже есть такая подписка'},
                status=status.HTTP_400_BAD_REQUEST)

        obj = Follow(author=author, user=user)
        obj.save()

        serializer = ShowFollowSerializer(
            author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        try:
            subscription = get_object_or_404(Follow, user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                'Отписаться не получилось',
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListFollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ShowFollowSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
