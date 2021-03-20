from findzen.indexer import index_builder
from findzen.models.user import User, Users
import dictdiffer

def test_index_builder(sample_users):
    expected_user_index ={
        'user_index_by_id' : {"1" : sample_users[0].dict(), "2" : sample_users[1].dict()},
        'user_index_by_url': {"url.com": [1, 2]},
        'user_index_by_external_id': {"100": [1], "200": [2]},
        'user_index_by_name': {"John Doe": [1], "Jane Doe": [2]},
        'user_index_by_alias': {"Johnny": [1], "None": [2]},
        'user_index_by_created_at': {"2016-06-23T10:31:39 -10:00": [1], "2017-06-23T10:31:39 -10:00": [2]},
        'user_index_by_active': {"True": [1], "False": [2]},
        'user_index_by_verified': {"True": [1], "None": [2]},
        'user_index_by_shared': {"False": [1, 2]},
        'user_index_by_locale': {"zh-CN": [1], "None": [2]},
        'user_index_by_timezone': {"Armenia": [1], "None": [2]},
        'user_index_by_last_login_at': {"2012-04-12T04:03:28 -10:00": [1], "2015-04-12T04:03:28 -10:00": [2]},
        'user_index_by_email': {"john@url.com": [1], "None": [2]},
        'user_index_by_phone': {"9575-552-585": [1], "9675-552-585": [2]},
        'user_index_by_signature': {"Fake": [1], "StillFake": [2]},
        'user_index_by_organization_id': {"101": [1], "None": [2]},
        'user_index_by_tags': {"tag1": [1, 2], "tag2": [1], "tag22": [2]},
        'user_index_by_suspended': {"False": [1], "True": [2]},
        'user_index_by_role': {"admin": [1], "role": [2]},
    }


    users = Users.parse_obj(sample_users)
    actual_users_index = index_builder(users, User)
    
    assert len(list(dictdiffer.diff(expected_user_index, actual_users_index))) == 0


