def read_tiff_file(filename):
  # Returns

  try:
    with open(filename, 'rb') as f:
      tiff_bytes = bytearray(f.read())
      return(tiff_bytes)
  except:
    print("Not a valid filename")

class Tiff(object):
  def __init__(self, byte_stream, destroy = False):
    try:
      if isinstance(byte_stream, bytearray):
        self.tiff_bytes = bytearray(byte_stream)
    except:
      print("Expected value type to be bytearray, open file with \
            'b' option")
    else:
      self.endian = self.set_endianness()
      self.tag_offset = self.set_tag_offset()
      self.tag_count = self.set_tag_count()
      self.tags = self.set_tags()
      if destroy == True:
        self.tiff_bytes = None

  def set_endianness(self):
    endian_byte = self.tiff_bytes[0]
    try:
      if endian_byte == 73:
        return('little')
      elif endian_byte == 77:
        return('big')
      else:
        raise Exception("Expected \x49 or \x4D as the first byte")
    except Exception as e:
      print(e.args)

  def set_tag_offset(self):
    try:
      tag_offset = int.from_bytes(self.tiff_bytes[4:8], byteorder = self.endian)
      return(tag_offset)
    except:
      print("Invalid value for tag offset in bytes 4-8")

  def set_tag_count(self):
    try:
      tag_count = int.from_bytes(self.tiff_bytes[self.tag_offset:self.tag_offset+2],
                                 byteorder = self.endian)
      return(tag_count)
    except:
      print("Byte " + self.tag_offset + " does not exist in file")

  def set_tags(self):
  # TO DO create a single tag updater
  # TO DO parse offset values
    try:
      tags = dict()
      for i in range(0, self.tag_count):
        j = self.tag_offset + 2 + (i * 12)

        tagID = int.from_bytes(self.tiff_bytes[j:j+2], byteorder=self.endian)
        value_type = self.make_tag_dict(self.tiff_bytes[j+2:j+4], j+2, j+4)
        value_count = self.make_tag_dict(self.tiff_bytes[j+4:j+8], j+4, j+8)

        #TO DO handle short int values
        '''
        # does not handle pointers to sequences of short ints
        if value_type['intValue'] == 3:
          value_bytes = self.tiff_bytes[j+8:j+10]
        else:
          value_bytes = self.tiff_bytes[j+8:j+12]
        '''

        value = self.make_tag_dict(self.tiff_bytes[j+8:j+12], j+8, j+12)

        tags[tagID] = {'type': value_type,
                       'count': value_count,
                       'valueOrOffset': value}
      return(tags)
    except:
      print("Couldn't get tags ¯\_(ツ)_/¯ (still perfecting this part)")

  def make_tag_dict(self, byte_value, offset, stop_byte):
    tagDict = {'byteValue': byte_value,
               'intValue': int.from_bytes(byte_value, byteorder=self.endian),
               'offset': offset,
               'stopByte': stop_byte}
    return(tagDict)

  def set_tag_value(self, tag, value):
    try:
      if tag in self.tags:
        #TO DO make sure input is 4 bytes
        #TO DO allow non-byte values
        #TO DO allow other values (not tags) to be written?
        if isinstance(value, bytes):
          original_value = self.tags[tag]['valueOrOffset']['byteValue']
          offset = self.tags[tag]['valueOrOffset']['offset']
          stop_byte = self.tags[tag]['valueOrOffset']['stopByte']

          self.tiff_bytes[offset:stop_byte] = value
          self.tags = self.set_tags()

          return(original_value, self.tags[tag]['valueOrOffset']['byteValue'])
        else:
          raise Exception("Expected value to be a byte code string")
      else:
        raise Exception("Tag not found in tiff")
    except Exception as e:
      print(e.args)

  def write_tiff(self, filename):
    try:
      with open(filename, 'wb+') as f:
        f.write(self.tiff_bytes)
    except:
      print("Couldn't write file")
