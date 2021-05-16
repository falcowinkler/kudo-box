# Kudobox

A virtual kudo box

- Team members can upload kudo card texts with a simple command
- Moderators can publish the cards in a slack channel, e.g. during agile rituals

### Requirements
- Python 3 and the packages in `requirements.txt`

### Setup
- Create a project in firebase
- Create an app in slack, turn on event subscriptions and specify
`https://your-host.com/slack/events` as callback url.
### Configuration

Because the app uses firebase for storing data / authentication, and slack for sending the cards,
there is a lot of configuration necessary. This configuration needs to be specified as
a json file, and wired to the app by setting `CONFIG_FILE` to the filename
(check the example file `example-config.json` if you are unsure about the format).

- `Firebase app ids and API key`: You find this data by visiting the overview of your 
firebase app, e.g: https://console.firebase.google.com/project/kudo-box-barracuda/overview.
Click on the "Web" button under the headline "Add firebase to your project". Specify 
an app name, and copy the `firebaseConfig` into config.json. 
- `Firebase serviceaccount credentials`: Go to e.g. https://console.firebase.google.com/u/0/project/my-firebase-project/settings/serviceaccounts/adminsdk. 
Click on "Generate new private key". Copy it's contents to `config.json` under the key `firebaseServiceaccount`.
- IMPORTANT: delete the firebase private key from the config file, and keep it somewhere safe. Never commit it to git.
- Add all secrets as env variables:
    - `SLACK_SIGNING_SECRET` from https://api.slack.com/apps/your-app-id/general
    - `SLACK_BOT_TOKEN` From https://api.slack.com/apps/your-app-id/oauth
    - `SERVICEACCOUNT_PRIVATE_KEY` From https://console.firebase.google.com/u/0/project/kudo-box/settings/serviceaccounts/adminsdk, previous step
    - `SECRET_KEY` for flask (can be anything as long as it's secret)

### Updating from git
You should never have to modify files except your configuration file.

```bash
git remote add upstream git@github.com:falcowinkler/kudo-box.git
git merge upstream/master
heroku login
git push heroku master
```

### Run locally

```bash
ngrok http 5000 &
flask run
```

Copy the ngrok http url (e.g. `https://1234abcd.ngrok.io`) and enter it as `Request url`
at `https://api.slack.com/apps/<your-slack-app>/event-subscriptions`.

### deploy
```shell script
heroku container:login
heroku container:push web --app=kudo-box-otto
heroku container:release web --app=kudo-box-otto
```

### Roadmap
- Encrypt kudos using the team id. Along with request verification, it should ensure that only a certain team can read the kudos.
- Use Postgres instead of firebase, for easier dev setup and no vendor lock in.
