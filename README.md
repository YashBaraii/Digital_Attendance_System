# 📘 Digital Attendance System with QR Code

A modern, QR code–based class attendance system built using **Django**, **Django REST Framework**, **JWT authentication**, and **PostgreSQL**. This project streamlines and secures student attendance using role-based access control, QR scanning, and real-time reporting.

> 🔗 **Live Demo**: [Website](https://digital-attendance-system-28f1.onrender.com/)  
> 🔗 **Swagger API Docs**: [Website Docs](https://digital-attendance-system-28f1.onrender.com/docs) <br/>
> 🔗 **Postman Testing Workspace**: [Workspace Link with deployed url](https://www.postman.com/test55-1090/workspace/digital-attendance-system-deployed-url)                              
> 🔗 **Data Seeding Automation**: [Instructions](https://github.com/YashBaraii/Digital_Attendance_System/blob/main/docs/seed_data_instructions.md)

**Note**: Workspace.json contains the postman workspace link which has been used to test the api endpoints, available at docs/

---

## 📂 Folder Structure

```
Digital_Attendance_System/
├── attendance/
├── classroom/
├── digital_attendance/        # Project core
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── users/                     # Custom user model, auth, roles
├── media/qr_codes/            # ⬅️ QR code images stored here
├── templates/index.html       # Project documentation homepage
├── docs/
│   ├── DAS_API_Testing_Workflow.postman_collection.json  # Postman testing collection
│   └── seed_data_instructions.md                         # Data seeding steps
├── manage.py
├── README.md
├── LICENSE
├── env.txt             # Env secrets
├── requirements.txt
```

---

## 🚀 Features

🔐 **Authentication** - JWT-based login and registration with roles (student, teacher)  
🧑‍🏫 **Role-Based Access** - Teachers manage classes, generate sessions. Students enroll and check stats  
🏫 **Class Management** - Teachers create/update/delete classes  
🧑‍🎓 **Student Enrollment** - Students can enroll into available classes  
📷 **QR Code Generation** - Each session generates a unique scannable QR code  
✅ **Attendance Tracking** - Students mark attendance via QR scanning  
📊 **Attendance Reports** - Summaries by class and student  
📤 **CSV Export** - Export class-wise attendance as `.csv`  
📬 **Email Alerts** - Notify on absence  
🛡️ **API Throttling** - Rate limiting for safety and stability

---

## 🧱 Tech Stack

| Layer          | Technology                    |
| -------------- | ----------------------------- |
| Backend        | Django, Django REST Framework |
| Authentication | SimpleJWT                     |
| Database       | PostgreSQL (Railway)          |
| QR Code        | `qrcode` + `Pillow`           |
| Docs           | Swagger (`drf-yasg`), ReDoc   |
| Frontend       | Custom HTML                   |
| DevOps         | GitHub, Render                |

---

## 🧩 Model Structure

### 🔐 `User`

```bash

from django.contrib.auth.models import AbstractUser
from django.db import models

class Institution(models.Model):  # Optional bonus model
    name = models.CharField(max_length=200)

class User(AbstractUser):
    ROLE_CHOICES = (("teacher", "Teacher"), ("student", "Student"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)

```

| Field       | Type       | Description                          |
| ----------- | ---------- | ------------------------------------ |
| username    | string     | Unique username                      |
| email       | string     | User email                           |
| password    | string     | Password (hashed)                    |
| role        | choice     | `student` or `teacher`               |
| institution | ForeignKey | Optional institution (bonus feature) |

### 🏫 `Classroom`

```bash

from django.db import models
from users.models import User

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classrooms")

```

| Field   | Type     | Description         |
| ------- | -------- | ------------------- |
| name    | string   | Name of the class   |
| subject | string   | Subject taught      |
| teacher | FK(User) | Teacher who owns it |

### 🧾 `Enrollment`

```bash

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

```

| Field     | Type     | Description       |
| --------- | -------- | ----------------- |
| student   | FK(User) | Enrolled student  |
| classroom | FK       | Related classroom |

### 📷 `Session`

```bash

import uuid

class Session(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    date = models.DateField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

```

| Field         | Type  | Description                |
| ------------- | ----- | -------------------------- |
| session_id    | UUID  | Unique session ID          |
| classroom     | FK    | Related classroom          |
| date          | date  | Auto-set on creation       |
| qr_code_image | Image | Path to generated QR image |

### 📝 `Attendance`

```bash

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(default="present")
    timestamp = models.DateTimeField(auto_now_add=True)

```

| Field     | Type        | Description                 |
| --------- | ----------- | --------------------------- |
| student   | FK(User)    | Attending student           |
| session   | FK(Session) | Attended session            |
| status    | string      | "present"                   |
| timestamp | DateTime    | Auto-set on attendance mark |

---

## 🔗 API Endpoints

### 🧍 Authentication (User)

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| POST   | `/api/auth/register/`      | Register a new user  |
| POST   | `/api/auth/token/`         | Login + JWT pair     |
| POST   | `/api/auth/token/refresh/` | Refresh access token |

### 🏫 Classrooms

| Method | Endpoint                       | Description                 |
| ------ | ------------------------------ | --------------------------- |
| GET    | `/api/classrooms/`             | List all classes            |
| POST   | `/api/classrooms/`             | Create class (teacher only) |
| GET    | `/api/classrooms/{id}/`        | View a specific class       |
| PUT    | `/api/classrooms/{id}/`        | Update class                |
| DELETE | `/api/classrooms/{id}/`        | Delete class                |
| POST   | `/api/classrooms/{id}/enroll/` | Enroll student in a class   |

### 📷 QR & Attendance

| Method | Endpoint                                            | Description                       |
| ------ | --------------------------------------------------- | --------------------------------- |
| POST   | `/api/attendance/classrooms/{id}/generate-session/` | Generate session QR (teacher)     |
| POST   | `/api/attendance/mark/`                             | Mark attendance (student scan QR) |
| GET    | `/api/attendance/student/{id}/summary/`             | Student summary                   |
| GET    | `/api/attendance/student/{id}/summary/?start=&end=` | Student summary by date           |
| GET    | `/api/attendance/class/{id}/summary/`               | Class-wide attendance summary     |
| GET    | `/api/attendance/class/{id}/summary/?start=&end=`   | Class summary by date             |
| GET    | `/api/attendance/class/{id}/export/`                | Export CSV                        |
| GET    | `/api/attendance/dashboard/summary/`                | Overall system stats              |

---

## ⚙️ Setup Instructions (Local)

1. Clone Project

```bash
git clone https://github.com/YashBaraii/Digital_Attendance_System.git
cd Digital_Attendance_System
```

2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On MacOS: source venv/bin/activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set up .env (Refer the env.txt) <br/>
   Create .env:

```bash

# Mandatory
SECRET_KEY=
DEBUG=

# Database Secrets
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# OR

DATABASE_URL=postgresql://<user>:<pass>@localhost:5432/db_name

# Email Secrets
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

```

6. Run Migrations

```bash
python .\manage.py makemigrations
python .\manage.py migrate
```

7. Create Superuser (optional)

```bash
python .\manage.py createsuperuser
```

8. Run Server

```bash
python .\manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🧪 Testing

```bash
# Run built-in tests
python manage.py test

```
**Optional**: Visit doc/seed_data_intructions.md (For populating data)

---

## 👨‍💻 Contributors

- [@YashBaraii](https://github.com/YashBaraii) – Developer
- DevifyX – Internship Assignment Provider

---

## 📄 License

This project is licensed under the [MIT License](https://github.com/YashBaraii/Digital_Attendance_System/blob/deployment/LICENSE).

---

## 📬 Contact

Have questions or suggestions? Feel free to reach out:
📧 yashbarai2308@gmail.com
