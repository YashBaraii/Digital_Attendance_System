from rest_framework import serializers
from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "id",
            "classroom",
            "session_id",
            "date",
            "qr_code_image",
            "qr_code_url",
        ]

    def get_qr_code_url(self, obj):
        request = self.context.get("request")
        if obj.qr_code_image and request:
            return request.build_absolute_uri(obj.qr_code_image.url)
        return None
