import struct as structlib


def pprint(struct):
    class Visitor:
        def __init__(self, identation=0, max_array_elems_per_line=10):
            self.identation = identation
            self.max_array_elems_per_line = max_array_elems_per_line
            self.return_text = ""

        def visitRawTypeScalar(self, struct, item, meta):
            self.return_text += " " * self.identation
            self.return_text += "{} = {}\n".format(
                item, struct.__getattr__(item))

        def visitStructuredScalar(self, struct, item, meta):
            self.return_text += " " * self.identation
            self.return_text += "{} = {".format(item, meta)

            inner_visitor = Visitor(
                self.identation + 2, self.max_array_elems_per_line)
            struct.__getattr__(item).accept(inner_visitor)
            self.return_text += inner_visitor.return_text

            self.return_text += " " * self.identation
            self.return_text += "}"

        def visitRawTypeArray(self, struct, item, meta):
            self.return_text += " " * self.identation
            self.return_text += "{}[] = [".format(item)

            a = struct.__getattr__(item)
            element_in_line_idx = 0
            line_idx = 0

            if a.size > self.max_array_elems_per_line:
                self.return_text += "\n" + " " * self.identation

            for v in a.flat:
                if line_idx > 0 and element_in_line_idx == 0:
                    self.return_text += " " * self.identation
                self.return_text += " {}".format(v)
                element_in_line_idx += 1
                if element_in_line_idx > self.max_array_elems_per_line:
                    self.return_text += "\n"
                    line_idx += 1
                    element_in_line_idx = 0

            self.return_text += " ]\n"

        def visitStructuredArray(self, struct, item, meta):
            self.return_text += " " * self.identation
            self.return_text += "{}[] = [".format(item)

            a = struct.__getattr__(item)
            for v in a.flat:
                self.return_text += " " * (self.identation + 2) + "{\n"
                inner_visitor = Visitor(self.identation + 4,
                                        self.max_array_elems_per_line)
                v.accept(inner_visitor)
                self.return_text += inner_visitor.return_text
                self.return_text += " " * (self.identation + 2) + "}\n"
            self.return_text += " " * self.identation + "]\n"

    inner_visitor = Visitor(2)
    struct.accept(inner_visitor)
    return "{} {{\n{}}}\n".format(
        type(struct).__name__, inner_visitor.return_text)


def bin_write(struct, myfile):
    class Visitor:
        def __init__(self, thefile):
            self.f = thefile

        def visitRawTypeScalar(self, struct, item, meta):
            d = structlib.pack("={}".format(
                meta['format']), struct.__getattr__(item))
            self.f.write(d)

        def visitStructuredScalar(self, struct, item, meta):
            inner_visitor = Visitor(self.f)
            struct.__getattr__(item).accept(inner_visitor)

        def visitRawTypeArray(self, struct, item, meta):
            d = structlib.pack("={}{}".format(
                struct.__getattr__(item).size, meta['format']),
                *(struct.__getattr__(item).flatten()))
            self.f.write(d)

        def visitStructuredArray(self, struct, item, meta):
            a = struct.__getattr__(item)
            for v in a.flat:
                inner_visitor = Visitor(self.f)
                v.accept(inner_visitor)

    inner_visitor = Visitor(myfile)
    struct.accept(inner_visitor)


def bin_read(struct, myfile):
    class Visitor:
        def __init__(self, thefile):
            self.f = thefile

        def visitRawTypeScalar(self, struct, item, meta):
            fmt = "={}".format(meta['format'])
            n = structlib.calcsize(fmt)
            d = self.f.read(n)
            assert len(d) == n
            struct.__setattr__(item, struct.__getattr__(item).__class__(
                structlib.unpack(fmt, d)[0]))

        def visitStructuredScalar(self, struct, item, meta):
            inner_visitor = Visitor(self.f)
            struct.__getattr__(item).accept_and_init(inner_visitor)

        def visitRawTypeArray(self, struct, item, meta):
            fmt = "={}{}".format(
                struct.__getattr__(item).size, meta['format'])
            n = structlib.calcsize(fmt)
            d = self.f.read(n)
            assert len(d) == n
            tmp = structlib.unpack(fmt, d)
            struct.__getattr__(item).flat = tmp

        def visitStructuredArray(self, struct, item, meta):
            a = struct.__getattr__(item)
            for v in a.flat:
                inner_visitor = Visitor(self.f)
                v.accept_and_init(inner_visitor)

    inner_visitor = Visitor(myfile)
    struct.accept_and_init(inner_visitor)
