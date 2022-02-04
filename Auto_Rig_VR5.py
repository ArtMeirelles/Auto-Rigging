''' Made by Arthur Cury Meirelles
The goal is to make an Auto rigging for vehicle
Made for my studies at BCIT for the Technical Atist course
my e-mail is: arthurcurymeirelles@hotmail.com'''

import maya.cmds as cmds


Name_User="JointName"
Loclist=[]
TheJoint=[]
############Window UI

WinName = 'Auto' +'_IK_' +'FK'
if cmds.window(WinName, q=True, exists=True):
    cmds.deleteUI(WinName)
   
   
cmds.window(WinName,s=False,h=230,w=390,bgc=(0.2,0.2,0.2))
cmds.columnLayout(adj=False,h=230,w=390)
cmds.text('Arm rigging Tool')
msg001=cmds.text('Before anything make sure your model is aimin at positive Z')
msg001=cmds.text('Locators goes to pivot position of meshes that you select')
cmds.rowLayout(adj=2,nc=2)
MakeLocators=cmds.button(l='make Locators',en=True,c='LocatorPivot()')
ResetLBtn=cmds.button(l='Undo Locators', en=True,c='ResetLoc()')
cmds.setParent('..')
cmds.separator(w=550,h=20)
msg002=cmds.text('Always change the name before creating a new chain of joints!CONFIRM NAME!')
cmds.rowLayout(adj=1,nc=2)
Joint_Name = cmds.textFieldGrp(l="Name for the joints: ",tx="JointsName", cc="Name_User = cmds.textFieldGrp(Joint_Name, q=1, tx=1)")
Confirm_Name=cmds.button(l='Confirm Name',en=True,c='Name_User = cmds.textFieldGrp(Joint_Name, q=1, tx=1)')
cmds.setParent('..')
cmds.separator(w=550,h=20)
msg003=cmds.text('Create Joints')
cmds.rowLayout(adj=1,nc=3)
MakeJointBtn=cmds.button(l='make joints',en=True,c='MakeJoints()')
AxisJnts=cmds.button(l='show axis joints',en=True,c='setAxisDisplay(display=True)')
HideAxisJnts=cmds.button(l='hide axis joints',en=True,c='setAxisDisplay(display=False)')
cmds.setParent('..')
cmds.separator(w=550,h=20)
msg004=cmds.text('Choose between IK/FK')
cmds.rowLayout(adj=1,nc=2)
MakeIKBtn=cmds.button(l='make IK',en=True,c='Hierarchy(), Ikmaker()')
MakeFKBtn=cmds.button(l='make FK',en=True,c='FKMaker()')
cmds.setParent('..')
cmds.separator(w=550,h=20)
msg005=cmds.text('After you create the joints, you can press "Undo Locators", so you can make another chain of joints')


cmds.showWindow()


#Funcations

#Make locators
def LocatorPivot():
    sel = cmds.ls(sl = True)
    for obj in sel:
            newLoc = cmds.spaceLocator(n='_Jnt_%s' %i)
            newCon = cmds.parentConstraint(obj, newLoc, mo = 0)
            Loclist.append(newLoc[0])
            cmds.delete(newCon)


def Name_Joints():
    cmds.textFieldGrp(l="Name for the joints: ",tx="JointsName", cc="Name_User = cmds.textFieldGrp(Joint_Name, q=1, tx=1)")
       
#Undo Locators

def ResetLoc():
    global Loclist
    cmds.select(Loclist)
    cmds.delete()
    Loclist=[]
    
    
       
def saveLoc():
    global locLocation
    cmds.button(MakeJointBtn,edit=True,en=True)
    locLocation=[]
    for i in Loclist:
        locXYZ=cmds.getAttr(i+'.wp')
        locLocation.append(locXYZ[0])
       
        print (Loclist)
        print (locLocation)
        return locLocation
   
       
       
       
#this functions create joints where the locators are placed

def MakeJoints():
    cmds.select(cl=True)
    for i in Loclist:
        TheJoint=cmds.joint(n=Name_User + '%s' %i)
        sel=cmds.ls(sl=True, type='joint')
        cmds.select(sel)
        print (sel)
        Thelocator=i
        cmds.matchTransform(TheJoint,Thelocator,pos=True)



        
def setAxisDisplay(display=True):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    # if no joints are selected, do it for all the joints in the scene
    if len(cmds.ls(sl=1, type="joint")) == 0:
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    # set the displayLocalAxis attribute to what the user specifies.
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display)

        
def setAxisDisplay(display=False):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    # if no joints are selected, do it for all the joints in the scene
    if len(cmds.ls(sl=1, type="joint")) == 0:
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    # set the displayLocalAxis attribute to what the user specifies.
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display)
       
    
       
    
    
def orderjnts():
    sel=cmds.ls(sl=True, type='transform')
    for each in sel:
        cmds.setAttr('.rotateOrder',e=True, k=True)
   
   
   
def Ikmaker():
    IKSelec=cmds.ls(sl=True)
    print (IKSelec)
    last_jnt = cmds.listRelatives(allDescendents=True, type='joint')[1]
    rp_IK=cmds.ikHandle( sol='ikRPsolver', sj=(IKSelec[0]), ee=(last_jnt))
    rp= cmds.rename(rp_IK[0],('End_IK'))
    #eff= cmds.rename(IKSelec[len(IKSelec)-2],('Start_IK'))
    


def Hierarchy():
    children_joints = cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(children_joints, add=True)
   

   
   
def boxCTRL():
    cmds.curve(n='Box_CTRL',d=1, p=[(1,-1,1), (-1,-1,1), (-1,-1,-1), (1,-1,-1),(1,-1,1),(1,1,1), (-1,1,1),(-1,-1,1),(-1,1,1), (-1,1,-1),(-1,-1,-1),(-1,1,-1), (1,1,-1),(1,-1,-1),(1,1,-1),(1,1,1)])


def resize():
    items=cmds.ls(sl=True,type='transform')
    for item in items:
        cmds.select(item + '.cv[0:*]',r=True)
        cl=cmds.cluster()
        cl_resize=cmds.rename(cl[1],item + '_resize')
        cmds.addAttr(item, ln='radius', at='double',min=0,dv=1)
        cmds.setAttr(item + '.radius',e=True,k=False, channelBox=True)
        rad=item + '.radius'
        cmds.connectAttr(rad,cl_resize + '.sx', f=True)
        cmds.connectAttr(rad,cl_resize + '.sy', f=True)
        cmds.connectAttr(rad,cl_resize + '.sz', f=True)
        cmds.setAttr(cl_resize + '.visibility', 0)
        cmds.select(cl=True)
        
        
def grouping():
    sel=cmds.ls(sl=True,type='transform')
    for each in sel:
        offset_f = cmds.group(n=each + '_offset', em=True)
        world  = cmds.group(n=each + '_world')
        cmds.delete(cmds.parentConstraint(each,world))
        getParents=cmds.listRelatives(each, p=True)
        if getParents:
            cmds.parent(world, getParents[0])
        cmds.parent(each, offset_f)
        


def FKMaker():
    #here we select just the joints with hierarchy
    #and store selection of joints olnly in variable "jnts"
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    jnts=cmds.ls(sl=True,type='joint')
    for i in range(len(jnts)):
        boxCTRL()
        ctrl_node=cmds.ls(sl=True,type='transform')
        #Align translation and rotation using parent contraint
        cmds.delete(cmds.parentConstraint(jnts[i],ctrl_node))
        #Split "_Jnt" from joint name
        jnt_id=jnts[i].split('_Jnt')
        print (jnt_id)
        #Rename box curve to chosen name of control
        ctrl= cmds.rename(ctrl_node, Name_User + '_fk_CTRL' + jnt_id[1])
        cmds.select(ctrl, r=True)
        orderjnts()
        resize()
        cmds.select(ctrl, r=True)
        grouping()
        cmds.parentConstraint(ctrl, jnts[i])
        cmds.connectAttr(ctrl + '.scale',jnts[i] + '.scale',f=True)
        cmds.setAttr(ctrl + '.sx',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sy',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sz',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.visibility',e=True,l=True,k=False)
        #Dynamic parenting
        cmds.addAttr(ctrl,ln='parent',min=0,max=1,dv=1)
        cmds.setAttr(ctrl + '.parent',e=True, k=True)
    cmds.select(cl=True )
    for each in jnts:
        jnt_id = each.split('_Jnt')[0]
        cmds.select(jnt_id + '_Jnt_%s' %i, tgl=True )
    crvs = cmds.ls(typ='nurbsCurve', ni=True, o=True, r=True)
    print (crvs)
    xfos = cmds.listRelatives(crvs,p=True, typ="transform")
    print (xfos)
    cmds.select(xfos)
    for x in range(1,len(xfos)):
        cmds.parentConstraint(xfos[x-1],  (xfos[x] +  '_world'),mo=True)
        cmds.setKeyframe((xfos[x] +  '_world'), at=['translate','rotate'])
        cmds.connectAttr(xfos[x] + '.parent', (xfos[x] +  '_world.blendParent1'),f=True)
        
        
        
        

def IKFunction():
    objs=cmds.ls(sl=True,type='transform')
    for obj in objs:
        boxCTRL()
        ctrl_node=cmds.ls(sl=True,type='transform')
        #Align translation and rotation using parent contraint
        cmds.delete(cmds.parentConstraint(obj,ctrl_node))
        #Split "_Jnt" from joint name
        jnt_id=obj.split('_Jnt')
        print (jnt_id)
        #Rename box curve to chosen name of control
        ctrl= cmds.rename(ctrl_node, Name_User + jnt_id[0] + '_ik_CTRL' )
        cmds.select(ctrl, r=True)
        orderjnts()
        resize()
        cmds.select(ctrl, r=True)
        grouping()
        cmds.parent(obj,ctrl)
        cmds.setAttr(ctrl + '.sx',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sy',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sz',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.visibility',e=True,l=True,k=False)
        
        
def IK_pv_Function():
    objs=cmds.ls(sl=True,type='transform')
    for obj in objs:
        boxCTRL()
        ctrl_node=cmds.ls(sl=True,type='transform')
        #Align translation and rotation using parent contraint
        cmds.delete(cmds.parentConstraint(obj,ctrl_node))
        #Split "_Jnt" from joint name
        jnt_id=obj.split('_Jnt')
        print (jnt_id)
        #Rename box curve to chosen name of control
        ctrl= cmds.rename(ctrl_node, Name_User + jnt_id[0] + '_pv_CTRL' )
        cmds.select(ctrl, r=True)
        orderjnts()
        resize()
        cmds.select(ctrl, r=True)
        grouping()
        #rotation and scale
        cmds.setAttr(ctrl + '.rx',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.ry',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.rz',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sx',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sy',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.sz',e=True,l=True,k=False)
        cmds.setAttr(ctrl + '.visibility',e=True,l=True,k=False)
        
        
#Resize function in nurbs channels
def resize_circle():
    objs=cmds.ls(sl=True,type='transform')
    for obj in objs:
        cmds.addAttr(obj, ln='radius', at='double',min=0,dv=1)
        cmds.setAttr(obj + '.radius',e=True,k=False, channelBox=True)
        cmds.connectAttr((obj + '.radius'),(obj + '_attrs.radius'), f=True)
        
        
#Lock channels and making sure they are not keyable
def lockXformCH ():
    objs=cmds.ls(sl=True,type='transform')
    for obj in objs:
        cmds.setAttr(obj + '.tx',e=True,l=True,k=False)
        cmds.setAttr(obj + '.ty',e=True,l=True,k=False)
        cmds.setAttr(obj + '.tz',e=True,l=True,k=False)
        cmds.setAttr(obj + '.rx',e=True,l=True,k=False)
        cmds.setAttr(obj + '.ry',e=True,l=True,k=False)
        cmds.setAttr(obj + '.rz',e=True,l=True,k=False)
        cmds.setAttr(obj + '.sx',e=True,l=True,k=False)
        cmds.setAttr(obj + '.sy',e=True,l=True,k=False)
        cmds.setAttr(obj + '.sz',e=True,l=True,k=False)
        
#hide shape nodes
def hideshapes():
    objs=cmds.ls(sl=True,type='transform')
    for obj in objs:
        shapes=cmds.listRelatives(obj, type='shape')[0]
        for shape in shapes:
            cmds.setAttr(shape + '.visibility', 0)
            
            
