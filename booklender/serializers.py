from rest_framework import serializers
from .models import userData, borrowerDetails, AddBook, ReviewList


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = userData
        exclude = ['password']  


class BorrowerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = borrowerDetails
        fields = '__all__'


class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddBook
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewList
        fields = '__all__'
