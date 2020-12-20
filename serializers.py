from django_enum_choices.serializers import EnumChoiceField
from rest_framework import serializers

# Все примеры кода изъяты из контекста, так как проект, в котором они использовались, защищён NDA


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student_name', 'student_age', 'student_gender', 'student_group')


class UrlSerializer(serializers.ModelSerializer):
    """Сериализатор юрл"""

    class Meta:
        model = Url
        fields = ('id', 'path', 'url', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class AdvertisementSerializer(serializers.ModelSerializer):
    status = EnumChoiceField(read_only=True, enum_class=AdvertisementStatusEnum)
    photos = serializers.SerializerMethodField()
    state = AutoStateSerializer(required=False)
    option = ReverseSelectableOptionsSerializer(many=True, required=False)
    condition = AdvertisementConditionSerializer(required=False)
    contact = AdvertisementContactSerializer(required=False)
    car = AdvertisementAutoModificationSerializer(required=False)
    vin_code = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    def get_photos(self, instance):
        if not instance.photos.exists():
            return [
                {
                    'id': None,
                    'main_img': True,
                    'photo': ServiceConfig.get_solo().default_auto_image.url,
                    'created': None,
                    'modified': None
                },
            ]

        else:
            return AdvertisementPhotoSerializer(instance.photos, many=True).data

    def get_credit(self, instance):
        if instance.credit:
            return str(round(instance.credit.amount))

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'year_manufactured',
            'contact',
            'status',
            'created',
            'modified',
            'vin_code',
            'option',
            'condition',
            'state',
            'car',
            'photos',
            'popular',
            'is_prime',
            'pub_date',
            'credit',
        )

    def get_vin_code(self, instance):
        if instance.vin_code is not None:
            return re.sub(r'(?<=.{3}).', '*', instance.vin_code)
