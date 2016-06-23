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

"""Simple utilities for manipulating photo data"""

import urllib
import urlparse

import httplib2


def set_photo_size(url, size=250):
    """Given a link to a G+ photo, reset the size query parameter to the value
    specified."""
    parsed_url = urlparse.urlparse(url)
    query_params = dict(urlparse.parse_qs(parsed_url.query))
    query_params['sz'] = size
    new_query_string = urllib.urlencode(query_params)
    return urlparse.urlunparse(
        parsed_url[:4] + (new_query_string,) + parsed_url[5:])


def download_img(img_url):
    response, body = httplib2.Http().request(img_url, 'GET')
    return body
