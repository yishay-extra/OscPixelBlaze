from pixelblaze import *
from pythonosc import dispatcher, osc_server
from pprint import pprint

LOCAL_IP = '127.0.0.1'
OSC_SERVER_PORT = 7500
PB: Pixelblaze


def set_pixelblaze():
    global PB
    for ipAddress in Pixelblaze.EnumerateAddresses(timeout=1000):
        print("Found Pixelblaze at ", ipAddress)
        PB = Pixelblaze(ipAddress)


def get_osc_dispatcher():
    dp = dispatcher.Dispatcher()
    dp.map("/pattern", pattern_handler, "pattern_name")
    dp.map("/brightness", brightness_handler, "brightness_value")
    dp.map("/method", method_handler)
    dp.map("/clear", clear_handler)
    dp.set_default_handler(default_handler)
    return dp


def pattern_handler(unused_addr, args, pattern_name):
    global PB
    print(f'Setting pattern: {pattern_name}')
    PB.setActivePatternByName(pattern_name)


def brightness_handler(unused_addr, args, brightness_value):
    global PB
    print(f'Setting brightness: {brightness_value}')
    PB.setBrightnessSlider(brightness_value)


def method_handler(unused_addr, *args):
    global PB
    method_name = args[0]
    print(f'Executing PixelBlaze Method: {method_name}')
    try:
        method = PB.__getattribute__(method_name)
        resp = method(*args[1:]) if len(args) > 1 else method()
        pprint(resp)
    except AttributeError as e:
        print(e)


def clear_handler(unused_addr):
    global PB
    print(f'Clearing')
    PB.setBrightnessSlider(0.0)


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


def main():
    set_pixelblaze()
    dp = get_osc_dispatcher()

    server = osc_server.ThreadingOSCUDPServer((LOCAL_IP, OSC_SERVER_PORT), dp)
    print(f'OSC Serving on {server.server_address}')
    server.serve_forever()


if __name__ == '__main__':
    main()
