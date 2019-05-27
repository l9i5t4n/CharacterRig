"""
tranform @ utils

Function to manipulate and create tranforms
"""

import maya.cmds as mc

from .import name

def makeOffsetGrp( object, prefix = '' ):

    """
    make offset group for given object

    @param object : transform object to get offset group
    @param prefix : prefix to name new objects
    @return : str, name of new offset group
    """

    if not prefix :

        prefix = name.removeSuffix( object )

    offsetGrp = mc.group( n = prefix + _offset_GRP, em = 1 )

    objectParent = mc.listRelatives( object, p = 1 )

    if objectParent :

        mc.parent( offsetGrp, objectParent[0] )

    # match object tranform

    mc.delete( mc.parentContraint( object, offsetGrp ) )
    mc.delete( mc.scaleConstraint( object, offsetGrp ) )

    # parent object under group

    mc.parent( object, offsetGrp )

    return offsetGrp