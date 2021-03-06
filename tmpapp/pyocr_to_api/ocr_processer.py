import pyocr
import pyocr.builders
from collections import namedtuple

from .utils import get_default_ocr_tool
from .pdf_processer import PDFProcesser
from .image_processer import ImageProcesser

DEFAULT_BUILDER = pyocr.builders.LineBoxBuilder()
DEFAULT_IMAGE_PROCESSER = ImageProcesser()
DEFAULT_OCR_TOOL = get_default_ocr_tool()
DEFAULT_PDF_PROCESSER = PDFProcesser()
DEFAULT_DATA_PROCESSERS = {
    'pdf': DEFAULT_PDF_PROCESSER,
    'image': DEFAULT_IMAGE_PROCESSER,
}

OCRProcessedImage = namedtuple('OCRProcessedImage', ['images', 'text'])


class OCRProcessor:
    def __init__(
            self,
            ocr_tool=DEFAULT_OCR_TOOL,
            lang='pol',
            default_builder=DEFAULT_BUILDER,
            data_processers=DEFAULT_DATA_PROCESSERS,
    ):
        self._ocr_tool = ocr_tool
        self._lang = lang if self._is_present(lang) else 'eng'
        self._default_builder = default_builder
        self._data_processer = data_processers

    def process(self, data_file):
        data_processer = self._choose_data_processor(data_file)
        for image in data_processer.open(data_file):
            text = self._ocr_tool.image_to_string(
                image=image,
                lang=self._lang,
                builder=self._default_builder,
            )
            yield OCRProcessedImage(images=image, text=text)

    def _is_present(self, lang):
        return lang in self._ocr_tool.get_available_languages()

    def _validate_tool(self, ocr_tool):
        return ocr_tool.is_available()

    def _choose_data_processor(self, data_file):
        return self._data_processer.get(
            self._get_file_extension(data_file),
            self._data_processer['image'],
        )

    def _get_file_extension(self, data_file):
        return data_file.split('.')[-1]