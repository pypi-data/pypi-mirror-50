# monsoon-backup-mysql
Add support for MySQL backups on [`monsoon`](https://github.ibm.com/apset/monsoon).

## Requirements
This plug-in is build on top of [`mysqldump`](http://dev.mysql.com/doc/refman/en/mysqldump.html),
so you will need to it installed.

`mysqldump` is part of the `mysql` client.cd .

## Installing
You can use `pip` to install this plug-in from Artifactory.

First you will need to configure your pip client by creating or editing the
`~/.pip/pip.conf` file to look like this:

```
[global]
index-url = https://pypi.python.org/simple
extra-index-url = https://<USERNAME>:<API KEY>@na.artifactory.swg-devops.com/artifactory/api/pypi/apset-pypi-local/simple
```

After that you should be able to run
```sh
$ pip install monsoon-backup-mysql
```

Alternatively, you can install it directly from GHE:
```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon-backup-mysql
```

## Using
After installing the plug-in you will be able to use the `backup mysql` command
on `monsoon`.

```sh
$ monsoon backup mysql -h
usage: monsoon backup mysql [-h] [--gzip] [-o OUTPUT]

Backup a MySQL database. It uses `mysqldump` so it's required to have it
installed and added to the system's PATH. You can use any of the arguments
supported by `mysqldump`. Use `mysqldump -h` for more information.

optional arguments:
  -h, --help            show this help message and exit
  --gzip                compress output file  (requires gzip to be installed)
  -o OUTPUT, --output OUTPUT
                        output file path
```

You can pass any option that you would normally use on `mysqldump`:

```sh
$ monsoon backup mysql --host 192.168.99.1 -u root -ppassword --port 32769 --all-databases
```

As shown in the `--help` message, there are two extra arguments you can use in
your backup process `--gzip` and `-o`.

`--gzip` will compress the output and requires the `gzip` command to be
available in your system.

`-o OUTPUT` or `--output OUTPUT` will save the output of `mysqldump` into a
file.

**Important:** There is a conflict with the `-h` argument since it is reserved
for the help/usage message. User `--host` to pass the hostname.
