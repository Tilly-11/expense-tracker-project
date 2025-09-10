from rest_framework import serializers
from .models import Expense
from .ai_utils import predict_category

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'description', 'category', 'date',
                  'predicted_category', 'ai_confidence', 'user_override', 'created_at', 'updated_at']
        read_only_fields = ['user', 'predicted_category', 'ai_confidence', 'user_override', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        # set user
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user

        description = validated_data.get('description', '') or ''
        supplied_category = validated_data.get('category', '').strip()

        # Only call AI if no category provided
        if not supplied_category:
            label, conf = predict_category(description)
            validated_data['predicted_category'] = label
            validated_data['ai_confidence'] = conf
            validated_data['category'] = label  # default to predicted category
            validated_data['user_override'] = False
        else:
            validated_data['user_override'] = True

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If user updates category manually, mark user_override True.
        new_category = validated_data.get('category', None)
        if new_category is not None and new_category != instance.predicted_category:
            validated_data['user_override'] = True
        return super().update(instance, validated_data)