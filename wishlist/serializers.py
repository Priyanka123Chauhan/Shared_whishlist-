from rest_framework import serializers
from .models import Wishlist, Product

class WishlistSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'name', 'description', 'created_at', 'item_count', 'created_by_username', 'contributors']

    def get_item_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'wishlist', 'name', 'image_url', 'price', 'added_by', 'added_by_username', 'created_at']
