from rest_framework import serializers
from .models import Cafe, Coordinates, Item, OpeningHours, Feedback, Address, Order
from users.models import User
from users.serializers import UserSerializer


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = (
            "lat",
            "lon"
        )


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "item_id",
            "name",
            "description",
            "time",
            "icon",
            "image",
            "price",
            "type"
        )


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = (
            "opening_time",
            "closing_time"
        )


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            "feedback_id",
            "author",
            "desc",
            "rating",
            "add_time"
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "country",
            "city",
            "street",
            "house",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    customer = UserSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "on_time",
            "order_time",
            "items",
            "payed"
        )

    def create(self, validated_data):
        print(validated_data)


class CafeSerializer(serializers.ModelSerializer):
    cafe_coordinates = CoordinatesSerializer()
    cafe_menu = ItemSerializer(many=True)
    cafe_opening_hours = OpeningHoursSerializer()
    cafe_address = AddressSerializer()

    class Meta:
        model = Cafe
        fields = (
            "cafe_id",
            "cafe_name",
            "cafe_rating",
            "cafe_description",
            "cafe_coordinates",
            "cafe_menu",
            "add_time",
            "icon",
            "cafe_feedback",
            "cafe_opening_hours",
            "cafe_address"
        )
