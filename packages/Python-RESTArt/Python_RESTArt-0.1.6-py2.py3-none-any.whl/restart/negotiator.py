from __future__ import absolute_import

from werkzeug.http import parse_options_header

from . import exceptions


class Negotiator(object):
    """The class used to select the proper parser and renderer."""

    def select_parser(self, parser_classes, content_type):
        """Select the proper parser class.

        :param parser_classes: the parser classes to select from.
        :param content_type: the target content type.
        """
        content_type, _ = parse_options_header(content_type)

        for parser_class in parser_classes:
            if parser_class.content_type == content_type:
                return parser_class

        raise exceptions.UnsupportedMediaType(
            'Unsupported content type "%s" in request' % content_type
        )

    def select_renderer(self, renderer_classes, format_suffix):
        """Select the proper renderer class.

        Note:
            For simplicity, the content-negotiation here is only based
            on the format suffix specified in the request uri. The more
            standard (and also complex) Accept header is ignored.

        :param renderer_classes: the renderer classes to select from.
        :param format_suffix: the format suffix of the request uri.
        """
        # If no format suffix is specified, select the first renderer
        # class (if provided), or raise a NotAcceptable error.
        if not format_suffix:
            if renderer_classes:
                return renderer_classes[0]
            else:
                raise exceptions.NotAcceptable()

        for renderer_class in renderer_classes:
            if renderer_class.format_suffix == format_suffix:
                return renderer_class

        raise exceptions.NotFound('The requested resource with format '
                                  '".%s" is not found' % format_suffix)
