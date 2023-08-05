from sdk.file_index import FileIndex
from sdk.hues import Hues
from PIL import Image
from .utils import get_arbg_from_16_bit
from struct import unpack


class Gumps:
    _file_index = FileIndex("gumpidx.mul", "gumpart.mul", 0xFFFF, 12)
    _cache = [None] * 0xFFFF
    _removed = [False] * 0xFFFF
    _patched = {}

    @classmethod
    def get_gump(cls, index, hue=0):
        def read_number():
            return unpack('h', stream.read(2))[0]
        # todo: patching etc
        patched = False
        stream, length, extra, patched = cls._file_index.seek(index)
        if not stream or extra == -1:
            return
        width = (extra >> 16) & 0xFFFF
        height = extra & 0xFFFF
        if not width or not height:
            return

        orig_pos = stream.tell()
        lookups = [0] * height
        for i in range(height):
            lookups[i] = unpack('i', stream.read(4))[0] * 4

        bitmap = Image.new("RGBA", (width, height))
        for y in range(height):
            x = 0
            stream.seek(orig_pos + lookups[y])
            while x < width:
                color, x_run = read_number(), read_number()
                if color != 0:
                    color ^= 0x8000
                    for pix in range(x_run):
                        bitmap.putpixel((x + pix, y), get_arbg_from_16_bit(color))
                x += x_run
        if hue:
            only_hue_grey = (hue & 0x8000) != 0
            hue = (hue & 0x3FFF) - 1
            return Hues.HUES[hue].apply_to(bitmap, only_grey_pixels=only_hue_grey)
        return bitmap


get_gump = Gumps.get_gump