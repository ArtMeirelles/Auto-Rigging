'''
Made by Arthur Cury Meirelles
The goal is to make an Auto rigging for vehicle
Made for my studies at BCIT during Technical Artist course.

Contact:
    arthurcurymeirelles@hotmail.com
    https://www.linkedin.com/in/arthurm3d
'''

import maya.cmds as cmds
import maya.mel as mel

# General Vars
name_user="JointsName"
NewJointName = 'JointsN'
loc_list=[]
the_joint=[]
i=[]
to_rename = []
first_run = True
in_joint_made = False
out_joint_made = False
window_maker = []
updated_index = 0
vehicle_GRP = []
wheel_ctrl = []
global_CTRL = []

    ### Auto Rig Functions ###
    
    # Make Locators
def locator_pivot():
    cmds.ls(sl=True,type='transform')
    if len(cmds.ls(sl=1, type="transform")) == 0:  
        cmds.warning('Please, first select something!')
    else:
        sel = cmds.ls(sl = True)
        for obj in sel:
                newLoc = cmds.spaceLocator(n='_Jnt'%i+'+1')
                newCon = cmds.parentConstraint(obj, newLoc, mo = 0)
                loc_list.append(newLoc[0])
                cmds.delete(newCon)

    # Undo Locators
def delete_locators():
    global loc_list
    cmds.select(loc_list)
    loc_list=[]
    cmds.select(cl=True)
    if cmds.objExists('_Jnt*')!=True:
        pass
    else:
        loc_lis = cmds.ls(sl=True, type='transform')
        loc_d = cmds.select('_Jnt*')
        cmds.delete()
          
    # Functions to create joints where the locators are placed
def make_joints():
        if cmds.objExists('_Jnt*')!=True:
            cmds.warning('Please, first create the locators')
        else:
            cmds.select(cl=True)
            for i in loc_list:
                the_joint = cmds.joint(n=name_user + '%s' %i + '_skin', rotationOrder = "xyz")
                sel = cmds.ls(sl=True, type='joint')
                cmds.select(sel)
                print (sel)
                Thelocator=i
                cmds.matchTransform(the_joint,Thelocator,pos=True)
            else:
                cmds.select(cl=True)

    # Show Axis for Joints
def show_axis_display(display=True):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: 
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) 

    # Hide Axis for Joints
def hide_axis_display(display=False):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: 
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) 
       
def order_joints():
    sel = cmds.ls(sl=True, type='transform')
    for each in sel:
        cmds.setAttr('.rotateOrder',e=True, k=True)
   
def ik_maker():
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0:  
        cmds.warning('Please, first select the root joint!')
    else:
        IKSelec=cmds.ls(sl=True)
        print (IKSelec)
        last_jnt = cmds.listRelatives(allDescendents=True, type='joint')[1]
        rp_IK = cmds.ikHandle( sol='ikRPsolver', sj=(IKSelec[0]), ee=(last_jnt))
    
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
        cmds.parent(each)
        
def select_global_ctrl():
    cmds.select(cl=True)
    cmds.select(all=True)
    sel_global_ctrl = cmds.ls(sl=True, type="transform")
    cmds.select('global_CTRL')

def orient_joints():
        cmds.select(hi=True)
        joints_ori = cmds.ls(sl=True, type='joint')
        if len(joints_ori) ==0:  
            cmds.warning('Please, first select the root joint')
        else:
            cmds.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
            cmds.select(cl=True)
        
def fk_rg():
        jnts = cmds.ls(sl=True, type= 'joint')
        for i in range(len(jnts)):
            box_curve_ctrl()
            ctrl_node = cmds.ls(sl=True,type='transform')[0] 
            cmds.delete(cmds.parentConstraint(jnts[i], ctrl_node)) 
            jnt_id = jnts[i].split('_skin')
            print (jnt_id[0]) 
            ctrl = cmds.rename(ctrl_node, jnt_id[0] + '_CTRL') 
            cmds.select(ctrl, r=True) 
            order_joints()
            resize() 
            cmds.select(ctrl, r=True) 
            grouping()
            cmds.parentConstraint(ctrl, jnts[i]) 
            cmds.connectAttr(ctrl + '.scale', jnts[i] + '.scale', f=True) 
            axis_xyz = ['x','y','z']
            for axis in axis_xyz:
                cmds.setAttr(ctrl + '.s' + axis, e=True, l=True, k=False) 
            cmds.setAttr(ctrl + '.visibility', e=True, l=True, k=False) 
            cmds.addAttr(ctrl,ln='parent', min=0, max=1, dv=1) 
            cmds.setAttr(ctrl + '.parent', e=True, k=True) 
        cmds.select(cl=True ) 
        for each in jnts:
            jnt_id = each.split('_skin')[0] 
            cmds.select(jnt_id + '_CTRL', tgl=True ) 
        crvs = cmds.ls(sl=True, type='transform') 
        print (crvs)
        for x in range(1,len(crvs)): 
            cmds.parentConstraint(crvs[x-1], (crvs[x] +  '_grp'), mo=True) 
            cmds.setKeyframe((crvs[x] +  '_grp'), at=['translate','rotate']) 
            cmds.connectAttr(crvs[x] + '.parent', (crvs[x] +  '_grp.blendParent1'), f=True)

def ik_rg():
        objs = cmds.ls(sl=True, type= 'transform') 
        for obj in objs:
            box_curve_ctrl()
            ctrl_node = cmds.ls(sl=True,type='transform')[0] 
            cmds.delete(cmds.parentConstraint(obj, ctrl_node)) 
            jnt_id = obj.split('_skin')
            print (jnt_id[0]) 
            ctrl = cmds.rename(ctrl_node, jnt_id[0] + '_ik_CTRL') 
            cmds.select(ctrl, r=True) 
            order_joints()
            resize() 
            cmds.select(ctrl, r=True) 
            grouping()
            cmds.parent(obj)
            xyz = ['sx','sy','sz','visibility']
            for ctrls in ctrl:
                for axis in xyz:
                        cmds.setAttr(ctrl + '.' + axis, edit=True, lock=True, keyable=False)
            
    # Resize function in nurbs channels
def resize_circle():
    objs = cmds.ls(selection=True, type='transform')
    for obj in objs:
        cmds.addAttr(obj, longName='radius', attributeType='double', min=0, defaultValue=1)
        cmds.setAttr(obj + '.radius', edit=True, keyable=False, channelBox=True)
        cmds.connectAttr((obj + '.radius'), (obj + '_attrs.radius'), force=True) 
         
    # Lock channels 
def lock_xform_channel():
    objs = cmds.ls(selection=True, type='transform')
    trs = ['t','r','s']
    xyz = ['x','y','z']
    for obj in objs:
        for attr_trs in trs:
            for axis in xyz:
                cmds.setAttr(obj + '.'+ attr_trs + axis, edit=True, lock=True, keyable=False)
              
    # Lock channels 
def hideshapes(): 
    objs = cmds.ls(selection=True,type='transform')
    for obj in objs:
        shapes=cmds.listRelatives(obj, type='shape')[0]
        for shape in shapes:
            cmds.setAttr(shape + '.visibility', 0)
            
def string_replace(string, search, replace):
    if string == '':
        return ''
    replace_string = string.replace(search, replace)
    return replace_string
            
def get_short_name(obj):
    if obj == '':
        return ''
    split_path = obj.split('|')
    if len(split_path) >= 1:
        short_name = split_path[len(split_path)-1]
    return short_name
            
def rename_search_replace(obj_list, search, replace):
    for obj in obj_list:
        object_short_name = get_short_name(obj)
        new_name = string_replace(str(object_short_name), search, replace)
        if cmds.objExists(obj) and 'shape' not in cmds.nodeType(obj, inherited=True) and obj != new_name:
            to_rename.append([obj,new_name])
            
    for pair in reversed(to_rename):
        if cmds.objExists(pair[0]):
            cmds.rename(pair[0], pair[1])
     
def fk_ik_maker():
    jts = cmds.ls(selection=True, type='joint')
    if len(jts) !=1:  
        cmds.warning('Please, first select the root joint')
    else: 
        root_jnt = jts[0] 
        print (root_jnt)
        cmds.select(root_jnt, replace=True) 
        cmds.pickWalk(d='up') 
        prt_main = cmds.ls(selection=True, type='transform') 
        rad = cmds.getAttr(root_jnt + '.radius') 
        if cmds.objExists('vehicle_GRP')!=True: 
            cmds.group(n='vehicle_GRP', empty=True)
            cmds.select('vehicle_GRP', replace=True)
            lock_xform_channel()
        else:
            pass 
        if cmds.objExists('global_CTRL')!=True: 
            ctrl_node = cmds.circle(degree=1, sections=6, normal=[0,1,0])
            ctrl = cmds.rename(ctrl_node[0], 'global_CTRL') 
            ctrl_attrs = cmds.rename(ctrl_node[1], (ctrl + '_attrs')) 
            cmds.select(ctrl, r=True ) 
            resize_circle()
            order_joints()
            global_prt = cmds.listRelatives(ctrl, p=True)
            if global_prt:
                pass
            else:
                cmds.parent(ctrl, 'vehicle_GRP')
        else:
            pass 
        resizers = root_jnt + '_control_resize_grp' 
        skeleton = root_jnt + '_skeleton'
        controls = root_jnt + '_controls'
        global_ctrl = 'global_CTRL'
        if cmds.objExists(skeleton)!=True: 
            cmds.group(n=skeleton, empty=True)
            cmds.select(skeleton, replace=True)
            lock_xform_channel()
        else:
            pass
        if cmds.objExists(controls)!=True: 
            cmds.group(n=controls, empty=True)
            cmds.select(controls, replace=True)
            lock_xform_channel()
        else:
            pass
        if cmds.objExists(resizers)!=True: 
            cmds.group(n=resizers, empty=True)
            cmds.select(resizers, replace=True)
            lock_xform_channel()
        else:
            pass
        fkIK = root_jnt.split('_skin')[0] + '_fkIK' 
        cmds.addAttr(global_ctrl, longName=fkIK, attributeType='double', min=0, max=1, dv=1) 
        cmds.setAttr((global_ctrl + '.' + fkIK), e=True, k=True) 
        cmds.parent(skeleton, controls, global_ctrl)
        rad_offset = 1 
        rad_root = cmds.getAttr(root_jnt + '.radius')
        cmds.select(root_jnt, r=True)
        cmds.duplicate(rr=True) 
        root_fk_node = cmds.ls(sl=True, type='joint')[0]
        root_fk = cmds.rename(root_fk_node, (root_jnt.split('_skin')[0] + '_fk')) 
        cmds.select(hierarchy=True) 
        cmds.select(root_fk, tgl=True) 
        fk_chain = cmds.ls(sl=True, type='joint')
        for each_fk in fk_chain:
            cmds.setAttr(each_fk + '.radius', (rad_root + rad_offset)) 
        cmds.select(hi=True) 
        str_skin = '_skin'
        str_fk = '_fk'
        rename_search_replace(fk_chain, str_skin, str_fk)
        cmds.select(root_jnt, r=True)
        cmds.duplicate(rr=True)
        root_ik_node = cmds.ls(sl=True, type='joint')[0]
        root_ik = cmds.rename(root_ik_node, (root_jnt.split('_skin')[0] + '_ik'))
        cmds.select(root_ik, hi=True)
        ik_chain = cmds.ls(sl=True, type='joint')
        for each_ik in ik_chain:
            cmds.setAttr(each_ik + '.radius', (rad_root + rad_offset +1)) 
        cmds.select(hi=True)
        cmds.select(root_fk, tgl=True)
        str_skin = '_skin'
        str_ik = '_ik'
        rename_search_replace(ik_chain, str_skin, str_ik)
        renamed_root_ik = cmds.select(root_ik, hi=True)
        renamed_ik_chain = cmds.ls(sl=True, type='joint')
        print ('RENAMED:', renamed_ik_chain)
        cmds.select(root_jnt, hi=True) 
        chain = cmds.ls(sl=True, type='joint')
        size_chain = len(chain)
        cmds.select(chain[size_chain-1], tgl=True)
        main_chain = cmds.ls(sl=True, type='joint') 
        for each_main in main_chain: 
            jnt_prefix = each_main.split('_skin')[0] 
            rev = cmds.createNode('reverse', n=(jnt_prefix  + '_ik_rev')) 
            ik = jnt_prefix + '_ik'
            fk = jnt_prefix + '_fk'
            prtc = cmds.parentConstraint(fk, ik, each_main)[0] 
            cn_wgt = cmds.parentConstraint(prtc, q=True, wal=True) 
            fk_wgt = cn_wgt[0]
            ik_wgt = cn_wgt[1]
            cmds.connectAttr((global_ctrl + '.' + fkIK), (prtc + '.' + ik_wgt), f=True) 
            cmds.connectAttr((global_ctrl + '.' + fkIK), (rev + '.inputX'), f=True)
            cmds.connectAttr((rev + '.outputX'), (prtc + '.' + fk_wgt), f=True)
            cmds.setAttr((fk + '.visibility'),0) 
            cmds.setAttr((ik + '.visibility'),0)
        cmds.select(root_fk, hi=True)
        fk_skel = cmds.ls(sl=True, type='joint')
        size_fk_skel = len(fk_skel)
        cmds.select(fk_skel, r=True)
        cmds.select(fk_skel[size_fk_skel-1], tgl=True)
        fk_skel_ctrl = cmds.ls(sl=True, type='joint') 
        fk_rg()
        fkIk_chn = global_ctrl + '.' + fkIK
        rev_fk = cmds.createNode('reverse', n=(root_fk + '_rev')) 
        cmds.connectAttr(fkIk_chn, (rev_fk + '.inputX'), f=True)
        for each_fk_ctrl in fk_skel_ctrl: 
            cmds.parent((each_fk_ctrl + '_CTRL_grp', controls))
            cmds.parent((each_fk_ctrl + '_CTRL_resize', resizers))
            cmds.connectAttr((rev_fk + '.outputX'),(each_fk_ctrl + '_CTRL_grp.visibility'), f=True)  
        end_eff_ik = renamed_ik_chain[len(renamed_ik_chain)-1]
        cmds.select(root_ik, end_eff_ik, r=True) 
        ik_maker()
        ik_hdl = cmds.ls(sl=True, type='transform')[0]
        cmds.setAttr(ik_hdl + '.visibility', 0)
        cmds.select(ik_hdl, r=True) 
        ik_rg()  # create the ik control
        cmds.connectAttr(fkIk_chn, (ik_hdl + '_ik_CTRL_grp.visibility'), f=True) 
        cmds.parent((ik_hdl + '_ik_CTRL_grp'), controls)
        cmds.parent((ik_hdl + '_ik_CTRL_resize'), resizers)
        cmds.parent(resizers,  'vehicle_GRP')
        if prt_main[0]==root_jnt:
            cmds.parent(root_jnt,root_ik, root_fk, skeleton)
        else:
            pass
            
    #Tread Functions
def make_locator():
    global first_run
    make_locator.front_locator = cmds.spaceLocator(n = "CircleLocator_Front")
    cmds.scale(3,3,3)
    cmds.move(0,0,10, r = True)
    make_locator.back_locator = cmds.spaceLocator(n = "CircleLocator_Back")
    cmds.scale(3,3,3)
    
    #Only prompt for locator placement the first time the user runs the program
    if first_run == True:
        cmds.confirmDialog(title = "Locator Placement", message = "Place the Locators where you need.")
        first_run =  False
    cmds.button(window_maker.init_button, edit = True, enable = False)
    cmds.button(window_maker.reset_button, edit = True, enable = True)
    cmds.button(window_maker.curve_button, edit = True, visible = True, enable = True)

def reset_locator():
    #Delete Locators
    cmds.delete(make_locator.front_locator)
    cmds.delete(make_locator.back_locator)
    
    #Hide Buttons
    cmds.button(window_maker.init_button, edit = True, enable = True)
    cmds.button(window_maker.curve_button, edit = True, enable = False, visible = False)
    cmds.button(window_maker.reset_button, edit = True, enable = False)
    cmds.textFieldButtonGrp(window_maker.text_button, edit = True, enable = False, visible = False, text = "")
    cmds.intSliderGrp(window_maker.copies_slider, edit= True, visible= False, value=0)
    cmds.text(window_maker.text_tread, edit=True, visible=False)
    
    # If the user resets before the Curve gets created, just try to get it and ignore the Error
    try:
        cmds.delete(make_curve.tread_curve)
        cmds.delete(make_curve.locator_group)
        cmds.delete(numchange.new_polyobject)
    except AttributeError:
        pass
    except ValueError:
        pass
        
def make_curve():
    cmds.select(make_locator.front_locator)
    front_locator_position = cmds.getAttr(".translateZ")
    cmds.select(make_locator.back_locator)
    back_locator_position = cmds.getAttr(".translateZ")
    print(front_locator_position)
    print(back_locator_position)
    locator_distance = abs(front_locator_position-back_locator_position)
    print("Total Distance is %i" %locator_distance)
    curve_radius = locator_distance/2
    make_curve.tread_curve = cmds.circle(n = "TreadCurve", r = curve_radius, nr = (1, 0, 0))
    make_curve.locator_group = cmds.group(make_locator.front_locator, make_locator.back_locator, n = "Loc_Group")
    cmds.select(make_curve.tread_curve, r = True)
    cmds.select("Loc_Group", add = True)
    cmds.align(z = "mid", atl = True)
    cmds.select(make_curve.tread_curve)
    cmds.FreezeTransformations()
    cmds.textFieldButtonGrp(window_maker.text_button, edit = True, enable = True, visible = True)
    cmds.button(window_maker.curve_button, edit = True, enable = False, visible = False)
    cmds.select(clear=True)
    cmds.confirmDialog(title="Tread",message="Select an object to be the tread")
    #delete the values of selected_object

def pick_object():
    global selected_object
    selected_object = cmds.ls(sl = True)
        
    if len(selected_object) == 1:
        shapes=cmds.listRelatives(selected_object[0],shapes=True)
        if shapes:
            print(cmds.objectType(shapes[0]))
            if cmds.objectType(shapes[0],isType='mesh'):
                cmds.textFieldButtonGrp(window_maker.text_button, edit = True, text = selected_object[0])
                cmds.intSliderGrp(window_maker.copies_slider, edit= True, visible= True)
                cmds.text(window_maker.text_tread, edit=True, visible=True)
                return selected_object
            else:
                cmds.warning("Please Select an Object that has a mesh.")
    else:
        cmds.warning("Select 1 object")
        cmds.textFieldButtonGrp(window_maker.text_button, e = True, tx = "")
        
        
def numchange():
    if cmds.objExists("TreadFull"):
        cmds.delete("TreadFull")
    if cmds.objExists("_wire"):
        cmds.delete("_wire")
    
    global updateCopynum
    updateCopynum = cmds.intSliderGrp(window_maker.copies_slider, v = True, q = True)
    
    cmds.select(selected_object, r = True)
    cmds.select(make_curve.tread_curve, add = True)
    cmds.pathAnimation(
        f = True,
        fa = "z",
        ua= "y",
        wut = "vector",
        wu = (0,1,0),
        inverseFront = False,
        iu = False,
        b = False,
        stu = 1,
        etu = updateCopynum
        )
    cmds.select(selected_object, r = True)
    cmds.selectKey("motionPath1_uValue", time = (1, updateCopynum))
    cmds.keyTangent(itt = "linear", ott = "linear")
    cmds.snapshot(n = "TreadSS", i = 1, ch = False, st = 1, et = updateCopynum, u= "Animation Curve")
    cmds.DeleteMotionPaths()
    cmds.select("TreadSSGroup", r = True)
    numchange.new_polyobject = cmds.polyUnite(n = "TreadFull", ch = False)
    cmds.CenterPivot(numchange.new_polyobject)
    cmds.select("TreadSSGroup", r = True)
    cmds.delete()
    def create_wireDeformer(geo, wireCurve, dropoff_distance = 40):
        wire = cmds.wire(geo, w = wireCurve, n = "_wire")
        wire_node = wire[0]
        cmds.setAttr(wire_node+".dropoffDistance[0]", dropoff_distance)
    
    cmds.select("TreadFull")
    wireObj = cmds.ls(sl = True, o = True)[0]
    
    cmds.select(make_curve.tread_curve)
    wireCurve = cmds.ls(sl = True, o = True)[0]
    
    create_wireDeformer(wireObj, wireCurve, 40)
    return updateCopynum
    
def make_treads():
    cmds.select(selected_object, r = True)
    cmds.select(make_curve.tread_curve, add = True)
    cmds.pathAnimation(
        f = True,
        fa = "z",
        ua= "y",
        wut = "vector",
        wu = (0,1,0),
        inverseFront = False,
        iu = False,
        b = False,
        stu = 1,
        etu = updateCopynum
        )
    cmds.select(selected_object, r = True)
    cmds.selectKey("motionPath1_uValue", time = (1, updateCopynum))
    cmds.keyTangent(itt = "linear", ott = "linear")
    cmds.snapshot(n = "TreadSS", i = 1, ch = False, st = 1, et = updateCopynum, u= "Animation Curve")
    cmds.DeleteMotionPaths()
    cmds.select("TreadSSGroup", r = True)
    cmds.polyUnite(n = "TreadFull", ch = False)
    cmds.select("TreadSSGroup", r = True)
    cmds.delete()
    def create_wireDeformer(geo, wireCurve, dropoff_distance = 40):
        wire = cmds.wire(geo, w = wireCurve, n = "_wire")
        wire_node = wire[0]
        cmds.setAttr(wire_node+".dropoffDistance[0]", dropoff_distance)
    
    cmds.select("TreadFull")
    wireObj = cmds.ls(sl = True, o = True)[0]
    
    cmds.select(make_curve.tread_curve)
    wireCurve = cmds.ls(sl = True, o = True)[0]
    
    create_wireDeformer(wireObj, wireCurve, 40)
    
    ### Auto Wheel Functions ###
def master_group():
    if cmds.objExists('vehicle_GRP')!=True: 
        cmds.group(n='vehicle_GRP', empty=True)
        cmds.select('vehicle_GRP', replace=True)
        lock_xform_channel()
    else:
        pass 
        
def master_CTRL():
        if cmds.objExists('global_CTRL')!=True: 
            ctrl_node = cmds.circle(degree=1, sections=6, normal=[0,1,0])
            ctrl = cmds.rename(ctrl_node[0], 'global_CTRL') 
            ctrl_attrs = cmds.rename(ctrl_node[1], (ctrl + '_attrs')) 
            cmds.select(ctrl, r=True ) 
            resize_circle()
            order_joints()
            global_prt = cmds.listRelatives(ctrl, p=True)
            if global_prt:
                pass
            else:
                cmds.parent(ctrl, 'vehicle_GRP')
        else:
            pass 
        
def MakeJoint():
    jntList = []
    nameNumber = 1
    locList = []
    sel = cmds.ls(sl=1)
    locPosX = 0
    locPosY = 0
    locPosZ = 0
    global NewJointName
    WorldRotation = 1
    HirarchyCheckBox =0

    if NewJointName == "":
        NewJointName = "joint"
    for i in sel:
        locator = cmds.spaceLocator(n ="locator_For_Rig_"+ str(nameNumber).zfill(3))
        locList.append(locator[0])
        nameNumber += 1
        cmds.delete(cmds.parentConstraint( i , locator , mo = 0 ))
        cmds.select( clear=True )
    nameNumber = 0
    for Loc in locList:
        locPosX = cmds.getAttr(Loc+".translateX")
        locPosY = cmds.getAttr(Loc+".translateY")
        locPosZ = cmds.getAttr(Loc+".translateZ")
        newJoint = cmds.joint(p=(locPosX, locPosY, locPosZ),n = NewJointName + "_jnt_" +str(nameNumber).zfill(3))
        nameNumber += 1
        jntList.append(newJoint)
    if WorldRotation == 0:
        cmds.joint(jntList[0] ,e= True,oj = "xyz" , sao = "yup" , ch = True , zso = True )
    if HirarchyCheckBox == 0:
        for jnt in jntList:
            try:
                cmds.parent(jnt , world = True)
            except:
                print("")
        cmds.select( locList )
        cmds.delete()
        master_group()
        master_CTRL()    

def bindskin_joints():
    obj_sel = cmds.ls(sl=True, type='transform')
    joints_sel = cmds.ls(sl=True, type='joint')
    if (len(obj_sel) == 0):
        cmds.warning('You have to select the mesh before bind the skin')
    if (len(joints_sel) == 0):
        cmds.warning('You have to select the joint before bind the skin')
    else:
        mel.eval('newSkinCluster \"-toSelectedBones -bindMethod 1  -normalizeWeights 1 -mi 1 -omi true -rui true\"')

def arrow_drop():
    cmds.curve(
        n = "WheelCTRL",
        d = 1, 
        p = [(-1,0,-2), (-1, 0 ,2), (-2, 0,2), (0,0,4), (2,0,2),
        (1,0,2), (1,0,-2), (2,0,-2), (0,0,-5), (-2,0,-2),(-1,0,-2)], 
        k = [0,1,2,3,4,5,6,7,8,9,10]
    )
    radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)
    if radial_selection == 1:
        print("Direction is X")
        cmds.rotate(0,90,0)
    if radial_selection == 2:
        print("Direction is Y")
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo = True)

def wheel_selection():
    nameNumber = 1
    global updated_index
    wheel_selection.selected_wheels = cmds.ls(sl=True)
    print(wheel_selection.selected_wheels)
    if len(wheel_selection.selected_wheels) >= 1:
        wheel_selection.wheel_group = cmds.group(n = "Wheels_Jnt_GRP_" + str(nameNumber).zfill(3))
        nameNumber += 1
        arrow_drop()
        cmds.select('WheelCTRL')
        cmds.select(wheel_selection.wheel_group, add = True)
        #Now we need the arrow controller to control the wheels
        rot_mult = cmds.intSliderGrp(rotation_speed, q = True, v = True)
        radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)
        if radial_selection == 1:
            print("Axis is X")
            axis = "x"
            rotation = "z"
        if radial_selection == 2:
            print("Axis is Y")
            axis = "y"
            rotation = "x"
        if radial_selection == 3:
            print("Axis is z")
            axis = "z"
            rotation = "x"
        for wheel in wheel_selection.selected_wheels:
            cmds.expression(n = "rotator", s = f"{wheel}.r{rotation}=WheelCTRL.t{axis}*{rot_mult}")
        cmds.parentConstraint('WheelCTRL', wheel_selection.wheel_group, mo = True)
        rename_asset()
        cmds.parent(wheel_selection.wheel_group, 'vehicle_GRP')
        group_wheel_CTRL()
        grp_wheel = cmds.ls("Wheels_Jnt_GRP_*", type='transform')
        for x in range(len(grp_wheel)):
            cmds.connectAttr('global_CTRL' + '.scale', grp_wheel[x] + '.scale', f=True)
            cmds.warning('Ready to use!')
        else:
            pass
    else:
        cmds.warning("Select at least 1 object")

def group_wheel_CTRL():
    nodes = cmds.ls("WheelCTRL_*")
    print (nodes)
    cmds.select(nodes)
    cmds.parent(nodes, 'global_CTRL')

def reset_all():
    cmds.delete(f"WheelCTRL_*")
    cmds.select(wheel_selection.selected_wheels) 
    cmds.ungroup(f"Wheels_Jnt_GRP_*")
    cmds.ungroup('vehicle_GRP')
    cmds.select(cl=True)
    master_group()
    cmds.parent('global_CTRL', 'vehicle_GRP')
    
def extra_arrow_drop():
    cmds.curve(
        n = "ExtraCTRL1",
        d = 1, 
        p = [(-1,0,-2), (-1, 0 ,2), (-2, 0,2), (0,0,4), (2,0,2),
        (1,0,2), (1,0,-2), (2,0,-2), (0,0,-5), (-2,0,-2),(-1,0,-2)], 
        k = [0,1,2,3,4,5,6,7,8,9,10]
    )
    radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)
    if radial_selection == 1:
        print("Direction is X")
        cmds.rotate(0,90,0)
    if radial_selection == 2:
        print("Direction is Y")
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo = True)
        
def rename_asset():
    nameNumber = 1
    global updated_index
    curv_sel = cmds.rename("WheelCTRL","WheelCTRL_" + str(nameNumber).zfill(3))

# ==== Hydraulics Functions ====
def outer_pistons():
    global outer_piston_name
    outer_result = cmds.promptDialog(title = "Outer piston", message = "Name the outer piston",button = ['OK','Cancel'])
    if outer_result == 'OK':
        outer_piston_name = cmds.promptDialog(query = True, text = True)
        
        cmds.polyCylinder(name = outer_piston_name, r = 0.3, h = 8,
                        sx= 10 ,sy = 1, sz = 1, ax = (1, 0, 0),
                        rcp = 0, cuv = 3, ch =1)
        cmds.select(f'{outer_piston_name}.f[20:29]')
        cmds.delete()
        cmds.select(f'{outer_piston_name}.f[0:9]')
        
        #going to extrude mode
        cmds.polyExtrudeFacet(f'{outer_piston_name}.f[0:9]',
        constructionHistory = 1,
        keepFacesTogether = 1,
        pvx = 0,
        pvy = 1.490116119e-08,
        pvz = -1.490116119e-08,
        divisions = 1, twist = 0,
        taper = 1,
        off = 0,
        thickness = 0,
        smoothingAngle = 30)
        
        #extruding in the Z transform
        cmds.setAttr("polyExtrudeFace1.localTranslate",  0,0,0.116179, type = 'double3')
        
        #making the outer space locator
        outer_pistons.front_locator = cmds.spaceLocator(n="OuterLocator_Front")
        cmds.scale(2,2,2)
        cmds.move(4,0,0, r=True)
        outer_pistons.back_locator = cmds.spaceLocator(n="OuterLocator_Back")
        cmds.scale(2,2,2)
        cmds.move(-4,0,0, r=True)
        cmds.select(clear=True)
        
        cmds.button(window_maker.out_joint_button, edit = True, enable = True, visible = True)
        #editor
        
def inner_pistons():
    global inner_piston_name
    inner_result = cmds.promptDialog(title = "Inner piston", message = "Name the inner piston",button = ['OK','Cancel'])
    if inner_result == 'OK':
        inner_piston_name = cmds.promptDialog(query = True, text = True)
        
        cmds.polyCylinder(name = inner_piston_name, r = 0.29, h = 5,
                        sx= 20 ,sy = 1, sz = 1, ax = (1, 0, 0),
                        rcp = 0, cuv = 3, ch =1)
        cmds.move(4,0,0, r=True)
        
        #making the inner space locator
        inner_pistons.front_locator = cmds.spaceLocator(n="InnerLocator_Front")
        cmds.scale(1.5,1.5,1.5)
        cmds.move(6.5,0,0, r=True)
        inner_pistons.back_locator = cmds.spaceLocator(n="InnerLocator_Back")
        cmds.move(1.5,0,0, r=True)
        cmds.scale(1.5,1.5,1.5)
        cmds.select(clear=True)
        
        cmds.button(window_maker.in_joint_button, edit = True, enable = True, visible = True)

def inner_joints():
    global in_joint_made
    in_joint_made = True
    
    #make the inner joints set their position to the inner locators
    cmds.select(clear=True)
    inner_joints.front_joint = cmds.joint(n="inner front joint")
    cmds.matchTransform(inner_joints.front_joint, inner_pistons.front_locator)
    
    inner_joints.back_joint = cmds.joint(n="inner back joint")
    cmds.matchTransform(inner_joints.back_joint, inner_pistons.back_locator)
    cmds.select(clear=True)
    

    
    #checks if outer joints is made and sets the constraints button to visible
    if out_joint_made == True:
        print("in constrain true")
        cmds.button(window_maker.constraint_button, edit = True, enable = True, visible = True)
    
def outer_joints():
    
    global out_joint_made
    out_joint_made = True
    
    #make the outer joints set their position to the outer locators
    cmds.select(clear=True)
    
    outer_joints.back_joint = cmds.joint(n="outer back joint")
    cmds.matchTransform(outer_joints.back_joint, outer_pistons.back_locator)
    
    outer_joints.front_joint = cmds.joint(n="outer front joint")
    cmds.matchTransform(outer_joints.front_joint, outer_pistons.front_locator)
    
    cmds.select(clear=True)
  
    #checks if inner joints is made and sets the constraints button to visible
    if in_joint_made == True:
        cmds.button(window_maker.constraint_button, edit = True, enable = True, visible = True)
        print("out constrain true")
        
        
def constraint_joints():
    print("constraint is being called")
    if in_joint_made == True and out_joint_made == True:
    #aim constraint the inner front joint to the outer back joint
        cmds.aimConstraint(inner_joints.front_joint,outer_joints.back_joint)
    
    #aim constrain the outer back joint to the inner front joint
        #make the vector negative
        cmds.aimConstraint(outer_joints.back_joint,inner_joints.front_joint, aimVector =(-1,0,0))
        cmds.select(clear=True)
        cmds.button(window_maker.relocate_button, edit = True, enable = True, visible = True)
    else:
        print ("only one joint has been made")

def relocate_pivots():
    # Re-locate Object Pivots to Joints location and parent them
    # Inner Piston
    cmds.select(inner_piston_name)
    cmds.select(inner_joints.front_joint, add = True)
    cmds.MatchPivots()
    cmds.parent()
    cmds.select(cl = True)
    
    #Outer Piston
    cmds.select(outer_piston_name)
    cmds.select(outer_joints.back_joint, add = True)
    cmds.MatchPivots()
    cmds.parent()
    cmds.select(cl = True)
    
def unlock_channels():
    objs = cmds.ls(selection=True, type='transform')
    trs = ['t','r','s']
    xyz = ['x','y','z']
    for obj in objs:
        for attr_trs in trs:
            for axis in xyz:
                cmds.setAttr(obj + '.'+ attr_trs + axis, edit=True, lock=False)
                    
### Window UI ###
def window_maker():
    pass
    
win_name = 'Auto_Rigging'
if cmds.window(win_name, query=True, exists=True):
    cmds.deleteUI(win_name)
   
cmds.window(win_name, sizeable=False, height=350, width=460, backgroundColor=(0.1,0.1,0.1))


# Create the tabLayout
tabControls = cmds.tabLayout()

# Arm tab
tab1Layout = cmds.columnLayout(adj=True)
    # Button for Locators
msg_001 = cmds.text('Before anything make sure your model is aimin at positive Z', backgroundColor=(0.5,0,0),h=30)
msg_002 = cmds.text('Locators goes to pivot position of meshes that you select')
cmds.separator(width=200, height=20)
make_locators = cmds.button(label='make Locators', enable=True, command='locator_pivot()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
reset_loc_btn = cmds.button(label='Undo Locators', enable=True, command='delete_locators()', backgroundColor=(0.3,0.3,0.3))

    # Button to name joints
cmds.separator(width=200, height=20)
msg_003 = cmds.text('Always change the name before creating a new chain of joints!CONFIRM NAME!')
joint_name = cmds.textFieldGrp(label="Name for the joints: ", text="JointsName", cc="name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)")
confirm_name = cmds.button(label='Confirm Name', enable=True, command='name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)', backgroundColor=(0.3,0.3,0.3))

    # Button to create joints
cmds.separator(width=200, height=20)
msg_004 = cmds.text('Create Joints')
make_joint_btn = cmds.button(l='make joints', enable=True,c='make_joints()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
show_axis_joints = cmds.button(label='show axis joints', enable=True, command='show_axis_display(display=True)', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
hide_axis_joints = cmds.button(label='hide axis joints', enable=True, command='hide_axis_display(display=False)', backgroundColor=(0.3,0.3,0.3))

    # Button to orient joints
cmds.separator(width=200, height=20)
msg_005 = cmds.text('Select the root to orient the joints')
ORIENT_JOINTS_BTN = cmds.button(label='Orient Joint', enable=True, command='orient_joints()', backgroundColor=(0.3,0.3,0.3))

# Button for IK/FK
cmds.separator(width=200, height=20)
msg_005 = cmds.text('IK/FK Switcher')
MAKE_FK_BTN = cmds.button(label='make FK/IK', enable=True, command='fk_ik_maker()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
SEL_GLOBAL_BTN = cmds.button(label='select Global_CTRL', enable=True, command='select_global_ctrl()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width=200, height=20)
msg_006 = cmds.text('After you create the joints, you can press "Undo Locators"')
msg_007 = cmds.text('So you can make another chain of joints')
# We need to go back one to the tabLayout (the parent) to add the next tab layout.
cmds.setParent('..')

# Tread Maker tab
tab2Layout = cmds.columnLayout(adj=True)
window_maker.init_button = cmds.button(label = "Initialize", command = "make_locator()", backgroundColor=(0.3,0.3,0.3))
window_maker.reset_button = cmds.button(label = "Reset", command = "reset_locator()", enable = False, backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200)
window_maker.curve_button = cmds.button(label = "Make Tread Curve", command = "make_curve()", visible = False, enable = False, backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200)
window_maker.text_button = cmds.textFieldButtonGrp(buttonLabel="Pick Tread OBJ", buttonCommand = "pick_object()" , editable = False, visible = True)
window_maker.picker_button = cmds.button(label = "Pick Tread Object", command = "make_curve()", visible = False, enable = False, backgroundColor=(0.3,0.3,0.3))
window_maker.text_tread=cmds.text("No. Treads", visible=False)
window_maker.copies_slider = cmds.intSliderGrp(min = 10, max = 200, width = 500, field = True, changeCommand = "numchange()", visible = True,w=10)
cmds.setParent('..')

# Wheel tab
tab3Layout = cmds.columnLayout(adj=True)
# Place a text message into this layout for reference
cmds.text(l="Select the Wheels you Want to Control Together")
cmds.separator(width = 200, h = 10)
joint_name_wheel = cmds.textFieldGrp(label="Name for the joints: ", text="JointsName", cc="NewJointName = cmds.textFieldGrp(joint_name_wheel, q=1, tx=1)")
confirm_name = cmds.button(label='Confirm Name', enable=True, command='NewJointName = cmds.textFieldGrp(joint_name_wheel, q=1, tx=1)', backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
rotation_speed = cmds.intSliderGrp(l = "Adjust Rotation Multiplier",f = True, v = 20, min = 1, max = 100, sbm = "You are setting the rotation multiplier")
radial_selection_button = cmds.radioButtonGrp(
    l = "Direction of Controler",
    labelArray3 = ["X", "Y", "Z"],
    nrb = 3,
    sl = 3
    )
cmds.separator(width = 200, h = 10)
cmds.button(l = "joints", c = "MakeJoint()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
cmds.button(l = "bind skin", c = "bindskin_joints()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
cmds.button(l = "Wheel Controls", c = "wheel_selection()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
cmds.button(l = "Undo", c = "reset_all()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, h = 10)
cmds.button(l = "Extra Arrow CTRL", c = "extra_arrow_drop()", backgroundColor=(0.3,0.3,0.3))

cmds.setParent('..')

# Hydraulics tab
tab4Layout = cmds.columnLayout(adj=True)
window_maker.out_piston_button = cmds.button(label = "Create Outer Piston", command ="outer_pistons()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, height = 10)
window_maker.in_piston_button = cmds.button(label = "Create Inner Piston", command ="inner_pistons()", backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, height = 10)
window_maker.out_joint_button = cmds.button(label = "Set Outer Joints", command = "outer_joints()", enable = False, visible = True, backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, height = 10)
window_maker.in_joint_button = cmds.button(label = "Set Inner Joints", command = "inner_joints()", enable = False, visible = True, backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, height = 10)
window_maker.constraint_button = cmds.button(label = "Constraint Joints", command = "constraint_joints()", enable = False, visible = True, backgroundColor=(0.3,0.3,0.3))
cmds.separator(width = 200, height = 10)
window_maker.relocate_button = cmds.button(label = "Attach to Pipes", command = "relocate_pivots()", enable = False, visible = True, backgroundColor=(0.3,0.3,0.3))
cmds.setParent('..')

# Create appropriate labels for the tabs
cmds.tabLayout(tabControls, edit=True, tabLabel=(
(tab1Layout, "Arm Maker"), (tab2Layout, "Tread Maker"), (tab3Layout, "Wheel Maker"), (tab4Layout, "Hydraulics Maker")))
radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)


cmds.showWindow('Auto_Rigging')