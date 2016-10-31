#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import os
import qrcode
import hashlib
import tempfile
from PIL import Image
from lixingtie.web import RequestHandler, route


@route("/qrcode")
class QRCode(RequestHandler):
    def get(self):
        text = self.get_argument("text", "")
        print text
        name = hashlib.md5(text).hexdigest()
        path = os.path.join(tempfile.gettempdir(), "{0}.jpg".format(name))

        q = qrcode.main.QRCode(border=2)
        q.add_data(text)
        q.make()

        m = q.make_image()
        m.save(path)

        return self.file(path)
