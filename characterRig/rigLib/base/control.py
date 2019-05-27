"""
module for making rig control
"""

import maya.cmds as mc 

class Control():

    """ class for building controls """
    
    def _init_(
                self,
                prefix = 'new',
                scale = 1.0,
                translateTo = '',
                rotateTo = '',
                parent = '',
                shape = 'circle',
                lockChannels = [ 's', 'v' ]
                ):

        """
        @param prefix : str, prefix to name new objects
        @param scale : float, scale value for size of control shape
        @param translateTo : str, reference object for control position
        @param rotateTo : str, reference object for control rotation
        @param parent : str, object to be parent of control
        @param shape : str, control shape type
        @lockChannels : list( str ), list of channels to be locked and non-keyable
        @return : None
        """
            
        ctrlObject = None
        circleNormal = [ 1, 0, 0 ]
        
        if shape in [ 'circle', 'circleX' ]:
            
            circleNormal = [ 1, 0, 0 ]
            
        elif shape in [ 'circleY' ]:

            circleNormal = [ 0, 1, 0 ]
        
        elif shape in [ 'circleZ' ]:

            circleNormal = [ 0, 0, 1 ]
        
        elif shape in [ 'sphere' ]:

            ctrlObject = mc.circle ( n = prefix + '_CTRL1', ch = False, radius = scale, normal = [ 1, 0, 0 ] )[0]
            addShape = mc.circle ( n = prefix + '_CTRL2', ch = False, radius = scale, normal = [ 0, 1, 0 ] )[0]
            mc.parent ( mc.listRelatives ( addShape, s = 1 ), ctrlObject, r = 1, s = 1 )
            mc.delete( addShape )
            
        if not ctrlObject:

            mc.circle ( n = prefix + '_CTRL', ch = False, radius = scale, normal = circleNormal )[0]

        ctrlOffset = mc.group( n = prefix + '_offset_GRP', em = 1 )
        mc.parent( ctrlObject, ctrlOffset )

        # control color

        ctrlShapes = mc.listRelatives( ctrlObject, s = 1 )
        [ mc.setAttr( s + '.ove', 1 ) for s in ctrlShapes ]

        if prefix.startswith( 'l_' ):

            [ mc.setAttr( s + '.ovc', 6 ) for s in ctrlShapes ]
            
        elif prefix.startswith( 'r_' ):

            [ mc.setAttr( s + '.ovc', 13 ) for s in ctrlShapes ]
            
        else:

            [ mc.setAttr( s + '.ovc', 22 ) for s in ctrlShapes ]
            
        # translateTo

        if mc.objExists( translateTo ):

            mc.delete( mc.pointContraint( translateTo, ctrlOffset ) )

        # rotateTo 

        if mc.objExists( rotateTo ):

            mc.delete( mc.orientContraint( rotateTo, ctrlObject ) )

        # parent control

        if mc.objExists( parent ):

            mc.delete( mc.parent( ctrlOffset, parent ) )
            
        # lock control channels

        singleAttrLockList = []

        for lockChannel in lockChannels:

            if lockChannel in [ 't', 'r', 's' ]:

                for axis in [ 'x', 'y', 'z' ]:

                    at = lockChannel + axis
                    singleAttrLockList.append( at )
                
            else:

                singleAttrLockList.append( lockChannel )
                
        for at in singleAttrLockList:

            mc.setAttr( ctrlObject + '.' + at, l = 1, k = 0 )

        # add public members

        self.C = ctrlObject
        self.Off = ctrlOffset
                    