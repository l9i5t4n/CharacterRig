"""
leg @ rig
"""

import maya.cmds as mc

from ..base import control
from ..base import module

from ..utils import joint
from ..utils import name

def Build(
            legJoints,
            topToeJoints,
            additionnalToeJoints,
            pvLocator,
            scapulaJoint = '',
            prefix = 'l_leg',
            rigScale = 1.0,
            baseRig = None
            ):
    
    """
    @param legJoints : list( str ), list of leg joints
    @param topToeJoints : list( str ), list of metacarpal joints
    @param pvLocator : str, reference locator for position of Pole Vector control
    @param scapulaJoint : str, optional, scapulat joint, parent of top leg
    @param prefix : str, prefix to name new objects
    @param rigScale : float, scale factor for size of controls
    @param baseRig : instance of base.module.Base class
    @return : dictionnary with rig module objects
    """

    # make rig module

    rigModule = module.Module( prefix = prefix, baseObj = baseRig )

    # make attach groups

    bodyAttachGrp = mc.group( n = prefix + '_BodyAttach_GRP', em = 1, p = rigModule.partsGrp )
    baseAttachGrp = mc.group( n = prefix + '_BaseAttach_GRP', em = 1, p = rigModule.partsGrp )

    # make controls

    if scapulaJoint :

        scapulaCtrl = control.Control( prefix = prefix + '_scapula', translateTo = scapulaJoint, rotateTo = scapulaJoint, 
                        scale = rigScale * 3, parent = rigModule.controlsGrp, shape = 'sphere', 
                        lockChannels = [ 'v', 's' ] )
    
    footCtrl = control.Control( prefix = prefix + '_foot', translateTo = legJoints[2], scale = rigScale * 3, 
                                parent = rigModule.controlsGrp, shape = 'circleY' )

    ballCtrl = control.Control( prefix = prefix + '_ball', translateTo = legJoints[3], rotateTo = legJoints[3],
                                scale = rigScale * 3, parent = footCtrl.C, shape = 'circleZ' )

    poleVectorCtrl = control.Control( prefix = prefix + '_PV', translateTo = pvLocator, scale = rigScale,
                                    parent = rigModule.controlsGrp, shape = 'sphere' )

    if additionnalToeJoints :

        toeIKControls = []

        for topToeJoint in topToeJoints :

            toePrefix = name.removeSuffix( topToeJoint )[ :-1 ]
            toeEndJoint = mc.listRelatives( topToeJoint, ad = 1, type = 0 )[0]

            toeIKControl = control.Control( prefix = toePrefix, translateTo = toeEndJoint, scale = rigScale,
                                            parent = footCtrl.C, shape = 'circleY' )

            toeIKControls.append( toeIKControl )
    
    else :

        toeIKControl = control.Control( prefix = prefix + '_toe', translateTo = toeEndJoint, scale = rigScale,
                                        parent = footCtrl.C, shape = 'circleY' )

    # make IK handle

    if scapulaJoint :

        scapulaIK = mc.ikHandle( n = prefix + '_scapula_ikh', sol = 'ikSCsolver', sj = scapulaJoint, ee = legJoints[0] )[0]
        mc.hide( scapulaIK )
    
    legIK = mc.ikHandle( n = prefix + '_leg_ikh', sol = 'ikRPsolver', sj = legJoints[0], ee = legJoints[2] )[0]
    ballIK = mc.ikHandle( n = prefix + '_ball_ikh', sol = 'ikSCsolver', sj = legJoints[2], ee = legJoints[3] )[0]
    mainToeIK = mc.ikHandle( n = prefix + '_mainToe_ikh', sol = 'ikSCsolver', sj = legJoints[3], ee = legJoints[4] )[0]

    mc.hide( legIK, ballIK, mainToeIK )

    if additionnalToeJoints :

        for i, topToeJoint in enumerate( topToeJoints ):

            toePrefix = name.removeSuffix( topToeJoint )[:-1]
            toeJoints = joint.listHierarchy( topToeJoint )
        
            toeIK = mc.ikHandle( n = toePrefix + '_ikh', sol = 'ikSCsolver', sj = toeJoints[1], ee = toeJoints[-1] )[0]
            mc.hide( toeIK )
            mc.parent( toeIK, toeIKControl[i].C )

    # attach controls

    mc.parentConstraint( bodyAttachGrp, poleVectorCtrl.Off, mo = 1 )

    if scapulaJoint :

        mc.parentConstraint( baseAttachGrp, scapulaCtrl.Off, mo = 1 )
    
    # attach objects to control 

    mc.parent( legIK, ballCtrl.C )
    mc.parent( ballIK, mainToeIK, footCtrl.C )

    mc.poleVectorConstraint( poleVectorCtrl.C, legIK )

    if scapulaJoint :

        mc.parent( scapulaIK, scapulaCtrl.C )
        mc.pointContraint( scapulaCtrl.C, scapulaJoint )

    # make pole vector connection line

    pvLinePos1 = mc.xform( legJoints[1], q = 1, t = 1, ws = 1 )
    pvLinePos2 = mc.xform( pvLocator, q = 1, t = 1, ws = 1 )
    poleVectorCrv = mc.curve( n = prefix + '_PV_CRV', d = 1, p = [ pvLinePos1, pvLinePos2 ] )
    mc.cluster( poleVectorCrv + '.cv[0]', n = prefix + 'PV1_CLS', wn = [ legJoints[1], legJoints[1] ], bs = True )
    mc.cluster( poleVectorCrv + '.cv[1]', n = prefix + 'PV2_CLS', wn = [ poleVectorCtrl.C, poleVectorCtrl.C ], bs = True )
    mc.parent( poleVectorCrv, rigModule.controlsGrp )
    mc.setAttr( poleVectorCrv + '.template', 1 )
    mc.setAttr( poleVectorCrv + '.it', 0 )

    return { 'module':rigModule, 'baseAttachGrp':baseAttachGrp, 'bodyAttachGrp':bodyAttachGrp }