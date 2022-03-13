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
We can start a local database as follows.
```bash
gcloud beta emulators datastore start
```
Now you can run the serverless function locally with a test database.
```bash
export DATASTORE_EMULATOR_HOST=localhost:8081
functions-framework-python --target write_kudo --debug
```
The `--debug` flag allows you to attach a debugger as well,
or you can create a pycharm run configuration that executes above command, 
and launch it with debugger.

## tests
```bash
pytest
```
## deployment
