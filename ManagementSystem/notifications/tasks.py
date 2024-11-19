from celery import shared_task
from django.core.mail import send_mail
from .models import Student, Grade
from datetime import date


@shared_task
def send_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            subject="Attendance Reminder",
            message="Please mark your attendance for today.",
            from_email="admin@example.com",
            recipient_list=[student.email],
        )
    return f"Attendance reminders sent to {students.count()} students."


@shared_task
def send_grade_update_notification(student_id, course_name, grade):
    student = Student.objects.get(id=student_id)
    send_mail(
        subject="Grade Updated",
        message=f"Your grade for {course_name} has been updated to {grade}.",
        from_email="admin@example.com",
        recipient_list=[student.email],
    )
    return f"Grade notification sent to {student.name}."


@shared_task
def daily_report():
    attendance_data = "Attendance summary for today..."
    grade_data = "Grades summary for today..."
    report = f"{attendance_data}\n\n{grade_data}"

    send_mail(
        subject="Daily Report",
        message=report,
        from_email="admin@example.com",
        recipient_list=["admin@example.com"],
    )
    return "Daily report sent."
