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

"""Uses the G+ API to obtain information about the current user and their
connections."""

import photo_utils


class User:
    def __init__(self, uid, name='', photo_url='', happiness_level=None):
        self.uid = uid
        self.name = name
        self.photo_url = photo_url
        self.happiness_level = happiness_level


def get_individual(service, user='me'):
    google_request = service.people().get(userId=user)
    result = google_request.execute()
    return User(
        result['id'],
        result['displayName'],
        photo_utils.set_photo_size(result['image']['url']))


def get_friends(service, user='me'):
    google_request = service.people().list(userId=user, collection='visible')
    response = google_request.execute()
    return [
        User(
            r['id'],
            r['displayName'],
            photo_utils.set_photo_size(r['image']['url']))
        for r in response['items']]
