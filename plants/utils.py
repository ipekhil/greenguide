from django.core.mail import send_mail
from datetime import date

def send_plant_reminder_email(user, plant, task_type):
    if not user.email:
        return

    task_text = "Water" if task_type == "water" else "Fertilize"
    message = (
        f"Hello {user.username},\n\n"
        f"Reminder: It's time to {task_text.lower()} your plant '{plant.nickname}' today!\n"
        f"Make sure to take care of it to keep it healthy and happy.\n\n"
        "Best regards,\nGreen Guide Team"
    )

    send_mail(
        subject=f"Green Guide Alert - Time to {task_text} '{plant.nickname}' 🌿",
        message=message,
        from_email="info@greenguide.com.tr",
        recipient_list=[user.email],
        fail_silently=True
    )
