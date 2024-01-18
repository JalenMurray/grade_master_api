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
    if not classes:
        return 0.0
    gp = [get_grade_points(cls.units, cls.score) for cls in classes]
    units = sum([cls.units for cls in classes])
    return sum(gp) / units


class UserSerializer(ModelSerializer):
    semesters = SerializerMethodField()
    current_semester = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_semesters(self, user):
        user_semesters = user.semesters.all()
        if user_semesters:
            serializer = SemesterSerializer(user_semesters, many=True, read_only=True)
            return serializer.data
        else:
            return None

    def get_current_semester(self, user):
        user_semesters = user.semesters.all()
        current_semester = user_semesters.filter(current=True).first()
        if current_semester:
            serializer = SemesterSerializer(current_semester, many=False, read_only=True)
            return serializer.data
        else:
            return None


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
