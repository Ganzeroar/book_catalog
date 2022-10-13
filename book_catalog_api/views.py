from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Books, Favorites, Reviews
from .serializer import GetBookSerializer, FavoriteSerializer, CreateReviewSerializer
from rest_framework.permissions import IsAuthenticated


class GetBook(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            queryset = Books.objects.filter(pk=pk)
        else:
            queryset = Books.objects.all()
        return queryset

    serializer_class = GetBookSerializer


class FavoritesAPIView(generics.views.APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, book_id, user_id):
        try:
            return Favorites.objects.get(book=book_id, user=user_id)
        except Favorites.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book_id = pk
        user_id = request.user.id
        event = self.get_object(book_id, user_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateReview(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = CreateReviewSerializer
    permission_classes = (IsAuthenticated, )
