from rest_framework import viewsets
from rest_framework.response import Response
from .models import BodyMeasurement
from .serializers import BodyMeasurementSerializer
from rest_framework.permissions import AllowAny

class BodyMeasurementViewSet(viewsets.ModelViewSet):
    queryset = BodyMeasurement.objects.all()
    serializer_class = BodyMeasurementSerializer
    permission_classes = [AllowAny]  # Add this line

    def create(self, request, *args, **kwargs):
        measurements_data = request.data.get('measurements', {})
        
        # Prepare data for serializer
        data = {
            'weight': request.data.get('weight'),
            'weight_unit': request.data.get('weight_unit', 'kg'),
            'neck': measurements_data.get('neck'),
            'shoulders': measurements_data.get('shoulders'),
            'left_bicep': measurements_data.get('leftBicep'),
            'right_bicep': measurements_data.get('rightBicep'),
            'left_tricep': measurements_data.get('leftTricep'),
            'right_tricep': measurements_data.get('rightTricep'),
            'left_forearm': measurements_data.get('leftForearm'),
            'right_forearm': measurements_data.get('rightForearm'),
            'upper_abs': measurements_data.get('upperAbs'),
            'waist': measurements_data.get('waist'),
            'hips': measurements_data.get('hips'),
            'left_calf': measurements_data.get('leftCalf'),
            'right_calf': measurements_data.get('rightCalf'),
            'left_thigh': measurements_data.get('leftThigh'),
            'right_thigh': measurements_data.get('rightThigh'),
        }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)