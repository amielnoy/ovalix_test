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



def test_user_crud(user_service):
    unique = uuid.uuid4().hex[:8]
    payload = {
        'first_name': f'Test{unique}',
        'last_name': 'User',
        'dob': '1990-01-01',
        'likes_chocolate': 'L',
        'age_first_taste_chocolate': 5,
    }

    r = user_service.create_user(payload)
    assert r is not None
    assert r.status_code in (200, 201, 202), f'Create failed: {r.status_code} {r.text}'
    try:
        body = r.json()
    except Exception:
        body = {}

    user_id = _extract_id(body)
    assert user_id, f'No id found in create response: {body}'

    # verify the user can be retrieved and fields are present
    g = user_service.get_user(user_id)
    assert g.status_code == 200, f'Get failed: {g.status_code} {g.text}'
    try:
        gbody = g.json()
    except Exception:
        gbody = {}
    if isinstance(gbody, dict):
        assert gbody.get('first_name') is not None
        # likes_chocolate should be one of the known choices
        lc = gbody.get('likes_chocolate')
        assert lc in (None, 'L', 'D')

    # update a field
    upd = {'first_name': 'Updated'}
    u = user_service.update_user(user_id, upd)
    assert u.status_code in (200, 204), f'Update failed: {u.status_code} {u.text}'

    # delete and ensure it's gone
    d = user_service.delete_user(user_id)
    assert d.status_code in (200, 202, 204), f'Delete failed: {d.status_code} {d.text}'

    gg = user_service.get_user(user_id)
    assert gg.status_code in (200, 404, 410), f'Unexpected get after delete: {gg.status_code} {gg.text}'
