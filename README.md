# kudo-box 

A virtual kudo box. 
- Team members can upload kudo card texts with a simple command
- Moderators can publish the cards in a slack channel, e.g. during agile rituals

The functionality is powered by two independent serverless functions.

## write-kudo

This serverless function can respond to a slack command and stores a kudo text in the kudo box.

## setup
Set up a virtual env and install the dependencies:
```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

## development
First we need some env vars;
```bash
export SLACK_SIGNING_SECRET=<Signing secret from basic information tab in api.slack.com/apps>
export SLACK_BOT_TOKEN=<Bot user oauth token from Oauth2 tab in api.slack.com/apps>
```
We can start a local database/pubsub as follows.
```bash
gcloud beta emulators datastore start &
gcloud beta emulators pubsub start &
```
Now you can run the serverless function locally with a test database.
```bash
export DATASTORE_EMULATOR_HOST=localhost:8081
export PUBSUB_EMULATOR_HOST=localhost:8432
functions-framework-python --target write_kudo --debug
```
If you want to debug locally with an actual slack request, use ngrok:
```bash
ngrok http 8080
```

The `--debug` flag allows you to attach a debugger as well,
or you can create a pycharm run configuration that executes above command, 
and launch it with debugger.

## tests
```bash
pytest
```
## deployment
