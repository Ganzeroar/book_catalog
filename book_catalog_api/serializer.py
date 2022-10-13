from rest_framework import serializers

from .models import Books, Favorites, Reviews
import statistics


class GetBookSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    average_raiting = serializers.SerializerMethodField()
    genre_name = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    is_in_favorites = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        book_id = obj.pk
        reviews = Reviews.objects.filter(book=book_id).values()
        return reviews

    def get_average_raiting(self, obj):
        book_id = obj.pk
        reviews = Reviews.objects.filter(book=book_id).values()
        if not reviews:
            return None

        raitings = []
        for review in reviews:
            raitings.append(review['raiting'])

        return round(statistics.mean(raitings), 2)

    def get_genre_name(self, obj):
        return obj.genre_id.name

    def get_author_name(self, obj):
        return obj.author_id.name

    def get_is_in_favorites(self, obj):
        user_id = self.context['request'].user.id
        if not user_id:
            return None

        book_id = obj.pk
        favorites_obj = Favorites.objects.filter(book=book_id, user=user_id)

        return bool(favorites_obj)

    class Meta:
        model = Books
        fields = ('__all__')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('__all__')

    def create(self, validated_data):
        book = validated_data['book']
        user = validated_data['user']
        self._validate_favorite_is_not_exist(book, user)
        return self._create_favorite(book, user)

    def _create_favorite(self, book, user):
        return Favorites.objects.create(
            book=book,
            user=user,
        )

    def _validate_favorite_is_not_exist(self, book, user):
        favorites_obj = Favorites.objects.filter(
            book=book,
            user=user,
        )
        if favorites_obj:
            raise serializers.ValidationError({'message': 'Already exist'})


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('__all__')

    def create(self, validated_data):
        book = validated_data['book']
        user = validated_data['user']
        raiting = validated_data['raiting']
        review_text = validated_data['review_text']

        self._validate_review_is_not_exist(book, user)
        return self._create_review(book, user, raiting, review_text)

    def _create_review(self, book, user, raiting, review_text):
        return Reviews.objects.create(
            book=book,
            user=user,
            raiting=raiting,
            review_text=review_text,
        )

    def _validate_review_is_not_exist(self, book, user):
        reviews_obj = Reviews.objects.filter(
            book=book,
            user=user,
        )
        if reviews_obj:
            raise serializers.ValidationError({'message': 'Already exist'})
