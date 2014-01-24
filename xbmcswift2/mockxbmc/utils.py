from xml.dom.minidom import parse
import os
import polib


def load_addon_strings(addon, filename):
    '''This is not an official XBMC method, it is here to faciliate
    mocking up the other methods when running outside of XBMC.'''
    if os.path.exists(filename):
        def get_strings(fn):
            po = polib.pofile(fn)
            strings = dict((entry.msgctxt[1:], entry.msgid) for entry in po)
            return strings
    else:
        def get_strings(fn):
            fn = os.path.splitext(fn)[0] + '.xml'
            xml = parse(fn)
            strings = dict((tag.getAttribute('id'), tag.firstChild.data) for tag in xml.getElementsByTagName('string'))
            #strings = {}
            #for tag in xml.getElementsByTagName('string'):
                #strings[tag.getAttribute('id')] = tag.firstChild.data
            return strings
    addon._strings = get_strings(filename)


def get_addon_id(addonxml):
    '''Parses an addon id from the given addon.xml filename.'''
    xml = parse(addonxml)
    addon_node = xml.getElementsByTagName('addon')[0]
    return addon_node.getAttribute('id')


def get_addon_name(addonxml):
    '''Parses an addon name from the given addon.xml filename.'''
    xml = parse(addonxml)
    addon_node = xml.getElementsByTagName('addon')[0]
    return addon_node.getAttribute('name')
