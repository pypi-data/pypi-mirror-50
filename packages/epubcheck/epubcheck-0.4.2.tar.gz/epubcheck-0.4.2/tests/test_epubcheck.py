# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import epubcheck
from epubcheck import samples
from epubcheck.cli import main


def test_valid():
    assert epubcheck.validate(samples.EPUB3_VALID)


def test_invalid():
    assert not epubcheck.validate(samples.EPUB3_INVALID)


def test_main_valid(capsys):
    argv = [samples.EPUB3_VALID]
    exit_code = main(argv)
    out, err = capsys.readouterr()
    assert 'ERROR' not in out and 'ERROR' not in err
    assert exit_code == 0


def test_main_invalid(capsys):
    argv = [samples.EPUB3_INVALID]
    exit_code = main(argv)
    out, err = capsys.readouterr()
    assert 'ERROR' in err and 'WARNING' in out
    assert exit_code == 1
