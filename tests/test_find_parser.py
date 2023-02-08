import pytest
from typing import List

from seeksubdirectories.find_parser import parse_find_output, Directory


def test_find_parser_requires_input():
    with pytest.raises(ValueError):
        parse_find_output(None, '/')
    with pytest.raises(ValueError):
        parse_find_output([], '/')
    with pytest.raises(ValueError):
        parse_find_output(['.'], None)


def test_find_parser_returns_simple_directory():
    assert parse_find_output(['.'], '/') == Directory(fullpath='./', name='.', directories=[])


def test_find_parser_returns_directory_with_a_single_filename_inside():
    assert parse_find_output(['.', './f01'], '/') == \
           Directory(fullpath='.', name='.', directories=[Directory(fullpath='./f01', name='f01', directories=[])])


def test_find_parser_ignore_trailing_separator():
    assert parse_find_output(['./'], '/') == Directory(fullpath='./', name='.', directories=[])
    assert parse_find_output(['./', './f01'], '/') == \
           Directory(fullpath='./', name='.', directories=[Directory(fullpath='./f01', name='f01', directories=[])])


@pytest.mark.parametrize('input_,expected', [
    [['./', './c', './cd', './aaa', './aaa/bc'], Directory(fullpath='.', name='.', directories=[
        Directory(fullpath='./c', name='c', directories=[]), Directory(fullpath='./cd', name='cd', directories=[]),
        Directory(fullpath='./aaa', name='aaa', directories=[Directory(fullpath='./aaa/bc', name='bc', directories=[])])
    ])],
    [['/tmp/a', '/tmp/a/c', '/tmp/a/cd', '/tmp/a/aaa', '/tmp/a/aaa/bc'],
     Directory(fullpath='/tmp', name='tmp', directories=[Directory(fullpath='/tmp/a', name='a', directories=[
         Directory(fullpath='/tmp/a/c', name='c', directories=[]),
         Directory(fullpath='/tmp/a/cd', name='cd', directories=[]),
         Directory(fullpath='/tmp/a/aaa', name='aaa',
                   directories=[Directory(fullpath='/tmp/a/aaa/bc', name='bc', directories=[])])
     ])])],
])
def test_find_parser(input_: List[str], expected: Directory):
    assert parse_find_output(input_, '/') == expected
