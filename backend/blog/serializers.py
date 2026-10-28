from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """Read shape — used for feed, single post, and 'mine'."""
    author = UserSerializer(read_only=True)
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'body', 'tag', 'author', 'createdAt', 'updatedAt']

    def get_createdAt(self, obj):
        return int(obj.created_at.timestamp() * 1000)

    def get_updatedAt(self, obj):
        return int(obj.updated_at.timestamp() * 1000) if obj.updated_at else None


class BlogWriteSerializer(serializers.ModelSerializer):
    """Write shape — used for create and update."""
    class Meta:
        model = Blog
        fields = ['title', 'body', 'tag']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('A post needs a title.')
        return value

    def validate_body(self, value):
        if not value.strip():
            raise serializers.ValidationError('A post needs some body text.')
        return value
