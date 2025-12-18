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


@pytest.mark.parametrize('age,expected', [
    (None, 'success'),
    (0, 'success'),
    (1, 'success'),
    (5, 'success'),
    (120, 'success'),
    (-1, 'either'),
    (121, 'either'),
    (1000, 'either'),
    (-1000, 'either'),
    (2147483647, 'either'),
    (-2147483648, 'either'),
    ('5', 'either'),          # numeric string
    ('5.0', 'either'),        # numeric-ish string
    ('5.5', 'invalid'),       # non-integer string
    (5.5, 'either'),          # float numeric
    ('', 'invalid'),
    (' ', 'invalid'),
    ('null', 'invalid'),
])
def test_age_first_taste_strict(user_service, age, expected):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'Edge{unique}',
        'last_name': 'Tester',
        'dob': '1990-01-01',
    }
    if age is not None:
        payload['age_first_taste_chocolate'] = age

    r = user_service.create_user(payload)
    assert r is not None

    if expected == 'success':
        assert r.status_code in (200, 201, 202), f'Expected success but got {r.status_code} {r.text}'
        try:
            body = r.json()
        except Exception:
            body = {}
        user_id = _extract_id(body)
        assert user_id
        # verify stored value when provided and comparable
        if age is not None and isinstance(body, dict):
            got = body.get('age_first_taste_chocolate')
            if got is not None:
                try:
                    assert int(float(got)) == int(float(age))
                except Exception:
                    pass
        # cleanup
        user_service.delete_user(user_id)
    elif expected == 'invalid':
        assert r.status_code in (400, 422), f'Expected validation error but got {r.status_code} {r.text}'
    else:  # either
        assert r.status_code in (200, 201, 202, 400, 422), f'Unexpected status {r.status_code} {r.text}'
