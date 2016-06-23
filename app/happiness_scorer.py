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

"""Uses the Google Cloud Vision API to determine how happy a group of
Google+ users are, based on their profile photos."""

import base64

import photo_utils

VISION_RESP_TO_SCORE = {
    'VERY_UNLIKELY': 1,
    'UNLIKELY': 2,
    'POSSIBLE': 3,
    'LIKELY': 4,
    'VERY_LIKELY': 5
}


def create_img_request(img_data):
    return {
        'image': {
            'content': base64.encodestring(img_data)
        },
        'features': [{
            'type': 'FACE_DETECTION'
        }]
    }


def evaluate_users(service, users):
    imgs = [photo_utils.download_img(user.photo_url) for user in users]
    img_requests = [create_img_request(img) for img in imgs]
    service_response = _execute_vision_request(service, img_requests)

    for idx, response in enumerate(service_response['responses']):
        if response:
            users[idx].happiness_level = VISION_RESP_TO_SCORE[
                response['faceAnnotations'][0]['joyLikelihood']]

    return users


def _execute_vision_request(service, img_requests):
    request = service.images().annotate(body={
        'requests': img_requests
    })
    return request.execute()
