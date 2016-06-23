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

from mock import patch

import photo_utils


def test_set_photo_size_using_default_size():
    url = 'https://lh3.googleusercontent.com/photo.jpg?sz=2'
    mod_url = photo_utils.set_photo_size(url)

    expected_url = 'https://lh3.googleusercontent.com/photo.jpg?sz=250'
    assert mod_url == expected_url


def test_set_photo_size_with_missing_input_size():
    url = 'https://lh3.googleusercontent.com/photo.jpg'
    mod_url = photo_utils.set_photo_size(url, 75)

    expected_url = 'https://lh3.googleusercontent.com/photo.jpg?sz=75'
    assert mod_url == expected_url


def test_set_photo_size_with_multiple_input_sizes():
    url = 'https://lh3.googleusercontent.com/photo.jpg?sz=2&sz=589'
    mod_url = photo_utils.set_photo_size(url, 75)

    expected_url = 'https://lh3.googleusercontent.com/photo.jpg?sz=75'
    assert mod_url == expected_url


def test_set_photo_size_with_relative_url():
    url = '/photo.jpg?sz=2'
    mod_url = photo_utils.set_photo_size(url, 75)

    expected_url = '/photo.jpg?sz=75'
    assert mod_url == expected_url


def test_set_photo_size_with_empty():
    mod_url = photo_utils.set_photo_size('', 75)
    assert mod_url == '?sz=75'


@patch.object(photo_utils, 'httplib2')
def test_download_img(mock_httplib2):
    mock_httplib2.Http.return_value.request.return_value = ('foo', 'bar')
    url = 'http://example.com/some_url.jpg'
    photo_utils.download_img(url)

    name, args, kwargs = mock_httplib2.mock_calls[1]
    assert name.endswith('request')
    assert len(args) == 2
    assert args == (url, 'GET')
