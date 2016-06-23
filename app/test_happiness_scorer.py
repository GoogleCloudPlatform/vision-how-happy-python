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

import base64

import pytest
from mock import MagicMock, patch

import happiness_scorer
from happiness_scorer import photo_utils
from user_getter import User


@pytest.fixture
def service():
    return MagicMock()


def execute_evaluate_users(
        service, mock_dl_img, mock_create_img_request, mock_execute,
        service_response):
    __tracebackhide__ = True

    users = [User(123, 'Phil', 'http://example.com/some_url.jpg')]
    img_data = 'some image data'
    img_request = {'foo': 'bar'}

    mock_dl_img.return_value = img_data
    mock_create_img_request.return_value = img_request
    mock_execute.return_value = service_response

    happiness_scorer.evaluate_users(service, users)

    return users, img_data, img_request


@patch.object(happiness_scorer, '_execute_vision_request')
@patch.object(happiness_scorer, 'create_img_request')
@patch.object(photo_utils, 'download_img')
def test_evaluate_users_no_vision_response(
        mock_dl_img, mock_create_img_request, mock_execute, service):

    users, img_data, img_request = execute_evaluate_users(
        service, mock_dl_img, mock_create_img_request, mock_execute,
        {'responses': []})

    mock_dl_img.assert_called_once_with(users[0].photo_url)
    mock_create_img_request.assert_called_once_with(img_data)
    print [service, img_request]
    print mock_execute.call_args_list
    mock_execute.assert_called_once_with(service, [img_request])
    assert users[0].happiness_level is None


@patch.object(happiness_scorer, '_execute_vision_request')
@patch.object(happiness_scorer, 'create_img_request')
@patch.object(photo_utils, 'download_img')
def test_evaluate_users_with_vision_response(
        mock_dl_img, mock_create_img_request, mock_execute, service):

    service_response = {
        'responses': [{
            'faceAnnotations': [{
                'joyLikelihood': 'LIKELY'
            }]
        }]
    }

    users, img_data, img_request = execute_evaluate_users(
        service, mock_dl_img, mock_create_img_request, mock_execute,
        service_response)

    mock_dl_img.assert_called_once_with(users[0].photo_url)
    mock_create_img_request.assert_called_once_with(img_data)
    mock_execute.assert_called_once_with(service, [img_request])
    assert users[0].happiness_level == 4


def test_create_img_request():
    data = 'fdjskalf;feiupo!#$'
    b64_data = base64.encodestring(data)

    expected_response = {
        'image': {
            'content': b64_data
        },
        'features': [{
            'type': 'FACE_DETECTION'
        }]
    }
    assert happiness_scorer.create_img_request(data) == expected_response


def test_execute_vision_request(service):
    img_requests = ['foo', 'bar', 'baz']
    happiness_scorer._execute_vision_request(service, img_requests)

    assert len(service.mock_calls) == 3

    name, args, kwargs = service.mock_calls[0]
    assert name == 'images'
    assert len(args) == 0
    assert len(kwargs) == 0

    name, args, kwargs = service.mock_calls[1]
    assert name.endswith('annotate')
    assert len(args) == 0
    assert len(kwargs) == 1
    expected_annotate_call = {'requests': img_requests}
    assert kwargs['body'] == expected_annotate_call

    name, args, kwargs = service.mock_calls[2]
    assert name.endswith('execute')
    assert len(args) == 0
    assert len(kwargs) == 0
