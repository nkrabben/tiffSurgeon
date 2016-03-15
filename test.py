import tiffSurgeon
import pprint

filename = input("File to operate on: ")
a = tiffSurgeon.Tiff(tiffSurgeon.read_tiff_file(filename))

pprint.pprint(a.tags)
print("Endian: " + a.endian)
print("Tag offset: " + str(a.tag_offset))
print("Calculated tag count: " + str(a.tag_count))
print("Tags available: " + str(len(a.tags)))

print("Tag byte values:")
for tag in a.tags:
  print(str(tag) + ": " + \
        str(a.tags[tag]['valueOrOffset']['byteValue']))
print("\n### Nested list of all tags is printed above\n")

tag = input("What tag do you want to nuke: ")
#value = input("New value for tag (must be 4 bytes): ")
#print(isinstance(value, bytes))
b = a.set_tag_value(int(tag), b'\x00\x00\x00\x00')
print("Old value: " + str(b[0]))
print("New value: " + str(b[1]))

a.write_tiff('new.tif')
print("Saved new tiff as new.tif. Compare to the original tiff using " + \
      "'cmp -l <original> new.tif'")
