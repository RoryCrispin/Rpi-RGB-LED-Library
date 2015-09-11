# test comment
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import rbgLib
# import time
import led_modes
import voice_command_interpreter

__author__ = 'Rory'
rbgLib.init()
frequency = 1000
redLED = rbgLib.LED(18, True, frequency)
greenLED = rbgLib.LED(24, True, frequency)
blueLED = rbgLib.LED(23, True, frequency)
rgbLEDx = rbgLib.rbgLed(redLED, greenLED, blueLED)

md = led_modes.mode_alert(rbgLib.aqua)
rgbLEDx.bind_mode(md)


def find_mode(mode_string):
    return led_modes.modes[mode_string]


def search_q(queries, search_string, return_list=False, fallback=None):
    try:
        if return_list:
            return queries[search_string]
        else:
            return queries[search_string][0]

    except:
        print("String Q not found: " + search_string + " Q: " + str(queries))
        return fallback

def rootQHandler(qs):
    try:
        print qs
        if qs['voicecommand'] != None:
            md = voice_command_interpreter.takeCommand(qs['avcommand'][0])
            rgbLEDx.bind_mode(md)
    except:
        mode_query_interpreter(qs)





def mode_query_interpreter(queries):
    mode = None
    colours = None
    try:
        mode = find_mode(search_q(queries, 'mode'))

        colours = []
        colours_q = search_q(queries, "hexcolour", return_list=True)
        for colour in colours_q:
            colours.append(rbgLib.hex_to_colour(colour))
        print colours
    except Exception:
        print Exception

    if mode == led_modes.mode_breathe:
        md = led_modes.mode_breathe(
            colours,
            search_q(
                queries,
                "period",
                fallback=0.01))
        rgbLEDx.bind_mode(md)

    elif mode == led_modes.mode_alert:

        md = led_modes.mode_alert(colours[0])
        rgbLEDx.interruptMode(md, pause=True, resume_thread=True)

    elif mode == led_modes.mode_strobe:
        md = led_modes.mode_strobe(
            colours,
            search_q(
                queries,
                "period",
                fallback=0.02))
        rgbLEDx.bind_mode(md)
    #elif mode == led_modes.None:
        # TODO I'm working on a 'mode' that kills all modes and turns the LEDs

    elif mode == led_modes.mode_static:
            md = led_modes.mode_static(
                colours[0])
            rgbLEDx.bind_mode(md)
        #elif mode == led_modes.None:
            # TODO I'm working on a 'mode' that kills all modes and turns the LEDs



    elif mode == led_modes.mode_rainbow:
        md =led_modes.mode_rainbow(
            search_q(
                queries,
                "period",
                fallback=0.01))
        rgbLEDx.bind_mode(md)

    elif mode == led_modes.mode_fadeto:
         md =led_modes.mode_fadeto(
             colours[0],
            search_q(
                queries,
                "period",
                fallback=0.01))
         rgbLEDx.bind_mode(md)



    else:
        rgbLEDx.set_colour(rbgLib.orange)


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("REQUEST YO YO!")
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Thanks!")

        parsed_path = urlparse.urlparse(self.path)
        qs = urlparse.parse_qs(parsed_path.query)
        rootQHandler(qs)
        return


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer

    server = HTTPServer(('192.168.1.141', 8001), GetHandler)

    print 'Starting server, use <Ctrl-C> to stop..'
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
