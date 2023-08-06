# backwork-notifier-sentry [![Build Status](https://travis-ci.org/IBM/backwork-notifier-sentry.svg?branch=master)] [![PyPI version](https://badge.fury.io/py/backwork-notifier-sentry.svg)](https://badge.fury.io/py/backwork-notifier-sentry)(https://travis-ci.org/IBM/backwork-notifier-sentry)
Add support for [Sentry](https://sentry.io) notifications on [`backwork`](https://github.com/IBM/backwork).

## Installing
You can use `pip` to install this plug-in directly from GHE:
```sh
$ pip install backwork-notifier-sentry
```

## Using
After installing the plug-in you will be able to use the `-n sentry`
argument on `backwork` commands.

```sh
$ backwork --help
usage: backwork [-h] [-n NOTIFIERS] [--sentry-dsn SENTRY_DSN]
               {backup,upload} ...

positional arguments:
  {backup,upload}

optional arguments:
  -h, --help            show this help message and exit
  -n NOTIFIERS, --notify NOTIFIERS
                        enable a notifier, it can be used multiple times
  --sentry-dsn SENTRY_DSN
                        Sentry DSN to be used for notifications. It can also
                        be set with the evironment variable $SENTRY_DSN.
```
