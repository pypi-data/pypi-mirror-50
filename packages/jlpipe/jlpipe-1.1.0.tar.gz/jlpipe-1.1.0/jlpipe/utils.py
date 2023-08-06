# -*- coding: utf-8 -*-
import json
import click
import sys
import os
from .base import StreamCommand, JsonStreamCommand
import gzip
import base64




class convert_dynamojson_cmd(JsonStreamCommand):
    """convert json from dynamodb format to normal"""
    options = [
        click.option("-c", "--csv", is_flag=True),
        click.option("-t", "--tsv", is_flag=True),
        click.option("-d", "--delimiter"),
        click.option("-f", "--fields")
    ]

    def prepare(self, csv, tsv, **kwargs):
        if csv:
            self.prepare_csv(**kwargs)
        elif tsv:
            kwargs["delimiter"] = "\t"
            self.prepare_csv(**kwargs)
        else:
            self.prepare_json()

    def prepare_json(self):
        self.process = self.json_process

    def csv_write(self, obj):
        self.writer.writerow(obj)

    def prepare_csv(self, fields, delimiter):
        kwargs = {}
        if delimiter:
            kwargs["delimiter"] = delimiter
        self.csv_kwargs = kwargs
        self.write = self.csv_write
        if fields:
            self.fields = fields.split(",")
            self._init_csv_writer()
            self.process = self.csv_process
        else:
            def first_process(obj):
                self.fields = list(self._convert_dynamojson(obj).keys())
                self._init_csv_writer()
                self.process = self.csv_process
                return self.csv_process(obj)
            self.process = first_process

    def _init_csv_writer(self):
        import csv
        self.writer = csv.DictWriter(self.outfile, self.fields, **self.csv_kwargs)
        self.writer.writeheader()
        return self

    def _convert_sints_to_str(self, sints):
        # sample:  "31,-117,8,0,0,0,0,0,0,0,13,"
        items = [int(item) for item in sints.split(",") if item]
        items = [i < 0 and 256 + i or i for i in items]
        return gzip.decompress(bytes(items)).decode()

    def _convert_dynamojson(self, item):
        if isinstance(item, list):
            return [self._convert_dynamojson(item_) for item_ in item]
        if isinstance(item, dict):
            if len(item) == 1 and "item" in item:
                item = item["item"]
            if len(item) == 1 and "dynamodb" in item:
                item = item["dynamodb"]
            if len(item) == 1:
                for k, v in item.items():
                    if k.lower() == "b":
                        return self._convert_sints_to_str(v)
                    if k.lower() == "bs":
                        return [self._convert_sints_to_str(vi) for vi in v]
                    if k.lower() in {"n", "bool", "null", "m", "l", "ss", "ns", "s"}:
                        return self._convert_dynamojson(v)
                    return {k: self._convert_dynamojson(v)}
            return {k: self._convert_dynamojson(v) for k, v in item.items()}
        return item

    def csv_process(self, obj):
        obj = self._convert_dynamojson(obj)
        res = {}
        for k in self.fields:
            v = obj[k]
            if isinstance(v, (list, tuple, dict)):
                res[k] = json.dumps(v, ensure_ascii=False)
            else:
                res[k] = v
        return res

    def json_process(self, obj):
        return json.dumps(self._convert_dynamojson(obj), ensure_ascii=False)


class json2csv(JsonStreamCommand):
    """convert json to csv"""

    options = [
        click.option("-d", "--delimiter"),
        click.argument("fields", nargs=-1),
        click.option("-n", "--no_header", is_flag=True),
    ]

    writer = None

    def prepare(self, fields, delimiter=None, no_header=False):
        kwargs = {}
        if delimiter:
            kwargs["delimiter"] = delimiter
        self.csv_kwargs = kwargs
        if fields:
            self.fields = fields
            self._init_csv_writer()
        else:
            def first_process(obj):
                self.fields = list(obj.keys())
                self._init_csv_writer()
                del self.process
                return self.process(obj)
            self.process = first_process

    def _init_csv_writer(self):
        import csv
        self.writer = csv.DictWriter(self.outfile, self.fields, **self.csv_kwargs)
        if not self.no_header:
            self.writer.writeheader()
        return self

    def process(self, obj):
        for k, v in obj.items():
            if isinstance(v, (list, tuple, dict)):
                obj[k] = json.dumps(v, ensure_ascii=False)
        return obj

    def write(self, obj):
        self.writer.writerow(obj)


class json_keys_cmd(JsonStreamCommand):
    """return json keys of each line"""

    def process(self, obj):
        return ", ".join(
            list(sorted(obj.keys()))
        )


class json_keys_total_cmd(StreamCommand):
    """show statistics of keys of json lines"""

    options = [
        # click.option("-r", "--report_fields", is_flag=True),
        click.option("-l", "--line", type=int),
        click.option("-pk"),
        click.option("-d", "--db_field", type=click.Choice(["pg","sqlite"]))
    ]

    def prepare(self, **kwargs):
        from collections import defaultdict
        # self.keys = set()
        self.kv = dict()
        self.kcount = defaultdict(lambda: 0)
        self.nullcount = defaultdict(lambda: 0)
        self.total = 0

    def compare(self, obj):
        for key, value in obj.items():
            self.kcount[key] += 1
            if value is None:
                self.nullcount[key] += 1
        more_keys = obj.keys() - self.kv
        # if not more_keys:
        #     return
        # self.keys.update(more_keys)
        for key in more_keys:
            # if value is None, then this key will exist in self.keys but not in self.kv
            value = obj[key]
            if value is not None:
                self.kv[key] = value

    def process(self, line):
        self.compare(json.loads(line))
        self.total += 1
        if self.line and self.total == self.line:
            self.stop()
        if not self.db_field:
            return line

    def get_pg_type(self, v):
        if isinstance(v, (int, float, bool, str, bytes)):
            return {
                int: "integer",
                float: "float",
                bool: "bool",
                str: "text",
                bytes: "bytea",
            }[type(v)]
        elif isinstance(v, list):
            return self.get_pg_type(v[0]) + "[]"
        elif isinstance(v, dict):
            return "jsonb"
        else:
            return type(v).__name__

    def get_sqlite_type(self, v):
        if isinstance(v, (int, float, bool, str, bytes)):
            return {
                int: "integer",
                float: "real",
                bool: "integer",
                str: "text",
                bytes: "blob",
            }[type(v)]
        elif isinstance(v, (list, dict)):
            return "json"
        else:
            raise TypeError(v, type(v), "unsupported type")

    def get_report(self):
        from pprint import pformat
        newline = "\n\t"
        return f"""
all values:
{pformat(self.kv)}
Key:
\t{newline.join(f'{k}:{count} null:{self.nullcount[k]}' for k,count in sorted(self.kcount.items(), key=lambda x:x[1], reverse=True))}
Length {len(self.kcount)}
Total {self.total}
"""

    def get_db_fields(self):
        type_getter = getattr(self, f"get_{self.db_field}_type")
        values = [
            f"{k} {type_getter(v)}{' primary key' if self.pk==k else ''}{' not null' if self.nullcount[k]==0 and self.kcount[k]==self.total else ''}"
            for k, v in self.kv.items()
        ]
        return ",".join(sorted(values))

    def get_fields(self):
        return list(sorted(self.kv.keys()))

    def final(self):
        report = self.get_db_fields() if self.db_field else self.get_report()
        sys.stderr.write(report+"\n")


class json_select_cmd(JsonStreamCommand):
    """select fields from json"""

    options = [
        click.argument("include", nargs=-1),
        # click.option("-ex", "--exclude", multiple=True),
    ]

    def parse_alias(self, path):
        if "=" in path:
            return path.split("=", 1)
        else:
            return path, path

    def parse_operator(self, path):
        from collections import defaultdict
        import re
        ops = defaultdict(list)
        raw_ops = re.findall("\[(.*?)\]", path)
        if raw_ops:
            for op in raw_ops:
                ops[op[0]].append(op[1:])
            return path[:path.index("[")], ops
        return path, None

    def prepare(self, include):
        include = set(include)
        # exclude = set(exclude)
        # assert (bool(include) + bool(exclude)) == 1, "include or exclude"
        alias_paths = [self.parse_alias(path) for path in include]
        alias_path_operators = [(alias, *self.parse_operator(path)) for alias, path in alias_paths]
        include = [(alias, path.split("__"), operators) for alias, path, operators in alias_path_operators]

        def get_from_path(obj, path):
            if path and not isinstance(obj, (list, dict)):
                raise TypeError
            if path == ["."]:
                return obj
            for i, p in enumerate(path):
                try:
                    obj = obj[p]
                except KeyError:
                    return None
                except TypeError:
                    obj = [get_from_path(o, path[i:]) for o in obj]
                    break
            return obj

        def eval_operators(obj, operators):
            if not operators:
                return obj
            obj = dict(obj)
            for op, keys in operators.items():
                if op == "-":
                    for key in keys:
                        try:
                            del obj[key]
                        except KeyError:
                            pass
                else:
                    raise NotImplementedError(op)
            return obj

        def new_obj_fun(obj):
            res = {}
            for key, path, operators in include:
                v = eval_operators(get_from_path(obj, path), operators)
                if key == ".":
                    res = v
                else:
                    res[key] = v
            # return {key:  for key, path, operators in include}
            return res
        # else:
        #     def new_obj_fun(obj):
        #         for key in exclude:
        #             try:
        #                 del obj[key]
        #             except KeyError:
        #                 continue
        #         return obj
        self.new_obj_fun = new_obj_fun

    def process(self, obj):
        return json.dumps(self.new_obj_fun(obj), ensure_ascii=False)


class decompress_full_line(StreamCommand):
    """decompress gzip + base64 text"""
    def process(self, obj):
        return gzip.decompress(base64.b64decode(obj)).decode('utf-8')


class decompress_binary_fields(JsonStreamCommand):
    """decompress gzip compressed field"""

    options = [
        # click.option("-d", "--delimiter"),
        click.argument("fields", nargs=-1)
    ]

    def _decompress(self, value):
        if value is None:
            return None
        return json.loads(gzip.decompress(base64.b64decode(value)).decode('utf-8'))

    def process(self, obj):
        for field in self.fields:
            obj[field] = self._decompress(obj.get(field))
        return json.dumps(obj, ensure_ascii=False)


class parquet2json(StreamCommand):
    """convert parquet file to json format"""

    def process(self, file_name):
        import pandas as pd
        sys.stderr.write(file_name + "\n")
        return pd.read_parquet(file_name, nthreads=4)

    _write_thread = None

    def write(self, df):
        import threading
        to_write = df.to_json(orient="records", lines=True)

        if self._write_thread:
            self._write_thread.join()

        def do_write():
            try:
                self.outfile.write(to_write)
                self.outfile.write("\n")
            except (ValueError, BrokenPipeError):
                return
        self._write_thread = threading.Thread(target=do_write)
        self._write_thread.start()

    def final(self):
        self._write_thread and self._write_thread.join()


class array_unpack(JsonStreamCommand):
    """similiar to postgres unnest, unnest a array to lines"""

    options = [
        click.argument("field", nargs=-1)
    ]

    def process(self, array):
        if self.field:
            array = array[self.field[0]]
        return "\n".join(json.dumps(item, ensure_ascii=False) for item in array)


class json_to_sqlite(StreamCommand):
    options = [
        click.argument("sqlite_path"),
        click.option("-t", "--table_name"),
        click.option("-pk", "--primary_key"),
        click.option("-n", "--not_create_table", is_flag=True),
        click.option("-b", "--buffer_lines", default=100)
    ]

    _namedpipe_path = None

    def prepare(self, table_name, sqlite_path, primary_key, not_create_table, buffer_lines):
        self._line_buffer = buffer_lines

    def process_buffer_lines(self, lines):
        # import ipdb; ipdb.set_trace()
        json_all_keys_instance = json_keys_total_cmd(db_field="sqlite", pk=self.primary_key, line=None)
        for line in lines:
            json_all_keys_instance.process(line)
        fields = json_all_keys_instance.get_db_fields()

        import sqlite3
        import tempfile
        import subprocess
        # import ipdb; ipdb.set_trace()
        if self.not_create_table:
            return
        if not self.table_name and self.infile_name is None:
            raise click.UsageError("need to specify table name with -t/--table_name")
        if not self.table_name:
            self.table_name = os.path.splitext(os.path.basename(self.infile_name))[0]
        with sqlite3.connect(self.sqlite_path) as conn:
            sql = f"CREATE TABLE {self.table_name} ({fields});"
            print(sql, file=sys.stderr, end="...")
            conn.execute(sql)
            print("done",file=sys.stderr)

        self._namedpipe_path = tempfile.mktemp(suffix=".pipe")
        os.mkfifo(self._namedpipe_path)
        subprocess.Popen(["sqlite3", "-csv", self.sqlite_path, f".import {self._namedpipe_path} {self.table_name}"])
        self._json2csv = json2csv(fields=json_all_keys_instance.get_fields(), outfile=self._namedpipe_path, no_header=True)

    def process(self, line):
        self._json2csv._process_line(line)

    def final(self):
        # self.conn.close()
        if self._namedpipe_path:
            os.remove(self._namedpipe_path)



class json2pgtext(JsonStreamCommand):
    """convert json to postgres plain text then can use pgcopy to import to database"""

    options = [
        click.argument("fields", nargs=-1),
        click.option("-a", "--list_as_array", is_flag=True)
    ]

    def prepare(self, fields, list_as_array):
        kwargs = {}
        self.csv_kwargs = kwargs
        if fields:
            self.fields = fields
            self._init_writer()
        else:
            def first_process(obj):
                self.fields = list(sorted(obj.keys()))
                self._init_writer()
                del self.process
                return self.process(obj)
            self.process = first_process

    def _init_writer(self):
        import csv
        # self.writer = csv.DictWriter(self.outfile, self.fields, **self.csv_kwargs)
        self.outfile.write(",".join(self.fields) + "\n")
        return self

    def process(self, obj):
        return "\t".join([self._process_string(self._process(obj.get(k))) for k in self.fields])

    def _process_string(self, v):
        if v is None:
            return r"\N"
        return v\
            .replace("\\", r"\\")\
            .replace("\n", r"\n")\
            .replace("\r", r"\r")\
            .replace("\t", r"\t")\
            # .replace("\b", r"\b")\
        # .replace("\f", r"\f")\
        # .replace("\v", r"\v")

    def _process(self, v):
        if v is None:
            return None
        elif isinstance(v, str):
            return v
        elif isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        elif isinstance(v, (list, tuple)):
            v = json.dumps(v, ensure_ascii=False)
            if self.list_as_array:
                v = "{%s}" % v[1:-1]
            return v
        else:
            return str(v)

    def _process_list(self, v):
        # TODO
        pass


import getpass


@click.command()
@click.argument("table")
@click.option("-H", "--host")
@click.option("-p", "--port")
@click.option("-U", "--user", default=getpass.getuser())
@click.option("-pw", "--password")
@click.option("-d", "--database", default=getpass.getuser())
@click.option("-f", "--fields")
@click.option("-s", "--sep")
def pgcopy(table, fields, sep, **kwargs):
    """similiar to pgfutter, but it use plain text to copy"""

    import psycopg2

    with psycopg2.connect(**{k: v for k, v in kwargs.items() if v}) as con:
        if not fields:
            fields = sys.stdin.readline().strip().split(sep)
        with con.cursor() as cur:
            cur.copy_from(sys.stdin, table, columns=fields, sep=sep)
            # cur.commit()


@click.command()
@click.argument("command", nargs=-1)
@click.option("-i", "--infile", type=click.Path(exists=True))
@click.option("-o", "--outfile", type=click.Path())
@click.option("-j", "--concurrency", default=10)
@click.option("-i1", "--input_first_line_broadcast", is_flag=True)
@click.option("-o1", "--output_first_line_distinct", is_flag=True)
def parallel_split(command, concurrency, infile=None, outfile=None, input_first_line_broadcast=False, output_first_line_distinct=False):
    """similiar to `parallel --pipe`, start multiple worker ahead, and cycle each line of input and route to each worker, then forword workers output to its stdout, not garentee order."""

    # TODO
    if infile:
        infile = open(infile)
    else:
        infile = sys.stdin

    if outfile:
        outfile = open(outfile, "w")
    else:
        outfile = sys.stdout

    import threading
    from queue import Queue
    import subprocess
    import itertools
    import signal
    import shlex

    # command = shlex.split(command)
    ps = [subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True) for i in range(concurrency)]

    def queue_runner():

        try:
            readline = infile.readline
            if input_first_line_broadcast:
                line = readline()
                if not line:
                    return
                for p in ps:
                    p.stdin.write(line)
            for i in itertools.cycle(range(concurrency)):
                line = readline()
                if not line:
                    break
                p = ps[i]
                p.stdin.write(line)
                # p.stdin.flush()
        finally:
            for p in ps:
                p.stdin.close()

    first_line_wrote = False
    lock = threading.Lock()

    def build_worker(p):
        def getter():
            try:
                nonlocal first_line_wrote
                write = sys.stdout.write
                if output_first_line_distinct:
                    out = p.stdout.readline()
                    if not out:
                        return
                    with lock:
                        if not first_line_wrote:
                            write(out)
                            first_line_wrote = True
                while True:
                    out = p.stdout.readline()
                    if not out:
                        break
                    write(out)
            except (ValueError, BrokenPipeError):
                p.stdout.close()
                return
        thread = threading.Thread(target=getter)
        thread.start()
        return thread

    try:
        threads = [build_worker(p) for p in ps]
        queue_runner()
        [thread.join() for thread in threads]
    finally:
        infile.close()
        outfile.close()

# class parquet2json(StreamCommand):
#     def prepare(self):
#         import csv
#         self.writer=csv.writer(self.outfile, "unix")

#     def process(self, file_name):
#         import pandas as pd
#         sys.stderr.write(file_name+"\n")
#         return pd.read_parquet(file_name, nthreads=4)

#     def write(self, df):
#         writer=self.writer.writerow
#         for row in zip(*(df[c] for c in df)):
#             writer(row

# @click.command()
# @click.option("-i", "--infile", type=click.Path(exists=True))
# @click.option("-o", "--outfile", type=click.Path())
# def json2pickle(include, exclude, infile=None, outfile=None):
#     if infile:
#         infile = open(infile)
#     else:
#         infile = sys.stdin

#     if outfile:
#         outfile = open(outfile, "wb")
#     else:
#         outfile = sys.stdout

#     try:
#         while True:
#             line = infile.readline()
#             if not line:
#                 break
#             obj = json.loads(line)
#             outfile.write(json.dumps(
#                 new_obj_fun(obj)
#             ))
#             outfile.write("\n")
#     finally:
#         infile.close()
#         outfile.close()
