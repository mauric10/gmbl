# -*- coding: utf-8 -*-
"""
"""

import sys
import json

TEST_DATA_PATH = 'tests/test_data.json'
VERIFIED_OUTPUT_PATH = 'tests/test_data_verified.json'


def test_decode_str():
    """Test string reversal."""
    assert custom_decoder('string') == 'gnirts'


def test_decode_bool_true():
    """Test boolean pass-through."""
    assert custom_decoder(True)


def test_decode_bool_false():
    """Test boolean pass-through."""
    assert not custom_decoder(False)


def test_decode_int():
    """Test doubling of integers."""
    assert custom_decoder(2) == 4


def test_decode_float():
    """Test float pass-through."""
    assert custom_decoder(1.1) == 1.1


def test_decode_dict():
    """Test doubling and reversal on dictionary."""
    assert custom_decoder({'id': 1, 'foo': 'bar'}) == {'id': 2, 'foo': 'rab'}


def test_decode_flat_list_of_strs():
    """Test string reversal on flat list of strings."""
    assert custom_decoder(['foo', 'bar']) == ['oof', 'rab']


def test_decode_flat_list_of_ints():
    """Test string doubling on flat list of integers."""
    assert custom_decoder([1, 2]) == [2, 4]


def test_transform():
    """
    Test that transformed JSON matches desired output.
    """

    # read test data file
    with open(TEST_DATA_PATH) as f:
        input_data = f.read()

    # transform data
    transformed_json = transform(input_data)

    # get desired output format
    with open(VERIFIED_OUTPUT_PATH) as f:
        verified_output = json.loads(f.read())

    # verify
    assert transformed_json == verified_output


def custom_decoder(element):
    """
    JSON decoder with custom handling for objects.
    - Flip string objects.
    - Double integers.
    """
    if isinstance(element, str):
        return element[::-1]
    elif isinstance(element, bool):
        return element
    elif isinstance(element, int):
        return element * 2
    elif isinstance(element, dict):
        return {k: custom_decoder(v) for k, v in element.items()}
    elif (isinstance(element, list) and
          len(element) > 0 and
          isinstance(element[0], str)):
        return [custom_decoder(i) for i in element]
    else:
        return element


def transform(input_data):
    """
    Transform file contents and save as separate files.
    """

    print('Transforming data...')

    data = json.loads(input_data, object_hook=custom_decoder)

    return data


def save_files(data, filename_prefix):
    """
    Save one file per JSON object.
    """

    print('Writing to files...')

    for i, obj in enumerate(data):

        filename = f'{filename_prefix}_{i}.json'

        with open(filename, 'w') as f:
            f.write(json.dumps(obj, indent=2))

        print(f'Saved file: {filename}.')


if __name__ == "__main__":

    input_filename = sys.argv[1]
    output_file_prefix = sys.argv[2]

    # open file `generated.json`
    with open(input_filename) as f:
        input_data = f.read()

    # transform data
    output_data = transform(input_data)

    # save JSON objects into separate files
    save_files(output_data, output_file_prefix)
