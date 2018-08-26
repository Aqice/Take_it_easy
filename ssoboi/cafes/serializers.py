from rest_framework import serializers
from .models import Cafe, Coordinates, Owner, Item, OpeningHours, Feedback


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = (
            "lat",
            "lon"
        )


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = (
            "owner_name",
            "owner_phone_number",
            "owner_email"
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


class CafeSerializer(serializers.ModelSerializer):
    cafe_owner = OwnerSerializer
    cafe_coordinates = CoordinatesSerializer
    cafe_menu = ItemSerializer(many=True)

    class Meta:
        model = Cafe
        fields = (
            "cafe_id",
            "cafe_name",
            "cafe_rating",
            "cafe_description",
            "cafe_coordinates",
            "cafe_owner",
            "cafe_menu",
            "cafe_opening_hours",
            "add_time",
            "icon",
            "cafe_feedback"
        )
