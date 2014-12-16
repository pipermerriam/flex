import six


class IntKeyedDict(dict):
    """
    Returns a dictionary that treats integers and strings as the same key for
    retrieval.  Useful for the return value from the `ResponsesSerializer` whos
    keys are the response status codes.
    """
    def __getitem__(self, key):
        try:
            return super(IntKeyedDict, self).__getitem__(key)
        except KeyError:
            if isinstance(key, int):
                key = str(key)
            elif isinstance(key, six.string_types) and key.isdigit():
                key = int(key)
            else:
                raise

            return super(IntKeyedDict, self).__getitem__(key)
