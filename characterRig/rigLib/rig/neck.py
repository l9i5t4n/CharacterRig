"""
neck @ rig
"""

import maya.cmds as mc

from ..base import control
from ..base import module

from ..utils import joint
from ..utils import name

def Build(
        neckJoints,
        headJoint,
        prefix = 'neck',
        rigScale = 1.0,
        baseRig = None
        ):
    
    """
    @param neckJoints : list( str ), list of neck joints
    @param headJoint : str, head joint at the end of neck joint chain
    @param prefix : str, prefix to name new objects
    @param rigScale : float, scale factor for size of controls
    @param baseRig : instance of base.module.Base class
    @return : dictionnary with rig module objects
    """

    # make rig module

    rigModule = module.Module( prefix = prefix, baseObj = baseRig )

    # make attach groups

    bodyAttachGrp = mc.group( n = prefix + 'BodyAttach_GRP', em = 1, p = rigModule.partsGrp )
    baseAttachGrp = mc.group( n = prefix + 'BaseAttach_GRP', em = 1, p = rigModule.partsGrp )

    # make controls

    headCtrl = control.Control( prefix = prefix + '_head', scale = rigScale, translateTo = neckJoints[-1], 
                                parent = rigModule.controlsGrp, shape = 'circleY' )

    neckCtrl = control.Control( prefix = prefix + '_neck', scale = rigScale, translateTo = neckJoints[0], 
                                parent = rigModule.controlsGrp, shape = 'circleY' )

    # attach controls

    mc.parent( headCtrl.Off, neckCtrl.C )
    mc.parentConstraint( bodyAttachGrp, neckCtrl.Off, mo = 1 )

    # attach joints

    mc.orientConstraint( headCtrl.C, headJoint, mo = 1 )
    mc.orientConstraint( neckCtrl.C, neckJoints[0], mo = 1 )

    return { 'module':rigModule, 'baseAttachGRP':baseAttachGrp, 'bodyAttachGRP':bodyAttachGrp }
