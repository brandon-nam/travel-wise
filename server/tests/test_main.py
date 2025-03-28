from unittest.mock import patch, MagicMock


from src.main import main, create_app


def test_main() -> None:
    mock_app = MagicMock()
    with (patch("src.main.create_app") as mock_create_app_func,):
        mock_create_app_func.return_value = mock_app
        main()
        mock_create_app_func.assert_called_once()
        mock_app.run.assert_called_once_with(host="0.0.0.0", port=3203)


def test_create_app() -> None:
    mock_app = MagicMock()
    mock_repo = MagicMock()
    with (
        patch("src.main.__name__") as mock_name,
        patch("src.main.Flask") as mock_flask,
        patch("src.main.CORS") as mock_cors,
        patch("src.main.ServerRepository") as mock_server_repo,
        patch("src.main.create_routes") as mock_create_routes,
    ):
        mock_flask.return_value = mock_app
        mock_server_repo.return_value = mock_repo
        returned_app = create_app()
        mock_flask.assert_called_once_with(mock_name)
        mock_cors.assert_called_once_with(mock_app)
        mock_repo.setup_db.assert_called_once_with(mock_app)
        mock_create_routes.assert_called_once_with(mock_app, mock_repo)
        assert returned_app == mock_app
