def _spread(__object: list | tuple | set):
    for item in list(__object):
        yield item
