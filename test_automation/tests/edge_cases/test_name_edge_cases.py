import uuid
import pytest
import json


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


@pytest.mark.parametrize('first,last,expected', [
    ('Alice', 'Smith', 'success'),
    ('', 'Smith', 'invalid'),
    (' ', 'Smith', 'invalid'),
    (None, 'Smith', 'invalid'),
    ('A'*30, 'Smith', 'success'),
    ('A'*31, 'Smith', 'either'),
    ('José', 'García', 'success'),
    ('😀', 'Smith', 'either'),
    ("Anne-Marie", "O'Neil", 'success'),
    ('123', '456', 'either'),
    ('a\nb', 'Smith', 'either'),
    ('', '', 'invalid'),
    ('\t', 'Smith', 'invalid'),
    ('x'*1000, 'y'*1000, 'invalid'),
])
def test_name_edge_cases(user_service, first, last, expected):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'{first}' if first is not None else None,
        'last_name': f'{last}' if last is not None else None,
        'dob': '1990-01-01',
        'likes_chocolate': 'L',
    }

    # remove keys if explicitly None to simulate missing fields
    if payload['first_name'] is None:
        payload.pop('first_name')
    if payload['last_name'] is None:
        payload.pop('last_name')

    # ensure unique non-empty names when input is empty strings to avoid collisions
    if payload.get('first_name') == '' and expected != 'invalid':
        payload['first_name'] = f'EmptyFirst{unique}'
    if payload.get('last_name') == '' and expected != 'invalid':
        payload['last_name'] = f'EmptyLast{unique}'

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
        user_service.delete_user(user_id)
    elif expected == 'invalid':
        assert r.status_code in (400, 422), f'Expected validation error but got {r.status_code} {r.text}'
    else:
        assert r.status_code in (200, 201, 202, 400, 422), f'Unexpected status {r.status_code} {r.text}'
