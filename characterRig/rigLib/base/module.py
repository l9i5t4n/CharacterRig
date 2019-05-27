"""
module for making top rig structure and rig module
"""

import maya.cmds as mc

sceneObjectType = 'rig'

from . import control

class Base():

    """
    class for building top rig structure
    """

    def __init__(
                self,
                characterName = 'new',
                scale = 1.0,
                mainCtrlAttachObj = ''
                ):

        """
        """

        self.topGrp = mc.group( n = characterName + '_rig_GRP' , em = 1 )
        self.rigGrp = mc.group( n = 'rig_GRP', em = 1, p = self.topGrp )
        self.modelGrp = mc.group( n = 'model_GRP', em = 1, p = self.topGrp )

        characterNameAt = 'characterName'
        sceneObjectTypeAt = 'sceneObjectType'

        for at in [ characterNameAt, sceneObjectTypeAt ]:

            mc.addAttr( self.topGrp, ln = at, dt = 'string' )
        
        mc.setAttr( self.topGrp + '.' + characterNameAt, characterName, type = 'string', l = 1 )
        mc.setAttr( self.topGrp + '.' + sceneObjectTypeAt, sceneObjectType, type = 'string', l = 1 )

        # making global control

        global1Ctrl = control.Control(
                                    prefix = 'global1',
                                    scale = scale * 10,
                                    parent = self.rigGrp,
                                    lockChannels = [ 'v' ]
                                    )
        
        global2Ctrl = control.Control(
                                    prefix = 'global2',
                                    scale = scale * 20,
                                    parent = global1Ctrl.C,
                                    lockChannels = [ 's', 'v' ]
                                    )

        self._flattenGlobalCtrlShape( global1Ctrl.C )
        self._flattenGlobalCtrlShape( global2Ctrl.C )

        for axis in [ 'y', 'z' ]:

            mc.connectAttr( global1Ctrl + '.sx', global1Ctrl + '.s' + axis )
            mc.setAttr( global1Ctrl + '.s' + axis, k = 0 )
        
        # make more groups

        self.partsGrp = mc.group( n = 'parts_GRP', em = 1, p = self.rigGrp )
        self.jointsGrp = mc.group( n = 'joints_GRP', em = 1, p = self.partsGrp )

        mc.setAttr( self.partsGrp + 'it', 0, l = 1 )

        self.modulesGrp = mc.group( n = 'modules_GRP', em = 1, p = global2Ctrl.C )

        # make main control

        mainCtrl = control.Control(
                                    prefix = 'main',
                                    scale = scale * 20,
                                    parent = global2Ctrl.C,
                                    translateTo = mainCtrlAttachObj,
                                    lockChannels = [ 't', 'r', 's', 'v' ]
                                    )

        self._adjustMainCtrlShape( mainCtrl, scale )

        if mc.objExists( mainCtrlAttachObj ):

            mc.parent( mainCtrlAttachObj, mainCtrl.Off, mo = 1 )
        
        mainVisAts = [ 'modelVis', 'jointsVis' ]
        mainDispAts = [ 'modelDisp', 'jointsDisp' ]
        mainObjList = [ self.modelGrp, self.jointsGrp ]
        mainObjVisDvList = [ 1, 0 ]

        # add rig visibility connections

        for at, obj, dfVal in zip( mainVisAts, mainObjList, mainObjVisDvList ):

            mc.addAttr( mainCtrl.C, ln = at, at = 'enum', enumName = 'off:on', k = 1, dv= dfVal )
            mc.setAttr( mainCtrl.C + '.' + at, cb = 1 )
            mc.connectAttr( mainCtrl.C + '.' + at, obj + '.v' )
        
        # add rig display type connections

        for at, obj in zip( mainDispAts, mainObjList ):

            mc.addAttr( mainCtrl.C, ln = at, at = 'enum', enumName = 'normal:template:reference', k = 1, dv = 2 )
            mc.setAttr( mainCtrl.C + '.' + at, cb = 1 )
            mc.setAttr( obj + 'ove', 1 )
            mc.connectAttr( mainCtrl.C + '.' + at, obj + '.ovdt' )

    def _adjustMainCtrlShape( self, ctrl, scale ):

        # adjust shape of main control

        ctrlShapes = mc.listRelatives( ctrl.C, s = 1, type = 'nurbsCurve' )
        cls = mc.cluster( ctrlShapes )[1]
        mc.setAttr( cls + '.ry', 90 )
        mc.delete( ctrlShapes, ch = 1 )

        mc.move( 8 * scale, ctrl.Off, moveY = True, relative = True )

    def _flattenGlobalCtrlShape( self, ctrlObject ):

        # flatten ctrl object shape

        ctrlShapes = mc.listRelatives( ctrlObject, s = 1, type = 'nurbsCurve' )
        cls = mc.cluster( ctrlShapes )[1]
        mc.setAttr( cls + '.ry', 90 )
        mc.delete( ctrlShapes, ch = 1 )
    
class Module():

    """
    class for building module rig structure
    """

    def __init__(
                self,
                prefix = 'new',
                baseObj = None
                ):

        """
        @param prefix : str, prefix to name new objects
        @param baseObj : instance of base.module.Base class
        @return : None
        """

        self.topGrp = mc.group( n = prefix + '_Module_GRP', em = 1 )

        self.controlsGrp = mc.group( n = prefix + '_Controls_GRP', em = 1, p = self.topGrp )
        self.jointsGrp = mc.group( n = prefix + '_Joints_GRP', em = 1, p = self.topGrp )
        self.partsGrp = mc.group( n = prefix + '_Parts_GRP', em = 1, p = self.topGrp )
        self.partsNoTransGrp = mc.group( n = prefix + '_PartsNoTrans_GRP', em = 1, p = self.topGrp )

        mc.hide (self.partsGrp, self.partsNoTransGrp )

        mc.setAttr( self.partsNoTransGrp + '.it', 0, l = 1 )

        # parent module

        if baseObj:

            mc.parent( self.topGrp, baseObj.modulesGrp )


        

        
