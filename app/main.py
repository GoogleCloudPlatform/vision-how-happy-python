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

"""Response handler for a GAE page. Accesses the current user's profile to
obtain their and their friends' profile photos, determines how happy the
photos seem, then displays everything to the user."""

import os

import jinja2
import webapp2
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets

import happiness_scorer
import user_getter

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

decorator = OAuth2DecoratorFromClientSecrets(
    os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
    'https://www.googleapis.com/auth/plus.login')


class MainHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        g_plus_service = get_g_plus_service()
        vision_service = get_vision_service()

        user = user_getter.get_individual(g_plus_service)
        happiness_scorer.evaluate_users(vision_service, [user])

        friends = user_getter.get_friends(g_plus_service)
        happiness_scorer.evaluate_users(vision_service, friends)
        scored_friends = [f for f in friends if f.happiness_level]
        avg_friend_happiness = sum(f.happiness_level for f in scored_friends) \
            / float(len(scored_friends))

        template_vals = {
            'user': user,
            'friends': friends,
            'user_score': user.happiness_level,
            'avg_friend_happiness': avg_friend_happiness
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_vals))


def get_vision_service():
    default_creds = GoogleCredentials.get_application_default()
    return build('vision', 'v1', credentials=default_creds)


def get_g_plus_service():
    return build('plus', 'v1', http=decorator.http())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
