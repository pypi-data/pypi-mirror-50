# jlpipe

## Introduction
Project owner: Jay Young <dev@yjmade.net>

## Installation

```bash
pip install jlpipe
```

## Usage
full commands list:

* dynamojson: convert json from dynamodb format to normal
* jsonkey: return json keys of each line
* jsonallkeys: show statistics of keys of json lines
* jsonselect: select fields from json
* json2csv: convert json to csv
* json2pgtext: convert json to postgres plain text then can use pgcopy to import to database
* parquet2json: convert parquet file to json format
* jsondecompress: decompress gzip compressed field
* arrayunpack: similiar to postgres unnest, unnest a array to lines
* pgcopy: similiar to pgfutter, but it use plain text to copy
* parallel_split: similiar to `parallel --pipe`, start multiple worker ahead, and cycle each line of input and route to each worker, then forword workers output to its stdout, not garentee order.



```bash
$ cat *.json|parallel_split dynamojson|jsonselect data=. patent_id description=patent_description|jsondecompress description|json2pgtext -a|pgcopg all_patent

$ cat *.json|jsonallkeys -l 10000 -r >/dev/null
$ ls *.parquet|parquet2json|json2pgtext|pgcopg all_patent
```

More usage reference to the command help text

```bash
command --help
```