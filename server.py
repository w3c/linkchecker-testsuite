from http import server
import socketserver
import os
import io

PORT = 9999

class LinkTestSuiteRequestHandler(server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = server.SimpleHTTPRequestHandler.translate_path(self, path)
        if path.endswith("/"):
            path = path + "index.html"
        relpath = os.path.relpath(path, os.getcwd())
        if self.headers.get('Host') == "checklink2.test:" + str(PORT):
            fullpath = "server-content/alt/" + relpath
        else:
            fullpath = relpath.replace('link-testsuite', 'server-content')
        self.localpath = fullpath
        return fullpath

    def handle_magic_http_status(self):
        import re
        m = re.match("^/link-testsuite/http\?code=([0-9][0-9][0-9])", self.path)
        if m:
            print(self.path)
            self.send_error(int(m[1]))
            return

    def do_HEAD(self):
        self.handle_magic_http_status()
        server.SimpleHTTPRequestHandler.do_HEAD(self)

    def do_GET(self):
        self.handle_magic_http_status()
        server.SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        try:
            with io.open(self.localpath + ".headers") as headers:
                for header in headers.split("\n"):
                    self.send_header(header.split(":")[0], header.split(":")[1])
        except:
            pass
        server.SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), LinkTestSuiteRequestHandler) as httpd:
        httpd.serve_forever()
