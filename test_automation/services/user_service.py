from typing import Any, Optional


class UserService:
    def __init__(self, http_client):
        """Wrapper around HttpClient for user-related operations.

        The `http_client` is expected to provide `get`, `post`, `put`, `delete` methods.
        """
        self.client = http_client

    # Generic HTTP methods (convenience wrappers)
    def get(self, path: str = '', **kwargs) -> Any:
        return self.client.get(path, **kwargs)

    def post(self, path: str = '', json: Optional[dict] = None, data: Optional[dict] = None, **kwargs) -> Any:
        return self.client.post(path, json=json, data=data, **kwargs)

    def put(self, path: str = '', json: Optional[dict] = None, data: Optional[dict] = None, **kwargs) -> Any:
        return self.client.put(path, json=json, data=data, **kwargs)

    def patch(self, path: str = '', json: Optional[dict] = None, data: Optional[dict] = None, **kwargs) -> Any:
        return self.client.session.patch(self.client._url(path), json=json, data=data, **kwargs)

    def delete(self, path: str = '', **kwargs) -> Any:
        return self.client.delete(path, **kwargs)

    # Backwards-compatible convenience methods
    def create_user(self, payload: dict) -> Any:
        return self.post('', json=payload)

    def get_user(self, user_id: str | int) -> Any:
        return self.get(str(user_id))

    def update_user(self, user_id: str | int, payload: dict) -> Any:
        # use PATCH for partial updates (API expects full object for PUT)
        return self.patch(str(user_id), json=payload)

    def delete_user(self, user_id: str | int) -> Any:
        return self.delete(str(user_id))
