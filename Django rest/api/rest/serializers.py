from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 120)
    author = serializers.CharField(max_length = 120)
    email = serializers.EmailField()
    date = serializers.DateTimeField(auto_now_add=True)

    def create(self,validated_data):
        return Article.objects.create(validated_data)

    def update(self,instance,validated_data):
        instance.title = validated_data.get()