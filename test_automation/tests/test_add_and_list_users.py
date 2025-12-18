import uuid
import json


def _extract_id(body: dict):
    for key in ('id', 'pk', 'user_id', 'userid', 'uid'):
        if key in body:
            return body[key]
    # some serializers return a `url` pointing to the created resource
    url = body.get('url') if isinstance(body, dict) else None
    if url:
        try:
            # take last path segment as id
            return url.rstrip('/').split('/')[-1]
        except Exception:
            return None
    return None


def test_add_and_list_users(user_service):
    unique = uuid.uuid4().hex[:6]
    payload = {
        'first_name': f'Script{unique}',
        'last_name': 'Runner',
        'dob': '1990-01-01',
        'likes_chocolate': 'L',
        'age_first_taste_chocolate': 6,
    }

    # create
    r = user_service.create_user(payload)
    assert r is not None
    assert r.status_code in (200, 201, 202), f'Create failed: {r.status_code} {r.text}'
    try:
        body = r.json()
    except Exception:
        body = {}

    user_id = _extract_id(body)
    assert user_id, f'No id found in create response: {body}'

    # list all users via the service wrapper
    l = user_service.get('')
    assert l is not None
    assert l.status_code == 200, f'List failed: {l.status_code} {l.text}'
    try:
        data = l.json()
    except Exception:
        data = None

    # print user list for debug/inspection
    print('Users list response:')
    try:
        print(json.dumps(data, indent=2))
    except Exception:
        print(l.text)

    # ensure created user appears in the list (best-effort)
    found = False
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get('first_name') == payload['first_name'] and item.get('last_name') == payload['last_name']:
                found = True
                break
    elif isinstance(data, dict):
        # some APIs return {'results': [...]}
        results = data.get('results') or data.get('data')
        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict) and item.get('first_name') == payload['first_name'] and item.get('last_name') == payload['last_name']:
                    found = True
                    break

    assert found, 'Created user not found in users list'

    # cleanup
    user_service.delete_user(user_id)
