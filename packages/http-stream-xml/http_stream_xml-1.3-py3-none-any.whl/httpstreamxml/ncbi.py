import xml.sax
from ssl import SSLSocket
import ssl
import socket

# Entrezgene_gene -> Gene-ref
items_to_collect = ['Gene-ref_desc', 'Entrezgene_summary', 'Gene-ref_syn']


class StreamHandler(xml.sax.handler.ContentHandler):

  items = {}
  fetching = {}

  def startElement(self, name, attrs):
    if name in items_to_collect :
      self.fetching[name] = True
      self.items[name] = []

  def endElement(self, name):
    if name in items_to_collect:
      print(name)
      print(''.join(self.items[name]))
      print()
      self.fetching[name] = False
      if len(self.items) == len(items_to_collect):
        raise StopIteration

  def characters(self, content):
    for name in self.items.keys():
      if self.fetching[name]:
        self.items[name].append(content)


if __name__ == '__main__':
  parser = xml.sax.make_parser()
  parser.setContentHandler(StreamHandler())

  header = b'GET /entrez/eutils/efetch.fcgi?db=gene&id=5465&retmode=xml HTTP/1.1\r\nHost: eutils.ncbi.nlm.nih.gov\r\nUser-Agent: For the lulz..\r\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\r\nContent-Length: 0'
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)
  s.connect(('eutils.ncbi.nlm.nih.gov', 443))
  s.send(header + b'\r\n\r\n\r\n\r\n')  # header + two times CR_LF + empty body + 2 times CR_LF to complete the request

  BOB = '\r\n\r\n'  # body begin
  chunk = ''
  in_body = False  # started fetching body
  fetched_bytes = 0
  while True:
    buf = s.recv(4096)
    if not buf:
      break
    fetched_bytes += len(buf)
    chunk += buf.decode()
    if not in_body and BOB in chunk:
      print()
      print(f'Header\n{chunk[:chunk.find(BOB) + len(BOB)]}')
      print()
      chunk = chunk[chunk.find(BOB) + len(BOB):]
      in_body = True

    if in_body:
      print(f'Fetched:\n{chunk}')

      # skip chunk length lines
      to_parse = []
      for line in chunk.split('\r\n')[:-1]:
        if len(line) < 5 and len(line) > 0 and line[0] in '0123456789abcdef':
          continue
        to_parse.append(line)
      to_parse = '\r\n'.join(to_parse)
      chunk = chunk.split('\r\n')[-1]  # do not parse not completed lines - leave them in chunk

      try:
        parser.feed(to_parse)
      except StopIteration:
        break
  s.close()

  print(f'Fetched {fetched_bytes} bytes')
