from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Comment, Group, Follow
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def paginate_queryset(self, queryset):
        if (
            "limit" in self.request.query_params
            or "offset" in self.request.query_params
        ):
            return super().paginate_queryset(queryset)
        return None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = None
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, 
                        post_id=self.kwargs.get("post_id")
                        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["following__username"]
    pagination_class = None
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
