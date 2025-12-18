import uuid


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


def test_create_missing_required_fields(user_service):
    # Missing first_name
    payloads = [
        {'last_name': 'X', 'dob': '1990-01-01', 'likes_chocolate': 'L'},
        {'first_name': 'X', 'dob': '1990-01-01', 'likes_chocolate': 'L'},
        {'first_name': 'X', 'last_name': 'Y', 'likes_chocolate': 'L'},
    ]
    for p in payloads:
        r = user_service.create_user(p)
        assert r is not None
        # expect validation error when required fields missing
        assert r.status_code in (400, 422), f'Expected validation error but got {r.status_code} {r.text}'


def test_delete_nonexistent_and_invalid_ids(user_service):
    # non-existent numeric id
    r = user_service.delete('99999999')
    assert r is not None
    assert r.status_code in (404, 410, 200, 204), f'Unexpected delete status {r.status_code} {r.text}'

    # invalid id format
    r2 = user_service.delete('not-an-id')
    assert r2 is not None
    assert r2.status_code in (400, 404, 410), f'Unexpected delete status for invalid id {r2.status_code} {r2.text}'


def test_double_delete(user_service):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'Del{unique}',
        'last_name': 'Tester',
        'dob': '1990-01-01',
        'likes_chocolate': 'L',
    }
    r = user_service.create_user(payload)
    assert r is not None
    assert r.status_code in (200, 201, 202)
    try:
        body = r.json()
    except Exception:
        body = {}
    user_id = _extract_id(body)
    assert user_id

    d1 = user_service.delete(user_id)
    assert d1 is not None
    assert d1.status_code in (200, 202, 204), f'First delete unexpected: {d1.status_code} {d1.text}'

    d2 = user_service.delete(user_id)
    assert d2 is not None
    assert d2.status_code in (404, 410, 200, 204), f'Second delete unexpected: {d2.status_code} {d2.text}'
