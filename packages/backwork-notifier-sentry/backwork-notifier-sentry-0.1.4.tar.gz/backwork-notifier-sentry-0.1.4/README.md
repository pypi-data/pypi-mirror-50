# monsoon-notifier-sentry
Add support for [Sentry](https://sentry.io) notifications on [`monsoon`](https://github.ibm.com/apset/monsoon).

## Installing
You can use `pip` to install this plug-in directly from GHE:
```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon-notifier-sentry
```

## Using
After installing the plug-in you will be able to use the `-n sentry` 
argument on `monsoon` commands.

```sh
$ monsoon --help
usage: monsoon [-h] [-n NOTIFIERS] [--sentry-dsn SENTRY_DSN]
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
