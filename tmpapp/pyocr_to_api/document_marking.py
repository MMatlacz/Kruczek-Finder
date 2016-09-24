from PIL import ImageDraw, ImageEnhance


class WrongMessageException(Exception):
    pass


class DocumentMarking:
    def __init__(self):
        pass

    def mark(self, image_object, position, message):
        """

        :param image_object: Image as object in image extension not in pdf.
        :param position: Position [(y0,x0),(y1,x1)] ex. ((2085, 153), (2243, 179)).
        :param message: ERROR or WARNING.
        :return: Image objects with marked rectangle as clause message.
        """
        im_reduced = self._reduce_opacity(image_object, 0.8)
        marked = self._imprint(im_reduced, position, message)
        return marked

    @staticmethod
    def _reduce_opacity(im, opacity):
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    def _imprint(self, image, position, message, opacity=0.5):
        color = MessageFactory.factory(message).color(opacity)
        y0, x0, y1, x1 = position
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        draw = ImageDraw.Draw(image)
        draw.rectangle([(x0, y0), (x1, y1)], fill=color)
        return image


class MessageFactory:
    @staticmethod
    def factory(message):
        if message == 'ERROR':
            return ErrorColor()
        elif message == 'WARNING':
            return WarningColor()
        else:
            raise WrongMessageException

    @staticmethod
    def color(opacity):
        raise NotImplementedError


class ErrorColor(MessageFactory):
    @staticmethod
    def color(opacity):
        return (200, 0, 0, int(opacity * 255))


class WarningColor(MessageFactory):
    @staticmethod
    def color(opacity):
        return (300, 300, 0, int(opacity * 255))