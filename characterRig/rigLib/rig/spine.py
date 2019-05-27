"""
spine @ rig
"""

import maya.cmds as mc

from ..base import control
from ..base import module

def Build( 
            spineJoints,
            rootJoint,
            bodyLocator,
            chestLocator,
            pelvisLocator,
            prefix = 'spine',
            rigScale = 1.0,
            baseRig = None
             ):

    """
    @param spineJoints : list( str ), list of spine joints
    @param rootJoint : str, name of root joint
    @param spineCurve : str, name of spine curve
    @param bodyLocator : str, reference transform for position of body control
    @param chestLocator : str, reference transform for position of chest control
    @param pelvisLocator : str, reference transform for position of pelvis control
    @param prefix : str, prefix to name new objects
    @param rigScale : float, scale factor for size of controls
    @param baseRig : instance of base.module.Base class
    @return : dictionnary with rig module objects 
    """

    # make rig module

    rigModule = module.Module( prefix = prefix, baseObj = baseRig )

    # make controls

    pelvisCtrl = control.Control( prefix = prefix + '_pelvis', translateTo = pelvisLocator, scale = rigScale * 6,
                                    parent = rigModule.controlsGrp )

    bodyCtrl = control.Control( prefix = prefix + '_body', translateTo = bodyLocator, scale = rigScale * 4, 
                                parent = pelvisCtrl.C )
    
    chestCtrl = control.Control( prefix = prefix + '_chest', translateTo = chestLocator, scale = rigScale * 6,
                                parent = bodyCtrl.C )
    
    # attach object to control

    mc.orientConstraint( chestCtrl.C, spineJoints[2], mo = 1 )
    mc.orientConstraint( bodyCtrl.C, spineJoints[1], mo = 1 )
    mc.orientConstraint( pelvisCtrl.C, spineJoints[0], mo = 1 )

    return { 'module':rigModule, 'bodyCtrl':bodyCtrl }

    




    

    