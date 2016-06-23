# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from mock import MagicMock

import photo_utils
import user_getter


@pytest.fixture
def service():
    return MagicMock()


def test_get_individual(service):
    service_response = {
        'id': 'foob@r00!',
        'displayName': 'Ray Charles',
        'image': {'url': '/'}
    }
    service.people.return_value.get.return_value.execute. \
        return_value = service_response

    individual = user_getter.get_individual(service)

    assert_user_equals_mock(individual, service_response)


def test_get_friends(service):
    friends_mock = [
        {'id': 'foob@r00!1',
         'displayName': 'Ray Charles',
         'image': {'url': '/'}},
        {'id': 'foob@r00!2',
         'displayName': 'Mr Googleys',
         'image': {'url': '/'}}]
    service_response = {'items': friends_mock}
    service.people.return_value.list.return_value.execute. \
        return_value = service_response

    friends = user_getter.get_friends(service)

    assert len(friends) == 2
    for friend, mock_friend in zip(friends, friends_mock):
        assert_user_equals_mock(friend, mock_friend)


def assert_user_equals_mock(user, mock_user):
    __tracebackhide__ = True

    assert user.uid == mock_user['id']
    assert user.name == mock_user['displayName']
    assert user.photo_url == photo_utils.set_photo_size(
        mock_user['image']['url'])
