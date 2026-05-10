from celery import shared_task


@shared_task
def generate_ai_summary(
    project_name: str
):

    return (
        f"AI-generated summary for "
        f"project: {project_name}"
    )