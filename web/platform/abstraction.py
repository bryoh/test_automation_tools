"""
All functions in this module provide abstraction features to toher plaform modules.
These are very simple abstractions and does not need to replace the need for higher level
abstractions such as ssh.command()  copy files. 


All functions take info (a dictionary or *kwargs)  as the first argument which contains the required
infomation for calling the low level functions
"""

import selenium


def launch(info):
    type_of_platform= str(info.get('type')).lower()
    if type_of_platform == 'firefox':
        return web.platform.firefox.launch(info)
    if type_of_platform == 'chrome':
        return web.platform.chrome.launch(info)
    if type_of_platform == 'opera':
        return web.platform.opera.launch(info)
    if type_of_platform == 'android':
        return web.platform.android(info)
    if type_of_platform == 'safari':
        return web.platform.safari.launch(info)
    #TODO: Should this be an AssertionError if the requested type is not available? Or should there be a common way of launching
    return None

def kill(info):
    type_of_platform= str(info.get('type')).lower()
    if type_of_platform == 'firefox':
        return web.platform.firefox.kill(info)
    if type_of_platform == 'chrome':
        return web.platform.chrome.kill(info)
    if type_of_platform == 'opera':
        return web.platform.opera.kill(info)
    if type_of_platform == 'android':
        return web.platform.android(info)
    if type_of_platform == 'safari':
        return web.platform.safari.kill(info)
