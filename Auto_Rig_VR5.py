import maya.cmds as cmds
#import maya.mel as mel
Loclist=[]
TheJoint=[]
############Window UI

WinName = 'ArmRig'
if cmds.window(WinName, q=True, exists=True):
    cmds.deleteUI(WinName)
   
   
cmds.window(WinName)
cmds.columnLayout()
cmds.text('Arm rigging Tool')
cmds.text('Before anything make sure your model is aimin at positive Z')
MakeLocators=cmds.button(l='make Locators',en=True,c='LocatorPivot()')
#saveLBtn=cmds.button(l='Save Positions',en=False,c='saveLoc()')
ResetLBtn=cmds.button(l='Undo Locators', en=True,c='ResetLoc()')
msg002=cmds.text('now click on create joints')
MakeJointBtn=cmds.button(l='make joints',en=True,c='MakeJoints()')
MakeIKBtn=cmds.button(l='make IK',en=True,c='Hierarchy(), Ikmaker()')
MakeFKBtn=cmds.button(l='make FK',en=True,c='FKMaker()')


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
        TheJoint=cmds.joint(n='Arm%s' %i)
        Thelocator=i
        cmds.matchTransform(TheJoint,Thelocator,pos=True)


        

       
        #print (TheJoint)
       


#print(Loclist.count-1)
       
       

    
    
def orderjnts():
    sel=cmds.ls(sl=True, type='transform')
    for each in sel:
        cmds.setAttr('.rotateOrder',e=True, k=True)
   
   
   
def Ikmaker():
    IKSelec=cmds.ls(sl=True)
    #ClearSelec=cmds.select(cl=True)
    print (IKSelec)
    #print (ClearSelec)
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
        cmds.setAttr(item + '.radius',e=True,k=True)
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
    children_joints = cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(children_joints, add=True)
    jnts=cmds.ls(sl=True,type='joint')
    for i in range(len(jnts)):
        boxCTRL()
        ctrl_node=cmds.ls(sl=True,type='transform')[0]
        #Align translation and rotation using parent contraint
        cmds.delete(cmds.parentConstraint(jnts[i],ctrl_node))
        #Split "_Jnt" from joint name
        jnt_id=jnts[i].split('_Jnt')
        print (jnt_id)
        #Rename box curve to chosen name of control
        ctrl= cmds.rename(ctrl_node, 'Arm_fk_CTRL' + jnt_id[1])
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
    xfos = cmds.listRelatives(crvs, allDescendents=True,p=True, typ="transform")
    print (xfos)
    cmds.select(xfos)
    for x in range(1,len(xfos)):
        cmds.parentConstraint(xfos[x+1],  (xfos[x] +  '_world'),mo=True)
        cmds.setKeyframe((xfos[x] +  '_world'), at=['translate','rotate'])
        cmds.connectAttr(xfos[x] + '.parent', (xfos[x] +  '_world.blendParent1'),f=True)
        
        
        
def parentCTRL():
    cmds.select(cl=True )
    crvs = cmds.ls(typ='nurbsCurve', ni=True, o=True, r=True)
    print (crvs)
    xfos = cmds.listRelatives(crvs,p=True, typ="transform")
    print (xfos)
    cmds.select(xfos[0])
    for x in range(1,len(crvs)):
        cmds.parentConstraint(xfos[x+1], (xfos[x] +  '_world'),mo=True)
        cmds.setKeyframe((xfos[x] +  '_world'), at=['translate','rotate'])
        cmds.connectAttr(xfos[x] + '.parent', (xfos[x] +  '_world.blendParent1'),f=True)
