from jpype import *
import chardet
import threading

lock = threading.Lock()

ByteArrayInputStream        = JClass('java.io.ByteArrayInputStream')
ByteArrayOutputStream       = JClass('java.io.ByteArrayOutputStream')


class Extractor(object):
    extractor = None
    data      = None

    def __init__(self, **kwargs):
        if 'pdf' in kwargs:
            self.data = kwargs['pdf']
        else:
            raise Exception('No pdf provided')
        if "language" in kwargs:
            self.language = kwargs['language']
        else:
            self.language = "en"
        if "options" in kwargs:
            self.options = kwargs['options']
        else:
            self.options = ""
        if "debug" in kwargs:
            self.debug = kwargs['debug']
        else:
            self.debug = 0
        try:
            # make it thread-safe
            if threading.activeCount() > 1:
                if isThreadAttachedToJVM() == False:
                    attachThreadToJVM()
            lock.acquire()

            self.extractor = JClass("com.java.app.PDFExtract")()

        finally:
            lock.release()

        self.reader = ByteArrayInputStream(self.data)

    def getHTML(self):
        return str(self.extractor.Extract(self.reader, JString(self.language), JString(self.options), self.debug).toString())
