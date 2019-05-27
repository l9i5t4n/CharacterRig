"""
module for making rig setup for "characterName"
main module 
"""

from rigLib.base import control
from rigLib.base import module

from rigLib.rig import arm
from rigLib.rig import ikChain
from rigLib.rig import leg
from rigLib.rig import neck
from rigLib.rig import spine

from rigLib.utils import joint

import maya.cmds as mc

rootJoint = 'root_JNT'
headJoint = 'head_JNT'
pelvisJoint = 'pelvis_JNT'

sceneScale = 1.0

def Build( characterName ):

    """
    main function to build rig
    """

    # make base

    baseRig = module.Base( characterName = characterName, scale = sceneScale, mainCtrlAttachObj = headJoint )

    # parent model

    modelGrp = '%d_GEO_GRP' % characterName
    mc.parent( modelGrp, baseRig.modelGrp )

    # parent skeleton 

    mc.parent( rootJoint, baseRig.jointsGrp )

    # control setup

    makeControlSetup( baseRig )

def makeControlSetup( baseRig ):

    """
    make control setup
    """

    # spine 

    spineJoints = [ 'spine1_JNT', 'spine2_JNT', 'spine3_JNT' ]

    spineRig = spine.Build( 
                            spineJoints = spineJoints,
                            rootJoint = rootJoint,
                            bodyLocator = 'body_LOC',
                            chestLocator = 'chest_LOC',
                            pelvisLocator = 'pelvis_LOC',
                            prefix = 'spine',
                            rigScale = sceneScale,
                            baseRig = baseRig 
                             )

    # neck

    neckJoints = [ 'neck1_JNT', 'neck2', 'head_JNT' ]

    neckRig = neck.Build(
                         neckJoints = neckJoints,
                         headJoint = headJoint,
                         prefix = 'neck',
                         rigScale = sceneScale,
                         baseRig = baseRig    
                        )
    
    mc.parentConstraint( spineJoints[-1], neckRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['body_CTRL'].C, neckRig['bodyAttachGrp'], mo = 1 )
    
    # left arm 

    lArmJoints = [ 'l_arm1_JNT', 'l_arm2_JNT', 'l_hand_JNT' ]
    lTopFingerJointA = 'l_topFingerA_JNT'
    lTopFingerJointB = 'l_topFingerB_JNT'
    lTopFingerJointC = 'l_topFingerC_JNT'
    lTopFingerJointD = 'l_topFingerD_JNT'
    lTopFingerJointE = 'l_topFingerE_JNT'

    lArmRig = arm.Build( 
                        armJoints = lArmJoints,
                        topFingerJointsA = lTopFingerJointA,
                        topFingerJointsB = lTopFingerJointB,
                        topFingerJointsC = lTopFingerJointC,
                        topFingerJointsD = lTopFingerJointD,
                        topFingerJointsE = lTopFingerJointE,
                        pvLocator = 'l_arm_poleVector_LOC',
                        scapulaJoint = 'l_scapula_JNT',
                        prefix = 'l_arm',
                        rigScale = sceneScale,
                        baseRig = baseRig
                        ) 

    mc.parentConstraint( spineJoints[-2], lArmRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['body_CTRL'].C, lArmRig['bodyAttachGrp'], mo = 1 )

    # right arm

    rArmJoints = [ 'r_arm1_JNT', 'r_arm2_JNT', 'r_hand_JNT' ]
    rTopFingerJointA = 'r_topFingerA_JNT'
    rTopFingerJointB = 'r_topFingerB_JNT'
    rTopFingerJointC = 'r_topFingerC_JNT'
    rTopFingerJointD = 'r_topFingerD_JNT'
    rTopFingerJointE = 'r_topFingerE_JNT'

    rArmRig = arm.Build( 
                        armJoints = rArmJoints,
                        topFingerJointsA = rTopFingerJointA,
                        topFingerJointsB = rTopFingerJointB,
                        topFingerJointsC = rTopFingerJointC,
                        topFingerJointsD = rTopFingerJointD,
                        topFingerJointsE = rTopFingerJointE,
                        pvLocator = 'r_arm_poleVector_LOC',
                        scapulaJoint = 'r_scapula_JNT',
                        prefix = 'r_arm',
                        rigScale = sceneScale,
                        baseRig = baseRig
                        ) 

    mc.parentConstraint( spineJoints[-2], rArmRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['body_CTRL'].C, rArmRig['bodyAttachGrp'], mo = 1 )

    # left leg

    lLegJoints = [ 'l_leg1_JNT', 'l_leg2_JNT', 'l_foot_JNT', 'l_ball_JNT', 'l_toe_JNT' ]

    lLegRig = leg.Build(
                        legJoints = lLegJoints,
                        pvLocator = 'l_leg_poleVector_LOC',
                        prefix = 'l_leg',
                        rigScale = sceneScale,
                        baseRig = baseRig
                        )
    
    mc.parentConstraint( spineJoints[0], lLegRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['body_CTRL'], lLegRig['bodyAttachGrp'], mo = 1 )

    # right leg

    rLegJoints = [ 'r_leg1_JNT', 'r_leg2_JNT', 'r_foot_JNT', 'r_ball_JNT', 'r_toe_JNT' ]

    rLegRig = leg.Build(
                        legJoints = rLegJoints,
                        pvLocator = 'r_leg_poleVector_LOC',
                        prefix = 'r_leg',
                        rigScale = sceneScale,
                        baseRig = baseRig
                        )
    
    mc.parentConstraint( spineJoints[0], rLegRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['body_CTRL'], rLegRig['bodyAttachGrp'], mo = 1 )
