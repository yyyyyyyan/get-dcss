import gzip
import re
from io import BytesIO
from shutil import copyfileobj
from ssl import SSLContext
from urllib.parse import urlencode
from urllib.request import urlopen

data = {"all": "Show all of the digits"}
response = urlopen(
    "https://primes.utm.edu/primes/page.php?id=37569",
    data=urlencode(data).encode(),
    context=SSLContext(),
)

html = response.read()
match = re.search(r"<blockquote>\n([\d ]+)\n</blockquote>", html.decode())
prime = int(match[1].replace(" ", ""))

gzip_bytes = BytesIO(
    prime.to_bytes((prime.bit_length() + 7) // 8, byteorder="big")[:-1]
)
with gzip.open(gzip_bytes) as gzip_file:
    with open("css-descramble.c", "wb") as code_file:
        copyfileobj(gzip_file, code_file)
