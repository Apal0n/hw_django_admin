from rest_framework import serializers
from django.db.utils import IntegrityError

from . import models


class TweetSerializer(serializers.ModelSerializer):
    reactions = serializers.ReadOnlyField(source='get_reactions')
    all_reactions = serializers.ReadOnlyField()

    class Meta:
        model = models.Tweet
        fields = "__all__"
        read_only_fields = ['profile', ]


class ReplySerializer(serializers.ModelSerializer):
    get_reactions = serializers.ReadOnlyField()

    class Meta:
        model = models.Reply
        fields = "__all__"
        read_only_fields = ['profile', 'tweet']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reaction
        fields = "__all__"
        read_only_fields = ['profile', 'tweet']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            new_reaction_type = validated_data.pop('reaction')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.reaction = new_reaction_type
            instance.save()
            return instance


class ReactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactionType
        fields = "__all__"


class ReplyReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReplyReaction
        fields = "__all__"
        read_only_fields = ['profile', 'reply']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            new_reaction_type = validated_data.pop('reaction')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.reaction = new_reaction_type
            instance.save()
            return instance
