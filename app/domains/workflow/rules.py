VALID_TRANSITIONS = {
    "todo": {"in_progress", "blocked"},
    "in_progress": {"review", "blocked", "completed"},
    "review": {"completed", "in_progress"},
    "blocked": {"todo", "in_progress"},
    "completed": set(),
}
