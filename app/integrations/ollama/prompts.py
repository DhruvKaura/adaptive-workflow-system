def build_workflow_summary_prompt(risk_score, reasons):

    return f"""
    Analyze this workflow task.

    Risk Score: {risk_score}

    Reasons:
    {", ".join(reasons)}

    Provide:
    - short operational summary
    - recommendation
    """
