def expected_assessment_assignment_data(is_assigned=True):
    return {
        "to": "new_assessor_being_assigned@email.com",
        "full_name": "Jeremy Assessor",
        "type": (
            "TEMPLATE_TYPE_ASSESSMENT_APPLICATION_ASSIGNED"
            if is_assigned
            else "TEMPLATE_TYPE_ASSESSMENT_APPLICATION_UNASSIGNED"
        ),
        "content": {
            "reference_number": "REF100",
            "project_name": "My project name",
            "assessment_link": "https://www.gov.uk",
            "message": "I'm assigning you this good luck",
            "lead_assessor_email": "lead_assessor_contact_me_for_suport@email.com",
        },
    }
