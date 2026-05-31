from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True
                                          )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Post
        fields = ("id", "text", "author", "pub_date", "group")
        read_only_fields = ("author", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True
                                          )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "post", "created")
        read_only_fields = ("author", "post", "created")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(slug_field="username",
                                        read_only=True
                                        )

    class Meta:
        model = Follow
        fields = ("user", "following")
        read_only_fields = ("user",)

    def validate(self, data):
        request_user = self.context["request"].user
        if data["following"] == request_user:
            raise serializers.ValidationError()
        if Follow.objects.filter(
            user=request_user, following=data["following"]
        ).exists():
            raise serializers.ValidationError()
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
