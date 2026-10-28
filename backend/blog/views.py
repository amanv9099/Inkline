from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Blog
from .serializers import BlogSerializer, BlogWriteSerializer


def first_error(errors):
    for value in errors.values():
        if isinstance(value, list) and value:
            return str(value[0])
    return 'Invalid input.'


class BlogListCreateView(generics.ListAPIView):
    """
    GET  /api/blogs/          -> public feed (supports ?search= and ?tag=)
    POST /api/blogs/          -> create a post (auth required)
    """
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Blog.objects.all()
        search = self.request.query_params.get('search')
        tag = self.request.query_params.get('tag')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(body__icontains=search))
        if tag:
            qs = qs.filter(tag__iexact=tag)
        return qs

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You must be logged in to publish a post.'}, status=401)

        serializer = BlogWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': first_error(serializer.errors)}, status=400)

        blog = serializer.save(author=request.user)
        return Response(BlogSerializer(blog).data, status=201)


class MyBlogsView(generics.ListAPIView):
    """GET /api/blogs/mine/ — only the logged-in user's posts."""
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)


class BlogDetailView(APIView):
    """
    GET    /api/blogs/<id>/   -> anyone
    PUT    /api/blogs/<id>/   -> owner only
    DELETE /api/blogs/<id>/   -> owner only
    """
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        return Blog.objects.filter(pk=pk).first()

    def get(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({'error': 'Post not found.'}, status=404)
        return Response(BlogSerializer(blog).data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({'error': 'Post not found.'}, status=404)
        if not request.user.is_authenticated or blog.author_id != request.user.id:
            return Response({'error': 'You can only edit your own posts.'}, status=403)

        serializer = BlogWriteSerializer(blog, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'error': first_error(serializer.errors)}, status=400)
        serializer.save()
        return Response(BlogSerializer(blog).data)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({'error': 'Post not found.'}, status=404)
        if not request.user.is_authenticated or blog.author_id != request.user.id:
            return Response({'error': 'You can only delete your own posts.'}, status=403)

        blog.delete()
        return Response({'success': True})
