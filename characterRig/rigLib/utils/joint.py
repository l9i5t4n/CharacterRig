"""
joint @ utils
various joint utilities
"""

import maya.cmds as mc

def listHierarchy( topJoint, withEndJoint = True ):

    """
    list joint hierarchy starting with top joint

    @param topJoint : str, joint to get listed with its joint hierarchy
    @param withEndJoint : bool, list hierarchy with end joint
    @return : list( str ), listed joints starting with top joint
    """

    listedJoints = mc.listRelatives( topJoint, type = 'joint', ad = True )
    listedJoints.append( topJoint )
    listedJoints.reverse

    completeJoints = listedJoints[:]

    if not withEndJoint:

        completeJoints = [ j for j in listedJoints if mc.listRelatives( j, c = 1, type = 'joint' ) ]
    
    return completeJoints