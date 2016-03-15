## TIFF Surgeon
Python3 code to read and correct TIFF tags. Currently only works on non-offset tag values in one-page TIFFs.

## Global Functions
_read_tiff_file(filename):_

Returns the bytestream of a TIFF file at filename

## Classes
_Tiff(filename, destroy = boolean):_
Consumes a TIFF bytestream and creates a TIFF instance with the attributes:
* byte_stream: bytestream of the TIFF, destroy = True sets this value to None
* endian: big or little
* tag_offset: byte offset to the first IFD
* tag_count: number of tags in the first IFD
* tags: a dictionary of tags in the first IFD

The Tiff class has two main methods

_set_tag_value(self, tag, value):_

Changes the byte value of a non-offset tag. This requires Tiff.byte_stream != None. Expects the new value to be formatted as a byte string, e.g. b'\x00\x00\x00\x00' Also resets the Tiff.tags attributes with the new tag value.

_write_tiff(self, filename):_

Writes Tiff.byte_stream as a file with the specified filename.
