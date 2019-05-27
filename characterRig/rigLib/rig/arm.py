"""
arm @ rig
"""

import maya.cmds as mc

from ..base import control
from ..base import module

from ..utils import name
from ..utils import joint

def Build(
            armJoints,
            topFingerJointsA,
            topFingerJointsB,
            topFingerJointsC,
            topFingerJointsD,
            topFingerJointsE,
            pvLocator,
            scapulaJoint = '',
            prefix = 'l_arm',
            rigScale = 1.0,
            baseRig = None
            ):
    
    """
    @param armJoints : list( str ), list of arm joints
    @param topFingerJoints : list( str ), list of metacarpal joints
    @param pvLocator : str, reference locator for position of Pole Vector control
    @param scapulaJoint : str, scapulat joint, parent of top arm
    @param prefix : str, prefix to name new objects
    @param rigScale : float, scale factor for size of controls
    @param baseRig : instance of base.module.Base class
    @return : dictionnary with rig module
    """

    # make rig module

    rigModule = module.Module( prefix = prefix, baseObj = baseRig )

    # make attach groups

    baseAttachGrp = mc.group( n = prefix + '_BaseAttach_GRP', em = 1, p = rigModule.partsGrp )
    bodyAttachGrp = mc.group( n = prefix + '_BodyAttach_GRP', em = 1, p = rigModule.partsGrp )

    # make controls

    if scapulaJoint :

        scapulaCtrl = control.Control( prefix = prefix +'_scapula', translateTo = scapulaJoint, rotateTo = scapulaJoint,
                                        scale = rigScale * 3, parent = rigModule.controlsGrp, shape = 'sphere',
                                        lockChannels = [ 'v','s' ] )
    
    handCtrl = control.Control( prefix = prefix + '_hand', translateTo = armJoints[2], scale = rigScale * 3,
                                parent = rigModule.controlsGrp, shape = 'sphere' )
    
    poleVectorCtrl = control.Control( prefix = prefix + '_PV', translateTo = pvLocator, scale = rigScale,
                                        parent = rigModule.controlsGrp, shape = 'sphere' )

    fingerCtrlListA = []
    fingerCtrlListB = []
    fingerCtrlListC = []
    fingerCtrlListD = []
    fingerCtrlListE = []

    fingerJointsListA = mc.listRelatives( topFingerJointsA, ad = 1 )
    fingerJointsListB = mc.listRelatives( topFingerJointsB, ad = 1 )
    fingerJointsListC = mc.listRelatives( topFingerJointsC, ad = 1 )
    fingerJointsListD = mc.listRelatives( topFingerJointsD, ad = 1 )
    fingerJointsListE = mc.listRelatives( topFingerJointsE, ad = 1 )

    fingerJointsListA.reverse()
    fingerJointsListB.reverse()
    fingerJointsListC.reverse()
    fingerJointsListD.reverse()
    fingerJointsListE.reverse()

    for fingerJoint in fingerJointsListA :

        fingerPrefix = name.removeSuffix( fingerJoint )[:-1]
        
        fingerCtrl = control.Control( prefix = fingerPrefix, scale = rigScale, parent = handCtrl.C, shape = 'sphere' )
        fingerCtrlListA.append( fingerCtrl )

    for i in range( len( fingerJointsListA ) ):

        mc.delete( mc.pointConstraint( fingerJointsListA[i-1], fingerCtrlListA[i-1] ) )
        mc.orientConstraint( fingerJointsListA[i-1], fingerCtrlListA[i-1] )

    for fingerJoint in fingerJointsListB :

        fingerPrefix = name.removeSuffix( fingerJoint )[:-1]
        
        fingerCtrl = control.Control( prefix = fingerPrefix, scale = rigScale, parent = handCtrl.C, shape = 'sphere' )
        fingerCtrlListB.append( fingerCtrl )

    for i in range( len( fingerJointsListB ) ):

        mc.delete( mc.pointConstraint( fingerJointsListB[i-1], fingerCtrlListB[i-1] ) )
        mc.orientConstraint( fingerJointsListB[i-1], fingerCtrlListB[i-1] )
    
    for fingerJoint in fingerJointsListC :

        fingerPrefix = name.removeSuffix( fingerJoint )[:-1]
        
        fingerCtrl = control.Control( prefix = fingerPrefix, scale = rigScale, parent = handCtrl.C, shape = 'sphere' )
        fingerCtrlListC.append( fingerCtrl )

    for i in range( len( fingerJointsListC ) ):

        mc.delete( mc.pointConstraint( fingerJointsListC[i-1], fingerCtrlListC[i-1] ) )
        mc.orientConstraint( fingerJointsListC[i-1], fingerCtrlListC[i-1] )
    
    for fingerJoint in fingerJointsListD :

        fingerPrefix = name.removeSuffix( fingerJoint )[:-1]
        
        fingerCtrl = control.Control( prefix = fingerPrefix, scale = rigScale, parent = handCtrl.C, shape = 'sphere' )
        fingerCtrlListD.append( fingerCtrl )

    for i in range( len( fingerJointsListD ) ):

        mc.delete( mc.pointConstraint( fingerJointsListD[i-1], fingerCtrlListD[i-1] ) )
        mc.orientConstraint( fingerJointsListD[i-1], fingerCtrlListD[i-1] )

    for fingerJoint in fingerJointsListE :

        fingerPrefix = name.removeSuffix( fingerJoint )[:-1]
        
        fingerCtrl = control.Control( prefix = fingerPrefix, scale = rigScale, parent = handCtrl.C, shape = 'sphere' )
        fingerCtrlListE.append( fingerCtrl )

    for i in range( len( fingerJointsListE ) ):

        mc.delete( mc.pointConstraint( fingerJointsListE[i-1], fingerCtrlListE[i-1] ) )
        mc.orientConstraint( fingerJointsListE[i-1], fingerCtrlListE[i-1] )

    # FK parenting finger controls

    for i in range ( len( fingerCtrlListA ) ):

        if i == 0 :

            continue

        mc.parent( fingerCtrlListA[i].Off, fingerCtrlListA[i-1].C )
    
    for i in range ( len( fingerCtrlListB ) ):

        if i == 0 :

            continue

        mc.parent( fingerCtrlListB[i].Off, fingerCtrlListB[i-1].C )
    
    for i in range ( len( fingerCtrlListC ) ):

        if i == 0 :

            continue

        mc.parent( fingerCtrlListC[i].Off, fingerCtrlListC[i-1].C )
    
    for i in range ( len( fingerCtrlListD ) ):

        if i == 0 :

            continue

        mc.parent( fingerCtrlListD[i].Off, fingerCtrlListD[i-1].C )
    
    for i in range ( len( fingerCtrlListE ) ):

        if i == 0 :

            continue

        mc.parent( fingerCtrlListE[i].Off, fingerCtrlListE[i-1].C )

    # make IK handle 

    if scapulaJoint :

        scapulaIK = mc.ikHandle( n = prefix + '_scapula_ikh', sol = 'ikSCsolver', sj = scapulaJoint, ee = armJoints[0] )[0]
        mc.hide( scapulaIK )

    armIK = mc.ikHandle( n = prefix + '_arm_ikh', sol = 'ikRPsolver', sj = armJoints[0], ee = armJoints[2] )[0]
    mc.hide( armIK )

    # attach controls

    mc.parentConstraint( baseAttachGrp, poleVectorCtrl.Off, mo = 1 )

    if scapulaJoint :

        mc.parentConstraint( baseAttachGrp, scapulaCtrl.Off, mo = 1 )

    # attach object to control

    mc.parent( armIK, handCtrl.C )
    
    mc.poleVectorConstraint( poleVectorCtrl.C, armIK )

    if scapulaJoint : 

        mc.parent( scapulaIK, scapulaCtrl.C )
        mc.pointConstraint( scapulaCtrl.C, scapulaJoint )

    # make pole vector connection line

    pvLinePos1 = mc.xform( armJoints[1], q = 1, t = 1, ws = 1 )
    pvLinePos2 = mc.xform( pvLocator, q = 1, t = 1, ws = 1 )
    poleVectorCRV = mc.curve( n = prefix + 'PV_CRV', d = 1, p = [ pvLinePos1, pvLinePos2 ] )
    mc.cluster( poleVectorCRV + '.cv[0]', n = prefix + 'PV1_CLS', wn = [ armJoints[1], armJoints[1] ], bs = True )
    mc.cluster( poleVectorCRV + '.cv[1]', n = prefix + 'PV2_CLS', wn = [ poleVectorCtrl.C, poleVectorCtrl.C ], bs = True )
    mc.parent( poleVectorCRV, rigModule.controlsGrp )
    mc.setAttr( poleVectorCRV + '.template', 1 )
    mc.setAttr( poleVectorCRV + '.it', 0 )

    return { 'module':rigModule, 'baseAttachGRP':baseAttachGrp, 'bodyAttachGRP':bodyAttachGrp }