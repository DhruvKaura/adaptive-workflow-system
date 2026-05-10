from app.domains.workflow.rules import VALID_TRANSITIONS


class WorkflowService:

    @staticmethod
    def validate_transition(current_status: str, new_status: str):

        allowed = VALID_TRANSITIONS.get(current_status, set())

        return new_status in allowed
