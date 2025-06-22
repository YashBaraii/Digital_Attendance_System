Step-by-Step Process to Populate the Database:

✅ **_Step 1_**: Open the Django Shell

```bash
python manage.py shell
```

✅ **_Step 2_**: Paste This Full Script to Seed Sample Data (You can tweak the size as per your requirements)

```bash
from django.core.management.base import BaseCommand
from users.models import User
from classroom.models import Classroom, Enrollment
from attendance.models import Session, Attendance
from django.utils import timezone
from datetime import timedelta
import uuid, random

class Command(BaseCommand):
help = "Seeds the database with sample teachers, students, classes, sessions, and attendance."

    def handle(self, *args, **kwargs):
        self.stdout.write("🔁 Resetting database (excluding superusers)...")

        User.objects.exclude(is_superuser=True).delete()
        Classroom.objects.all().delete()
        Enrollment.objects.all().delete()
        Session.objects.all().delete()
        Attendance.objects.all().delete()

        self.stdout.write("✅ Old data cleared.")

        # Create Teachers
        teachers = []
        for i in range(1, 6):
            t = User.objects.create_user(
                username=f"teacher{i}",
                email=f"teacher{i}@example.com",
                password="pass123",
                role="teacher",
            )
            teachers.append(t)

        # Create Students
        students = []
        for i in range(1, 51):
            s = User.objects.create_user(
                username=f"student{i}",
                email=f"student{i}@example.com",
                password="pass123",
                role="student",
            )
            students.append(s)

        # Create Classrooms
        subjects = [
            "Math",
            "Biology",
            "Physics",
            "Chemistry",
            "History",
            "CS",
            "Economics",
            "English",
            "Geography",
            "Art",
        ]
        classrooms = []
        for i in range(10):
            c = Classroom.objects.create(
                name=f"{subjects[i]} {i+1}01",
                subject=subjects[i],
                teacher=random.choice(teachers),
            )
            classrooms.append(c)

        # Enroll students (5 to 10 per class)
        for classroom in classrooms:
            class_students = random.sample(students, k=random.randint(5, 10))
            for student in class_students:
                Enrollment.objects.create(student=student, classroom=classroom)

        # Create sessions (last 7 days)
        sessions = []
        today = timezone.now().date()
        for classroom in classrooms:
            for day in range(7):
                session = Session.objects.create(
                    classroom=classroom,
                    session_id=uuid.uuid4(),
                    date=today - timedelta(days=day),
                )
                sessions.append(session)

        # Attendance marking
        for session in sessions:
            enrolled = Enrollment.objects.filter(classroom=session.classroom)
            for enrollment in enrolled:
                if random.random() > 0.2:  # 80% present rate
                    Attendance.objects.create(
                        student=enrollment.student, session=session, status="present"
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "🎉 Seeding complete! Sample data added to the database."
            )
        )
```
