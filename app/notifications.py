from django.conf import settings
from django.core.mail import send_mail

from .models import ModelJobAlert, ModelSkill


def notification_job_alert(data):
    """
    Notifications are sent to people who have subscribed to job alerts
    """
    name = data["name"] if "name" in data else ""
    salary = data["salary"] if "salary" in data else ""
    country = data["country"] if "country" in data else ""
    skill = data["skill"] if "skill" in data else ""

    job_alerts_with_filter = ModelJobAlert.objects.filter(
        salary_min__lte=salary, salary_max__gte=salary,
        country__icontains=country
    ).values_list("name", "email")

    job_alerts_without_filter = ModelJobAlert.objects.filter(
        name=None, salary_min=None, salary_max=None, country=None
    ).values_list("email")

    skills = ModelSkill.objects.filter(
        id__in=skill).values_list("skill", flat=True)
    skills = ", ".join(skills)

    html_message = (
        f"Name: {name}<br>Country: {country}<br>Salary: {salary}<br>Skills: {skills}"
    )
    message = f"Name: {name}\nCountry: {country}\nSalary: {salary}\nSkills: {skills}"

    for job_alert in job_alerts_with_filter:
        if job_alert[0].lower() in name.lower():
            send_mail(
                f"Job Alert: {name}",
                message,
                settings.SENDER,
                [job_alert[1]],
                fail_silently=True,
                html_message=html_message,
            )

    for job_alert in job_alerts_without_filter:
        send_mail(
            f"Job Alert: {name}",
            message,
            settings.SENDER,
            [job_alert[0]],
            fail_silently=True,
            html_message=html_message,
        )
