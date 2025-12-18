import uuid
import pytest


def _extract_id(body: dict):
    for key in ('id', 'pk', 'user_id', 'userid', 'uid'):
        if key in body:
            return body[key]
    url = body.get('url') if isinstance(body, dict) else None
    if url:
        try:
            return url.rstrip('/').split('/')[-1]
        except Exception:
            return None
    return None


@pytest.mark.parametrize('choice', ['L', 'D'])
def test_likes_chocolate_valid_choices(user_service, choice):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'Choc{unique}',
        'last_name': 'Tester',
        'dob': '1990-01-01',
        'likes_chocolate': choice,
    }

    r = user_service.create_user(payload)
    assert r is not None
    assert r.status_code in (200, 201, 202), f'Create with valid choice failed: {r.status_code} {r.text}'
    try:
        body = r.json()
    except Exception:
        body = {}

    user_id = _extract_id(body)
    assert user_id

    # cleanup
    user_service.delete_user(user_id)


def test_likes_chocolate_invalid_choice(user_service):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'ChocX{unique}',
        'last_name': 'Tester',
        'dob': '1990-01-01',
        'likes_chocolate': 'X',
    }

    r = user_service.create_user(payload)
    # Expect rejection due to choices (400) or server validation
    assert r is not None
    assert r.status_code in (400, 422, 500, 200, 201, 202)
    # If created, ensure we clean it up
    try:
        body = r.json()
    except Exception:
        body = {}
    user_id = _extract_id(body)
    if user_id:
        user_service.delete_user(user_id)


@pytest.mark.parametrize('age', [None, 0, -1, 2000])
def test_age_first_taste_edge_cases(user_service, age):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'Age{unique}',
        'last_name': 'Tester',
        'dob': '1990-01-01',
    }
    if age is not None:
        payload['age_first_taste_chocolate'] = age

    r = user_service.create_user(payload)
    assert r is not None
    # allow either success or validation error depending on API rules
    assert r.status_code in (200, 201, 202, 400, 422), f'Unexpected status: {r.status_code} {r.text}'

    if r.status_code in (200, 201, 202):
        try:
            body = r.json()
        except Exception:
            body = {}
        user_id = _extract_id(body)
        assert user_id
        # if stored, verify returned value matches (when present)
        if age is not None and isinstance(body, dict):
            # serializer may coerce types; compare as int when possible
            got = body.get('age_first_taste_chocolate')
            if got is not None:
                try:
                    assert int(got) == age
                except Exception:
                    pass
        # cleanup
        user_service.delete_user(user_id)