import pytest

from app.notification.assessment.map_contents import Assignment
from app.notification.model.notification import Notification
from examplar_data.assessment_data import expected_assessment_assignment_data


@pytest.mark.usefixtures("live_server")
def test_assignment_correctly_maps_from_external_JSON():
    data = expected_assessment_assignment_data(is_assigned=True)
    notification = Notification.from_json(data)
    assignment = Assignment.from_notification(notification)

    # mapping within the template type specific content
    assert assignment.lead_assessor_email == data["content"]["lead_assessor_email"]

    # mapping at the top level notification
    assert assignment.contact_info == data["to"]


@pytest.mark.parametrize("mock_notifications_api_client", [2], indirect=True)
def test_assigned_notification_sends_given_correct_payload(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
):
    _, code = Notification.email_recipient(expected_assessment_assignment_data(is_assigned=True))

    assert code == 200


@pytest.mark.parametrize("mock_notifications_api_client", [2], indirect=True)
def test_unassigned_notification_sends_given_correct_payload(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
):
    _, code = Notification.email_recipient(expected_assessment_assignment_data(is_assigned=False))

    assert code == 200
