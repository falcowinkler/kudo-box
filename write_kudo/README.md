# write-kudo

This serverless function can respond to a slack command and stores a kudo text in the kudo box.

## development
We can start a local database as follows.
```bash
gcloud alpha emulators datastore start
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
