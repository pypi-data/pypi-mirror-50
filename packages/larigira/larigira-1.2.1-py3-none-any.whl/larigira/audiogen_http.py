import os
import logging
import posixpath
from tempfile import mkstemp
import urllib.request
from urllib.parse import urlparse

log = logging.getLogger(__name__)


def put(url, destdir=None, copy=False):
    if url.split(":")[0] not in ("http", "https"):
        log.warning("Not a valid URL: %s", url)
        return None
    ext = url.split(".")[-1]
    if ext.lower() not in ("mp3", "ogg", "oga", "wma", "m4a"):
        log.warning('Invalid format (%s) for "%s"', ext, url)
        return None
    if not copy:
        return url
    fname = posixpath.basename(urlparse(url).path)
    # sanitize
    fname = "".join(c for c in fname if c.isalnum() or c in list("._-")).rstrip()
    tmp = mkstemp(suffix="." + ext, prefix="http-%s-" % fname, dir=destdir)
    os.close(tmp[0])
    log.info("downloading %s -> %s", url, tmp[1])
    fname, headers = urllib.request.urlretrieve(url, tmp[1])
    return "file://%s" % os.path.realpath(tmp[1])


def generate(spec):
    """
    resolves audiospec-static

    Recognized argument is  "paths" (list of static paths)
    """
    if "urls" not in spec:
        raise ValueError("Malformed audiospec: missing 'paths'")

    for url in spec["urls"]:
        ret = put(url, copy=True)
        if ret is None:
            continue
        yield ret


generate.description = "Fetch audio from an URL"
