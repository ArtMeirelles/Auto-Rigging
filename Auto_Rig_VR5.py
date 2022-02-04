'''
Made by Arthur Cury Meirelles
The goal is to make an Auto rigging for vehicle
Made for my studies at BCIT during Technical Artist course.

Contact:
    arthurcurymeirelles@hotmail.com
    https://www.linkedin.com/in/arthurm3d
'''

import maya.cmds as cmds

# General Vars

name_user="JointsName"
loc_list=[]
the_joint=[]

    ### Auto Rig Functions ###
    
    # Make Locators
def locator_pivot():
    cmds.ls(sl=True,type='transform')
    if len(cmds.ls(sl=1, type="transform")) == 0:  # Make sure that user select something
        cmds.warning('Please, first select something!')
    else:
        sel = cmds.ls(sl = True)
        for obj in sel:
                newLoc = cmds.spaceLocator(n='_Jnt_%s' %i)
                newCon = cmds.parentConstraint(obj, newLoc, mo = 0)
                loc_list.append(newLoc[0])
                cmds.delete(newCon)
       
    # Undo Locators
def reset_locator():
    global loc_list
    cmds.select(loc_list)
    cmds.delete()
    loc_list=[]
    
    # Save Locators Position
def save_locators():
    global loc_locations
    cmds.button(make_joint_btn,edit=True,en=True)
    loc_locations = []
    for i in loc_list:
        locXYZ=cmds.getAttr(i+'.wp')
        loc_locations.append(locXYZ[0])
       
        print (loc_list)
        print (loc_locations)
        return loc_locations
   
    # Functions to create joints where the locators are placed
def make_joints():
    cmds.select(cl=True)
    for i in loc_list:
        the_joint = cmds.joint(n=name_user + '%s' %i)
        sel = cmds.ls(sl=True, type='joint')
        cmds.select(sel)
        print (sel)
        Thelocator=i
        cmds.matchTransform(the_joint,Thelocator,pos=True)

    # Show Axis for Joints
def show_axis_display(display=True):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.

    # Hide Axis for Joints
def hide_axis_display(display=False):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.
       
def order_joints():
    sel = cmds.ls(sl=True, type='transform')
    for each in sel:
        cmds.setAttr('.rotateOrder',e=True, k=True)
   
def ik_maker():
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0:  # Make sure that user select the root joints
        cmds.warning('Please, first select the root joint!')
    else:
        IKSelec=cmds.ls(sl=True)
        print (IKSelec)
        last_jnt = cmds.listRelatives(allDescendents=True, type='joint')[1]
        rp_IK = cmds.ikHandle( sol='ikRPsolver', sj=(IKSelec[0]), ee=(last_jnt))
        rp = cmds.rename(rp_IK[0],('End_IK'))
        #eff= cmds.rename(IKSelec[len(IKSelec)-2],('Start_IK'))
    
def hierarchy_func():
    children_joints = cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(children_joints, add=True)
   
def box_curve_ctrl():
    cmds.curve(n='Box_CTRL', d=1, p=[(1,-1,1), (-1,-1,1),
    (-1,-1,-1), (1,-1,-1),
    (1,-1,1), (1,1,1), (-1,1,1),
    (-1,-1,1), (-1,1,1), (-1,1,-1),
    (-1,-1,-1), (-1,1,-1), (1,1,-1),
    (1,-1,-1), (1,1,-1), (1,1,1)]
    )

def resize():
    items = cmds.ls(sl=True,type='transform')
    for item in items:
        cmds.select(item + '.cv[0:*]', r=True)
        cl = cmds.cluster()
        cl_resize = cmds.rename(cl[1],item + '_resize')
        cmds.addAttr(item, ln='radius', at='double', min=0, dv=1)
        cmds.setAttr(item + '.radius', e=True, k=False, channelBox=True)
        rad = item + '.radius'
        cmds.connectAttr(rad,cl_resize + '.sx', f=True)
        cmds.connectAttr(rad,cl_resize + '.sy', f=True)
        cmds.connectAttr(rad,cl_resize + '.sz', f=True)
        cmds.setAttr(cl_resize + '.visibility', 0)
        cmds.select(cl=True)
            
def grouping():
    sel = cmds.ls(sl=True,type='transform')
    for each in sel:
        offset_f = cmds.group(n=each + '_offset', em=True)
        world  = cmds.group(n=each + '_grp')
        cmds.delete(cmds.parentConstraint(each, world))
        getParents=cmds.listRelatives(each, p=True)
        if getParents:
            cmds.parent(world, getParents[0])
        cmds.parent(each, offset_f)
        
def fk_maker():
    if len(cmds.ls(sl=1, type="joint")) == 0:  # Make sure that user select the root joints
        cmds.warning('Please, first select the root joint!')
    else:
        cmds.listRelatives(allDescendents=True, type='joint') # Here we select just the joints with hierarchy
        cmds.select(hi=True, add=True) # Store selection of joints olnly in variable "jnts"
        jnts = cmds.ls(sl=True, type='joint')
        for i in range(len(jnts)):
            box_curve_ctrl()
            ctrl_node = cmds.ls(sl=True,type='transform')
            cmds.delete(cmds.parentConstraint(jnts[i], ctrl_node)) # Align translation and rotation using parent contraint
            jnt_id = jnts[i].split('_Jnt')# Split "_Jnt" from joint name
            print (jnt_id)
            ctrl = cmds.rename(ctrl_node, name_user + '_fk_CTRL' + jnt_id[1]) # Rename box curve to chosen name of control
            cmds.select(ctrl, r=True)
            order_joints()
            resize()
            cmds.select(ctrl, r=True)
            grouping()
            cmds.parentConstraint(ctrl, jnts[i])
            cmds.connectAttr(ctrl + '.scale', jnts[i] + '.scale', f=True)
            cmds.setAttr(ctrl + '.sx', e=True, l=True, k=False)
            cmds.setAttr(ctrl + '.sy', e=True, l=True, k=False)
            cmds.setAttr(ctrl + '.sz', e=True, l=True, k=False)
            cmds.setAttr(ctrl + '.visibility', e=True, l=True, k=False)
            cmds.addAttr(ctrl,ln='parent', min=0, max=1, dv=1) # Here we start the dynamic parenting
            cmds.setAttr(ctrl + '.parent', e=True, k=True)
        cmds.select(cl=True )
        for each in jnts:
            jnt_id = each.split('_Jnt')[0]
            cmds.select(jnt_id + '_Jnt_%s' %i, tgl=True )
        crvs = cmds.ls(typ='nurbsCurve', ni=True, o=True, r=True)
        print (crvs)
        xfos = cmds.listRelatives(crvs, p=True, type="transform")
        print (xfos)
        cmds.select(xfos)
        for x in range(1,len(xfos)):
            cmds.parentConstraint(xfos[x-1], (xfos[x] +  '_grp'), mo=True)
            cmds.setKeyframe((xfos[x] +  '_grp'), at=['translate','rotate'])
            cmds.connectAttr(xfos[x] + '.parent', (xfos[x] +  '_grp.blendParent1'), f=True)
            
    def ik_function():
        objs = cmds.ls(sl=True, type='transform')
        for obj in objs:
            box_curve_ctrl()
            ctrl_node = cmds.ls(sl=True, type='transform')
            cmds.delete(cmds.parentConstraint(obj, ctrl_node)) # Align translation and rotation using parent contraint
            jnt_id=obj.split('_Jnt') # Split "_Jnt" from joint name
            print (jnt_id)
            ctrl = cmds.rename(ctrl_node, name_user + jnt_id[0] + '_ik_CTRL' ) # Rename box curve to chosen name of control
            cmds.select(ctrl, replace=True)
            order_joints()
            resize()
            cmds.select(ctrl, replace=True)
            grouping()
            cmds.parent(obj,ctrl)
            cmds.setAttr(ctrl + '.sx', edit=True, lock=True, keyable=False)
            cmds.setAttr(ctrl + '.sy', edit=True, lock=True, keyable=False)
            cmds.setAttr(ctrl + '.sz', edit=True, lock=True, keyable=False)
            cmds.setAttr(ctrl + '.visibility', edit=True, lock=True,keyable=False)
            
def ik_pv_function():
    objs = cmds.ls(selection=True, type='transform')
    for obj in objs:
        box_curve_ctrl()
        ctrl_node = cmds.ls(selection=True, type='transform')
        cmds.delete(cmds.parentConstraint(obj, ctrl_node)) # Align translation and rotation using parent contraint
        jnt_id = obj.split('_Jnt') # Split "_Jnt" from joint name
        print (jnt_id)
        ctrl = cmds.rename(ctrl_node, name_user + jnt_id[0] + '_pv_CTRL' ) # Rename box curve to chosen name of control
        cmds.select(ctrl, r=True)
        order_joints()
        resize()
        cmds.select(ctrl, r=True)
        grouping()
        cmds.setAttr(ctrl + '.rx', edit=True, lock=True, keyable=False) # Rotation and scale
        cmds.setAttr(ctrl + '.ry', edit=True, lock=True, keyable=False)
        cmds.setAttr(ctrl + '.rz', edit=True, lock=True, keyable=False)
        cmds.setAttr(ctrl + '.sx', edit=True, lock=True, keyable=False)
        cmds.setAttr(ctrl + '.sy', edit=True, lock=True, keyable=False)
        cmds.setAttr(ctrl + '.sz', edit=True, lock=True, keyable=False)
        cmds.setAttr(ctrl + '.visibility', edit=True, lock=True, keyable=False)
            
    # Resize function in nurbs channels
def resize_circle():
    objs = cmds.ls(selection=True, type='transform')
    for obj in objs:
        cmds.addAttr(obj, longName='radius', attributeType='double', min=0, defaultValue=1)
        cmds.setAttr(obj + '.radius', edit=True, keyable=False, channelBox=True)
        cmds.connectAttr((obj + '.radius'), (obj + '_attrs.radius'), force=True)
        
    # Lock channels and making sure they are not keyable
def lock_xform_channel():
    objs = cmds.ls(selection=True, type='transform')
    for obj in objs:
        cmds.setAttr(obj + '.tx', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.ty', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.tz', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.rx', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.ry', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.rz', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.sx', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.sy', edit=True, lock=True, keyable=False)
        cmds.setAttr(obj + '.sz', edit=True, lock=True, keyable=False)
              
    # Lock channels and making sure they are not keyable
def hideshapes():
    objs = cmds.ls(selection=True,type='transform')
    for obj in objs:
        shapes=cmds.listRelatives(obj, type='shape')[0]
        for shape in shapes:
            cmds.setAttr(shape + '.visibility', 0)
            
    
    ### Window UI ###
win_name = 'Auto' +'_IK_' +'FK'
if cmds.window(win_name, query=True, exists=True):
    cmds.deleteUI(win_name)
   
cmds.window(win_name, sizeable=False, height=350, width=460, backgroundColor=(0.2,0.2,0.2))
cmds.columnLayout(adjustableColumn=False)

# Button for Locators
cmds.text('Arm rigging Tool')
msg_001 = cmds.text('Before anything make sure your model is aimin at positive Z')
msg_002 = cmds.text('Locators goes to pivot position of meshes that you select')
cmds.rowLayout(adjustableColumn=2, numberOfColumns=2)
make_locators = cmds.button(label='make Locators', enable=True, command='locator_pivot()')
reset_loc_btn = cmds.button(label='Undo Locators', enable=True, command='reset_locator()')
cmds.setParent('..')

# Button to name joints
cmds.separator(width=550, height=20)
msg_003 = cmds.text('Always change the name before creating a new chain of joints!CONFIRM NAME!')
cmds.rowLayout(adjustableColumn=1, numberOfColumns=2)
joint_name = cmds.textFieldGrp(label="Name for the joints: ", text="JointsName",
cc="name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)"
)
confirm_name = cmds.button(label='Confirm Name', enable=True, command='name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)')
cmds.setParent('..')

# Button to create joints
cmds.separator(width=550, height=20)
msg_004 = cmds.text('Create Joints')
cmds.rowLayout(adjustableColumn=1, numberOfColumns=3)
make_joint_btn = cmds.button(l='make joints', enable=True,c='make_joints()')
show_axis_joints = cmds.button(label='show axis joints', enable=True, command='show_axis_display(display=True)')
hide_axis_joints = cmds.button(label='hide axis joints', enable=True, command='hide_axis_display(display=False)')
cmds.setParent('..')

# Button for IK/FK
cmds.separator(width=550, height=20)
msg_005 = cmds.text('Choose between IK/FK')
cmds.rowLayout(adjustableColumn=1, numberOfColumns=2)
MAKE_IK_BTN = cmds.button(label='make IK', enable=True, command='hierarchy_func(), ik_maker()')
MAKE_FK_BTN = cmds.button(label='make FK', enable=True, command='fk_maker()')
cmds.setParent('..')
cmds.separator(width=550, height=20)
msg_006 = cmds.text('After you create the joints, you can press "Undo Locators", so you can make another chain of joints')

cmds.showWindow()
