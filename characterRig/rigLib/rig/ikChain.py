"""
ikChain @ rig
"""

import maya.cmds as mc

from ..base import module
from ..base import control

def build(
        chainJoints,
        chainCurve,
        prefix = 'tail',
        rigScale = 1.0,
        smallestScalePercent = 0.5,
        fkParenting = True,
        baseRig = None
        ):
    
    """
    @param chainJoints : list( str ), list of chain joints
    @param chainCurve : str, name of chain of cubic curve
    @param prefix : str, prefix to name new objects
    @rigScale : float, scale factor for size of controls
    @smallestScalePercent : float, scale of smallest control at the end of chain compared to rigScale
    @fkParenting : bool, parent each control to previous one to make FK chain
    @baseRig : instance of base.module.Base class
    @return : None
    """

    # make rig module

    rigmodule = module.Module( prefix = prefix, baseObj = baseRig )

    # make chain curve clusters

    chainCurveCVs = mc.ls( chainCurve + '.cv[*]', fl = 1 )
    numChainCVS = len( chainCurveCVs )
    chainCurveClusters = []

    for i in range( numChainCVS ):

        cls = mc.cluster( chainCurveCVs[i], n = prefix + 'Cluster%d' % ( i + 1 ) )[1]
        chainCurveClusters.append( cls )

    mc.hide( chainCurveClusters )

    # parent chain curve

    mc.parent( chainCurve, rigmodule.partsNoTransGrp )

    # make attach groups

    baseAttachGrp = mc.group( n = prefix + '_BaseAttach_GRP', em = 1, p = rigmodule.partsGrp )

    mc.delete( mc.pointConstraint( chainJoints[0], baseAttachGrp ) )

    # make controls

    chainControl = []
    controlScaleIncrement = ( 1.0 - smallestScalePercent ) / numChainCVS
    mainCtrlScaleFactor = 5.0 

    for i in range( numChainCVS ):

        ctrlScale = rigScale * mainCtrlScaleFactor * ( 1.0 - ( i * controlScaleIncrement ) )
        Ctrl = control.Control( prefix = prefix + '%d' % ( i + 1), translateTo = chainCurveClusters[i], 
                                scale = ctrlScale, parent = rigmodule.controlsGrp, shape = 'sphere' )

        chainControl.append( Ctrl )

    # parent controls

    if fkParenting :

        for i in range( numChainCVS ):

            if i == 0 :

                continue
            
            mc.parent( chainControl[i].Off, chainControl[i-1].C )
    
    # attach clusters 

    for i in range( numChainCVS ):

        mc.parent( chainCurveClusters[i], chainControl[i].C )

    # attach control 

    mc.parentConstraint( baseAttachGrp, chainControl[0].Off, mo = 1 )

    # make IK handle

    chainIk = mc.ikHandle( n = prefix + '_ikh', sol = 'ikSplineSolver', sj = chainJoints[0], ee = chainJoints[-1], 
                            c = chainCurve, ccv = 0, parentCurve = 0 )[0]
    
    mc.hide(chainIk)
    mc.parent( chainIk, rigmodule.partsNoTransGrp )

    # add twist attribute

    twistAt = 'twist'
    mc.addAttr( chainControl[-1].C, ln = twistAt, k = 1  )
    mc.connectAttr( chainControl[-1].C + '.' + twistAt, chainIk + '.twist' )

    return { 'module': rigmodule, 'baseAttachGrp': baseAttachGrp }