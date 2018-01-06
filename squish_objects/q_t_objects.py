"""
import q_t_objects as ob

These functions are needed to be able to interact with QT objects
They do so using froglogics/squish's functions such as 
    object.children
    squish.snooze
    squish.waitForObject
    etc

Objectmap is a defined lookup where the main Qt Properties are described using JSON
By main I mean the common Objects that will always be there for example a BaseContainer is defined in theobject map whereas a button that changes colour or has visible/invisible props would not be defined in the objectMap
"""

import squish
import object
import __builtin__
import re
import test
import difflib
import objectMap



def findDescendantsByProps( parent_obj, properties_names_values, max_child_count=1, depth=-1):
    """
    NOTE: 
        This is a recursive funtion
        Finds children based on properties 
        negative depth is exhaustive which means this finds all(finite/infinite) children """
    if isinstance(parent_obj, basestring):
        parent_obj = squish.findObject(parent_obj) # framework function
    return _findChildrenByProps_func(
                                    parent_obj,
                                    properties_names_values,
                                    max_child_count,
                                    depth,
                                    [])

   
def _findChildrenByProps_func(parent_obj, properties_names_values, max_child_count, depth, found_children=[]):
    children = object.children(parent_obj)
    # Look for matching children
    for c in children:
        if _hasPropertiesAndValues(c, properties_names_values):
            found_children.append(c)
            if len(found_children) == max_child_count:
                return found_children

    # Look for matching grand-children
    if depth == 0:
        return found_children

    for c in children:
        found_children = _findChildrenByProps_func(
            c,
            properties_names_values,
            max_child_count,
            depth - 1,
            found_children)
        if len(found_children) == max_child_count:
            return found_children

    return found_children


def _hasPropertiesAndValues(obj, properties_names_values):
    # Verify type early to minimize property value comparisons
    if "type" in properties_names_values and \
        squish.className(obj) != properties_names_values["type"]:
            return False
    """
    add if statements that return false 

    """
    return True



def filterObjectListByProps(objectList, props):
    return [ obj for obj in objectList if _hasPropertiesAndValues(obj, props) ]


def getNextObject(properties, parent=None):
    """ cycle through each instance of an object
    Perfect for situations like when you need to click objects that have the same properties 
    example radio buttons
    """


    objectsOfInterest = []
    if _hasPropertiesAndValues(obj=parent, properties_names_values=properties):
        objectsOfInterest = [parent, ]

    objectsOfInterest += findDescendantsByProps(parent_obj=parent, properties_names_values=properties, max_child_count=-1, depth=-1)

    for occurence in range(len(objectsOfInterest)):
        yield getObject(properties=properties, parent=parent, occurence=occurence)


def getObject( properties, parent=None, occurence=0, visible=False ):
    """ properties can be dictionary(json), a symbolicName in the objectMap or a QT Object"""
    if isinstance(properties, dict):
        if _hasPropertiesAndValues(obj=parent,properties_names_values=properties):
            result = parent
        else: 
            try: 
                result = findDescendantsByProps(parent_obj=parent, properties_names_values=properties, max_child_count=occurence + 1, depth=-1)[occurence]

            except IndexError: 
                pass 
    elif isinstance( properties, basestring ):
        #QT/Squish symbolicNames  are sting 
        if properties.startswith(':'):
            assertNameInObjectMap(properties)
        result = obj_getter(properties)
    else: 
        # The properties argument is already an object 
        # Example in situations when a getter function is used in different scenarios
        # like waitFor or  regetting the same object multiple times 
        result = properties
    return result


def assertNameInObjectMap(name):
    """ check if a symbolicName exists in the objectMap.
    If it does not use the difflib library and log the closest match
    """
    objMap = objectMap.symbolicNames()
    if name not in objMap:
        potential = difflib.get_close_matches(name, objMap)
        msg = "The symbolic name {!r} is not in the objectMap, did you mean one of: {!r}".format(name, potential)
        #test.fatal(msg)
        raise RuntimeError(msg)

   
def obj_getter(properties):
    """ Call findDescendantsByProps/findChildrenByProps? """
    pass




def isPresent(myObjectOrName): pass

def isVisible(myObjectOrName): pass


def isEnabled(myObjectOrName): pass


def getText(obj, property='text'):
    """ find the text of an object
    property = text/shortNameText or whatever the developer decided to name the QML/QT text field
    """
    pass


def getImagePath(obj):
    """ return the source path of a QT/QML object"""
    pass 

