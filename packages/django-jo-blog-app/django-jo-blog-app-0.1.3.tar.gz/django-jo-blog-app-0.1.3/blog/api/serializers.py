from rest_framework import serializers
from blog.models import Post


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'body'
        ]

        read_only_fields = ['id']

    def validate_title(self, value):
        qs = Post.objects.filter(title=value)
        if self.instance:
            qs = qs.exclude(title=self.instance.title)
        if qs.exists():
            raise serializers.ValidationError(
                'This title has already been used!'
            )
        return value
