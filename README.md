## How Happy

How Happy is a sample application demonstrating usage of Google App Engine, Google Cloud Vision, and the Google+ API.
It accesses the current user's and the user's friends' Google+ profile photos, then uses Cloud Vision to analyze how
happy people in the photos are.

See our other [Google Cloud Platform github repos](https://github.com/GoogleCloudPlatform) for sample applications
and scaffolding for other frameworks and use cases.

## Run Locally
1. Clone this repo.

   ```
   git clone https://github.com/GoogleCloudPlatform/how-happy.git
   ```

1. Use the [Cloud Developer Console](https://console.developer.google.com) to create a project/app id. (App id and
project id are identical)

1. Enable the Cloud Vision and Google+ APIs through the Cloud Developer Console API Manager at
https://console.cloud.google.com/apis/library?project=your-app-id

1. Create OAuth2.0 credentials for your application to use when contacting the Google+ API at
https://console.cloud.google.com/apis/credentials?project=your-app-id . Include the following "Authorized redirect
URIs":

    ```
    http://localhost:8080/oauth2callback
    http://your-app-id.appspot.com/oauth2callback
    ```

Once created, download the JSON credentials into how-happy/app/client_secrets.json

1. Install and setup the [Google Cloud SDK](https://cloud.google.com/sdk/).

1. Run this project locally from the command line.

   ```
   dev_appserver.py how-happy/
   ```

1. Visit the application at [http://localhost:8080](http://localhost:8080).

## Deploying

1. Use gcloud to deploy your app.

   ```
   gcloud app deploy how-happy/app.yaml
   ```

1. Congratulations!  Your application is now live at your-app-id.appspot.com

## Contributing changes

* See [CONTRIBUTING.md](CONTRIBUTING.md)

## Licensing

* See [LICENSE](LICENSE)
