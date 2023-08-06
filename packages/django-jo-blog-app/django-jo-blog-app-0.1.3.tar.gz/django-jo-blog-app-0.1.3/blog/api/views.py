from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializers
from .pagination import CustomResultsSetPagination
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Post.objects.all()

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message": "request limit exceeded",
              "availableIn": f"{wait} seconds"
        })


class BlogPostCreateView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message": "request limit exceeded",
              "availableIn": f"{wait} seconds"
        })


class BlogPostListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializers
    pagination_class = CustomResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Post.objects.all()

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message": "request limit exceeded",
              "availableIn": f"{wait} seconds"
        })


class BlogPostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message": "request limit exceeded",
              "availableIn": f"{wait} seconds"
        })


class BlogPostRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message": "request limit exceeded",
              "availableIn": f"{wait} seconds"
        })
