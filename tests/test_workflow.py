from app.domains.workflow.service import WorkflowService


def test_valid_transition():

    valid = WorkflowService.validate_transition("todo", "in_progress")

    assert valid is True


def test_invalid_transition():

    valid = WorkflowService.validate_transition("completed", "todo")

    assert valid is False
