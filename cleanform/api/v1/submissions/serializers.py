from rest_framework import serializers
from cleanform.models.submission import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'id',
            'data',
            'created_at'
        ]
