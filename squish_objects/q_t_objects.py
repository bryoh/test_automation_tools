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


