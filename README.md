# Kudobox

A virtual kudo box

- Team members can upload kudo card texts with a simple command
- Moderators can publish the cards in a slack channel, e.g. during agile rituals

### Requirements
- Python 3 and the packages in `requirements.txt`

### Setup
- Create an app in slack using the manifest.yml
### Configuration
- Add all secrets as env variables:
    - `SLACK_SIGNING_SECRET` from https://api.slack.com/apps/your-app-id/general
    - `SLACK_BOT_TOKEN` From https://api.slack.com/apps/your-app-id/oauth
    - `SERVICEACCOUNT_PRIVATE_KEY` From https://console.firebase.google.com/u/0/project/kudo-box/settings/serviceaccounts/adminsdk, previous step
    - `SECRET_KEY` for flask (can be anything as long as it's secret)
  
### Deploying via git
You should never have to modify files except your configuration file.

```bash
git remote add upstream git@github.com:falcowinkler/kudo-box.git
git merge upstream/master
heroku login
git push heroku master
```

### Run locally
Docker compose:
```bash
ngrok http 5000 &
docker-compose up
```

With flask app seperately:
```bash
docker run --name kudo-box-postgres -e SLACK_SIGNING_SECRET=your-signing-secret \
           --env-file dev-database.env -p 5432:5432 -d postgres
```

Copy the ngrok http url (e.g. `https://1234abcd.ngrok.io`) and enter it as `Request url`
at `https://api.slack.com/apps/<your-slack-app>/event-subscriptions`.

### deploy
```shell script
heroku container:login
heroku container:push web --app=kudo-box-otto
heroku container:release web --app=kudo-box-otto
```