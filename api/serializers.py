from rest_framework.serializers import ModelSerializer, SerializerMethodField, FloatField
from .models import User, Class, AssignmentType, Assignment, Semester

DEFAULT_GRADE_SCALE = [(97, 'A+'), (93, 'A'), (90, 'A-'), (87, 'B+'), (83, 'B'), (80, 'B-'), (77, 'C+'), (73, 'C'),
                       (70, 'C-'), (67, 'D+'), (63, 'D'), (60, 'D-')]


def get_letter_grade(score, scale=DEFAULT_GRADE_SCALE):
    for (min_score, letter) in scale:
        if score >= min_score:
            return letter
    return 'F'


GPA_VALUES = {
    'A+': 4,
    'A': 4,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1,
    'D-': .7,
    'F': 0
}


def get_grade_points(units, score, scale=GPA_VALUES):
    letter_grade = get_letter_grade(score)
    points = GPA_VALUES[letter_grade]
    return points * units

def get_gpa(classes):
    gp = [get_grade_points(cls.units, cls.score) for cls in classes]
    units = sum([cls.units for cls in classes])
    return sum(gp) / units


class UserSerializer(ModelSerializer):
    classes = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_classes(self, user):
        user_classes = user.classes.all()
        serializer = ClassSerializer(user_classes, many=True)
        return serializer.data


class AssignmentSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentTypeSerializer(ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    total_score = FloatField(read_only=True)
    max_total_score = FloatField(read_only=True)

    class Meta:
        model = AssignmentType
        fields = '__all__'


class ClassSerializer(ModelSerializer):
    assignment_types = AssignmentTypeSerializer(many=True, read_only=True)
    score = SerializerMethodField()
    semester_str = SerializerMethodField()

    class Meta:
        model = Class
        fields = '__all__'

    def get_score(self, obj):
        return obj.score

    def get_semester_str(self, obj):
        return str(obj.semester)


class SemesterSerializer(ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    gpa = SerializerMethodField()

    class Meta:
        model = Semester
        fields = '__all__'

    def get_gpa(self, obj):
        classes = obj.classes.all()
        gpa = get_gpa(classes)
        return gpa
