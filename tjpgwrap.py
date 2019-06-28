from ctypes import *
class TurboJPEG(object):
    """A Python wrapper of libjpeg-turbo for decoding and encoding JPEG image."""
    def __init__(self, lib_path):
        turbo_jpeg = cdll.LoadLibrary(lib_path)
        self.__init_decompress = turbo_jpeg.tjInitDecompress
        self.__init_decompress.restype = c_void_p
        self.__destroy = turbo_jpeg.tjDestroy
        self.__destroy.argtypes = [c_void_p]
        self.__destroy.restype = c_int
        self.__decompress_header = turbo_jpeg.tjDecompressHeader3
        self.__decompress_header.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, POINTER(c_int),
            POINTER(c_int), POINTER(c_int), POINTER(c_int)]
        self.__decompress_header.restype = c_int
        self.__decompress = turbo_jpeg.tjDecompress2
        self.__decompress.argtypes = [
            c_void_p, POINTER(c_ubyte), c_ulong, POINTER(c_ubyte),
            c_int, c_int, c_int, c_int, c_int]
        self.__decompress.restype = c_int
        self.__get_error_str = turbo_jpeg.tjGetErrorStr
        self.__get_error_str.restype = c_char_p

    def decode(self, jpeg_buf, pixel_format=0, flags=0):
        """decodes JPEG memory buffer to string buffer."""
        handle = self.__init_decompress()
        try:
            pixel_size = [3, 3, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4]
            width = c_int()
            height = c_int()
            jpeg_subsample = c_int()
            jpeg_colorspace = c_int()
            jpeg_array = create_string_buffer(jpeg_buf)
            src_addr = cast( byref(jpeg_array),POINTER(c_ubyte))
            status = self.__decompress_header(
                handle, src_addr, len(jpeg_buf), byref(width), byref(height),
                byref(jpeg_subsample), byref(jpeg_colorspace))
            if status != 0:
                raise IOError(self.__get_error_str().decode())
            scaled_width = width.value
            scaled_height = height.value
            imgsize = scaled_height *scaled_width * pixel_size[pixel_format]
            img_array = create_string_buffer(imgsize)
            dest_addr = cast( byref(img_array),POINTER(c_ubyte))
            status = self.__decompress(
                handle, src_addr, len(jpeg_buf), dest_addr, scaled_width,
                0, scaled_height, pixel_format, flags)
            if status != 0:
                raise IOError(self.__get_error_str().decode())
            del jpeg_array
            return img_array, scaled_width, scaled_height
        finally:
            self.__destroy(handle)
