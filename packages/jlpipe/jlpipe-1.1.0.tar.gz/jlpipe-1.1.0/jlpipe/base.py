# -*- coding: utf-8 -*-
import json
import click
import sys


class MetaStreamCommand(type):
    def __new__(cls, name, bases, attrs):
        attrs.setdefault("abstract", False)
        options = attrs.pop("options", [])
        cls = super().__new__(cls, name, bases, attrs)
        if options:
            cls.options = options + getattr(cls, "options", [])
        return cls
        # if cls.abstract:
        #     return cls

        # obj = cls()
        # for option in reversed(cls.options):
        #     option(obj)
        # # import ipdb; ipdb.set_trace()
        # return click.command(name=cls.__name__)(obj)


class StopStream(Exception):
    pass


class StreamCommand(metaclass=MetaStreamCommand):
    abstract = True
    _line_buffer = None

    options = [
        click.option("-i", "--infile", type=click.Path(exists=True)),
        click.option("-o", "--outfile", type=click.Path())
    ]
    def __new__(cls, **kwargs):
        obj = super().__new__(cls)
        if kwargs:
            obj.prepare_base(**kwargs)
            return obj
        else:
            for option in reversed(cls.options):
                option(obj)
            click.command(name=cls.__name__)(obj)()
    #     # import ipdb; ipdb.set_trace()
    #     return obj()

    def __call__(self, **kwargs):

        self.prepare_base(**kwargs)

        if self._line_buffer:
            self._buffer_lines = list(filter(None, (self.infile.readline() for i in range(self._line_buffer))))
            self.process_buffer_lines(self._buffer_lines)

        try:
            for line in self._get_new_line():
                self._process_line(line)
        except StopStream:
            pass
        finally:
            self.final()
            self.infile.close()
            self.outfile.close()

    def _get_new_line(self):
        if self._line_buffer:
            for line in self._buffer_lines:
                yield line
        for line in self.infile:
            yield line

    def _process_line(self, line):
        obj = self.preprocess(line)
        obj = self.process(obj)
        obj is not None and self.write(obj)

    def process_buffer_lines(self, lines):
        pass

    def write(self, obj):
        self.outfile.write(obj)
        self.outfile.write("\n")

    def prepare_base(self, infile=None, outfile=None, **kwargs):
        if infile:
            self.infile_name = infile
            self.infile = open(infile)
        else:
            self.infile_name = None
            self.infile = sys.stdin

        if outfile:
            self.outfile_name = outfile
            self.outfile = open(outfile, "w")
        else:
            self.outfile_name = None
            self.outfile = sys.stdout

        self.__dict__.update(kwargs)
        self.prepare(**kwargs)

    def prepare(self, **kwargs):
        pass

    def preprocess(self, line):
        return line.strip()

    def process(self, obj):
        return obj

    def final(self):
        pass

    def stop(self):
        raise StopStream


class JsonStreamCommand(StreamCommand):
    abstract = True

    def preprocess(self, line):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            sys.stderr.write("line: %s" % json.dumps(line, ensure_ascii=False))
            raise
