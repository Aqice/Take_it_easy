from rest_framework import serializers
from .models import Cafe, Coordinates, Item, OpeningHours, Feedback, Address


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
