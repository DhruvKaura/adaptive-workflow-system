from app.core.celery.worker import celery_app


@celery_app.task
def process_workflow_event(event_type: str, task_id: str):

    print(f"Processing event: " f"{event_type} for task {task_id}")

    return {"processed": True}
