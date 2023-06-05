import pytest
from app.notification.application.map_contents import Application
from app.notification.model.multi_input_data import MultiInput
from examplar_data.application_data import multi_input_test_data


class TestMultiInput:
    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                multi_input_test_data["process_data"]["multiple_values"][
                    "input_data"
                ],
                multi_input_test_data["process_data"]["multiple_values"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["process_data"]["single_value"][
                    "input_data"
                ],
                multi_input_test_data["process_data"]["single_value"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["process_data"]["iso_values"][
                    "input_data"
                ],
                multi_input_test_data["process_data"]["iso_values"][
                    "expected_response"
                ],
            ),
        ],
    )
    def test_process_data(self, app_context, input_data, expected_response):

        response = MultiInput.process_data(input_data)

        assert response == expected_response

    @pytest.mark.parametrize(
        "input_data, expected_response",
        [
            (
                multi_input_test_data["map_data"]["multiple_values"][
                    "input_data"
                ],
                multi_input_test_data["map_data"]["multiple_values"][
                    "expected_response"
                ],
            ),
            (
                multi_input_test_data["map_data"]["single_value"][
                    "input_data"
                ],
                multi_input_test_data["map_data"]["single_value"][
                    "expected_response"
                ],
            ),
        ],
    )
    def test_map_multi_input_data(
        self, app_context, input_data, expected_response
    ):

        response = Application.map_multi_input_data(input_data)

        assert response == expected_response
