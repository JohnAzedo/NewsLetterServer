from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from news.models import News, Comment, UserNews


class NewsListSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'created_at', 'author', 'number_comments', 'number_likes')


class CommentSerializer(ModelSerializer):
    user = serializers.StringRelatedField(many=False, source='user.get_full_name')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'news', 'text', 'created_at']
        extra_kwargs = {
            'news': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(
            user=user,
            text=validated_data['text'],
            news=validated_data['news']
        )

        return comment


class NewsSerializer(ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'subtitle', 'author', 'number_likes', 'number_comments', 'text', 'comments', 'created_at']


class UserNewsSerializer(ModelSerializer):

    class Meta:
        model = UserNews
        fields = ['news', 'liked', 'read']

    def create(self, validated_data):
        user_news = UserNews.objects.create(
            user=self.context['request'].user,
            news=validated_data['news'],
            read=validated_data['read'],
            liked=validated_data['liked']
        )

        return user_news