tasklog: a terminal based application to submit work/task logs to JIRA issues, to Slack channels

Compatible with Python versions
====================

- Python 3.7.3+

Basic Setup
===========

Install for all users, from Pypi

```
sudo bash make.sh --install-package-globally-from-source
tasklog -h
```

Install + run app (for development):

```
source make.sh --enable-development-env
bash make.sh --install-dependencies
bash make.sh --install-package-in-development-mode
bash make.sh --show-tasklog-options
````

Install for all users, from source

```
sudo bash make.sh --install-package-globally-from-source
tasklog -h
```

Setup/Run the application:

```
bash make.sh --show-tasklog-options
OR
bash make.sh --show-tasklog-submit-worklog-cli-sample
bash make.sh --show-tasklog-submit-daily-cli-sample
```

Run the test suite:

_Requirement: App is installed for development purpose_

```
bash make.sh --install-test-dependencies
bash make.sh --run-tests
```
