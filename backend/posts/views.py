from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from . import permissions as perm
from . import models
from . import serializers
from . import paginations


class TweetViewSet(viewsets.ModelViewSet):
    queryset = models.Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    permission_classes = [perm.IsAuthorOrIsAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = paginations.TweetNumberPagination
    pagination_class = LimitOffsetPagination
    search_fields = ['text', 'profile__user__username']
    ordering_fields = ['updated_at', 'profile__user_id']

    def perform_create(self, serializer):

        serializer.save(profile=self.request.user.profile)

    @action(methods=['POST'], detail=True,
            serializer_class=serializers.ReactionSerializer,
            permission_classes=[permissions.IsAuthenticated],
            )
    def reaction(self, request, pk=None):
        serializer = serializers.ReactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=self.request.user.profile, tweet=self.get_object())
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ReactionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ReactionType.objects.all()
    serializer_class = serializers.ReactionTypeSerializer
    permission_classes = [perm.IsAdminOrReadOnly]


class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])


class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
    permission_classes = [permissions.IsAuthenticated, perm.IsAuthorOrIsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ['text']
    ordering_fields = ['updated_at']

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile, tweet_id=self.kwargs['tweet_id'])


class ReplyReactionCreateAPIView(generics.CreateAPIView):
    queryset = models.ReplyReaction.objects.all()
    serializer_class = serializers.ReplyReactionSerializer
    permission_classes = [perm.IsAuthorOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            reply=get_object_or_404(models.Reply, pk=self.kwargs['reply_id']),
            profile=self.request.user.profile
        )
