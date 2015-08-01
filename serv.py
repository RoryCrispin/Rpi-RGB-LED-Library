# test comment
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import rbgLib
import time
import led_modes

__author__ = 'Rory'
rbgLib.init()
frequency = 1000
redLED = rbgLib.LED(18, True, frequency)
greenLED = rbgLib.LED(24, True, frequency)
blueLED = rbgLib.LED(23, True, frequency)
rgbLEDx = rbgLib.rbgLed(redLED, greenLED, blueLED)
rgbLEDx.set_colour(rbgLib.blue)


def find_mode(mode_string):
    return led_modes.modes[mode_string]


def search_q(queries, search_string):
    try:
        return queries[search_string]
    except:
        print("String Q not found: " + search_string + " Q: " + queries)
        return None


def mode_query_interpreter(queries):
    mode = None
    colour = None
    try:
        mode = find_mode(search_q(queries, 'mode')[0])
        colours = rbgLib.hex_to_colour(search_q(queries, "hexcolour"))

    except Exception:
        print Exception

    if mode == led_modes.mode_breathe:
        md = led_modes.mode_breathe(colours[0], 0.01)
        rgbLEDx.bind_mode(md)

    elif mode == led_modes.mode_alert:

        md = led_modes.mode_alert(colours[0])
        rgbLEDx.interruptMode(md, pause=True, resume_thread=True)

    elif mode == led_modes.mode_strobe:
        md = led_modes.mode_strobe(colour, 0.1)
        rgbLEDx.interruptMode(md)

    else:
        rgbLEDx.set_colour(rbgLib.orange)


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("REQUEST YO YO!")
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Thanks! <A HREF='javascript:history.go(0)'>Click to refresh the page</A>")

        parsed_path = urlparse.urlparse(self.path)
        qs = urlparse.parse_qs(parsed_path.query)
        print(qs)
        print qs['mode'][0]
        mode_query_interpreter(qs)

        return


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer

    server = HTTPServer(('192.168.1.13', 8001), GetHandler)

    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()


def handleResuest():
    pass
    # message_parts = [
    #         'CLIENT VALUES:',
    #         'client_address=%s (%s)' % (self.client_address,
    #                                     self.address_string()),
    #         'command=%s' % self.command,
    #         'path=%s' % self.path,
    #         'real path=%s' % parsed_path.path,
    #         'query=%s' % parsed_path.query,
    #
    #         'request_version=%s' % self.request_version,
    #         '',
    #         'SERVER VALUES:',
    #         'server_version=%s' % self.server_version,
    #         'sys_version=%s' % self.sys_version,
    #         'protocol_version=%s' % self.protocol_version,
    #         '',
    #         'HEADERS RECEIVED:',
    #         ]
    # for name, value in sorted(self.headers.items()):
    #     message_parts.append('%s=%s' % (name, value.rstrip()))
    # message_parts.append('')
    # message = '\r\n'.join(message_parts)
    # self.send_response(200)
    # self.end_headers()
    # self.wfile.write(message)
    # md = led_modes.mode_breathe(rbgLib.blue, 0.04)
    # rgbLEDx.bind_mode(md)
