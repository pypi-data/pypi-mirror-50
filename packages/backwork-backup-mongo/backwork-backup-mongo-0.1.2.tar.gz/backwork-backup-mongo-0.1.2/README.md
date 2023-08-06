# monsoon-backup-mongo
Add support for MongoDB backups on [`monsoon`](https://github.ibm.com/apset/monsoon).

## Requirements
This plug-in is build on top of [`mongodump`](https://docs.mongodb.com/manual/reference/program/mongodump/#bin.mongodump),
so you will need to have [`mongo-tools`](https://github.com/mongodb/mongo-tools)
installed. 

If you already have the `mongod` server or `mongo` client installed then you 
should have `mongodump`. If not, you can install them using the 
[official packages](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#packages)
or build from [source](https://github.com/mongodb/mongo-tools).

## Installing
You can use `pip` to install this plug-in directly from GHE:
```sh
$ pip install git+ssh://git@github.ibm.com/apset/monsoon-backup-mongo
```

## Using
After installing the plug-in you will be able to use the `backup mongo` command
on `monsoon`.

```sh
$ monsoon backup mongo --help
usage: monsoon backup mongo [-h]

Backup a MongoDB database. It uses `mongodump` so it's required to have it
installed and added to the system's PATH. You can use any of the arguments
supported by `mongodump`. Use `mongodump -h` for more information.

optional arguments:
  -h, --help  show this help message and exit
```

```sh
$ monsoon backup mongo
2017-01-17 01:26:27,420 mongo.mongo INFO    starting mongo backup...
2017-01-17 01:26:27,421 mongo.mongo INFO    saving file to /dumps/mongo_backup_20170117-012627.archive.gz
2017-01-17 01:26:27,483 mongo.mongo INFO    output:

	2017-01-17T01:26:27.479-0500	writing app.products to archive '/dumps/mongo_backup_20170117-012627.archive.gz'
	2017-01-17T01:26:27.480-0500	done dumping app.products (1 document)

2017-01-17 01:26:27,483 mongo.mongo INFO    backup complete
```

You can pass any option that you would normally use on `mongodump`:

```sh
$ monsoon backup mongo --user=user --password=pass --host=mongo
```

The only exception is `-h` which is reserved for the help/usage message, so the
host needs to be passed as `--host`.
