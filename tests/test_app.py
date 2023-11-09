import os
from unittest.mock import Mock, patch

from quizbot.app import main


@patch("quizbot.app.ApplicationBuilder")
def test_can_initialize(mock_application_builder):
    # Mock the return values of the mock objects
    mock_app = Mock()
    mock_application_builder.return_value.token.return_value.build.return_value = (
        mock_app
    )

    # Set up the BOT_TOKEN environment variable
    os.environ["BOT_TOKEN"] = "test-token"

    # call main function
    main()

    mock_application_builder.assert_called_once_with()
    mock_app.add_handler.assert_called()
    assert mock_app.add_handler.call_count == 5
    mock_app.run_polling.assert_called_once_with()
