import FreeCAD as App
import Part
import numpy as np
import Sketcher
import Arch
import Draft
from BOPTools import BOPFeatures

doc = App.activeDocument()
sketch_main = doc.addObject('Sketcher::SketchObject', 'tree_main')
sketch_branch = doc.addObject('Sketcher::SketchObject', 'tree_branch')
sketch_distributor = doc.addObject('Sketcher::SketchObject', 'tree_spreader')
doc.recompute()

branch_spacing = 2
branch_length = 2.8
tree_spacing = 4
branch_num = 5
tree_num = 6
thickness_z = 1 #mm
branch_thickness = 0.5
tree_thickness = 1.5

height_start = 0
branch_height_start = height_start + tree_thickness/2
# for k in (0,1):
#     if k == 1: # Parameter inverted when branch flipped
#         print('')

# for i in np.arange(0,tree_num*2,1):
#     y_tree_spacing = branch_spacing*(i%2)/2
#     x_tree_spacing = tree_num*i
x_start = 0
y_start = 0
for i in np.arange(0,tree_num,1): #tree trunk
    x_tree_spacing = i*tree_spacing
    y_alternate = (i%2)*(branch_spacing/2)
    for j in np.arange(0,branch_num,1): #branch
        if i == 0: #Cut first trunk's branch in half
            x1 = x_start+x_tree_spacing+branch_length
            x2 = x_start+x_tree_spacing+branch_length*2
        elif i == branch_num: #Cut last trunk's branch in half
            x1 = x_start+x_tree_spacing
            x2 = x_start+x_tree_spacing+branch_length
        else:    
            x1 = x_start+x_tree_spacing
            x2 = x_start+x_tree_spacing+branch_length*2
            
        # x2 = x_start+x_tree_spacing+branch_length*2
        y1 = j*branch_spacing+y_alternate + y_start
        y2 = j*branch_spacing+y_alternate + y_start
        sketch_branch.addGeometry(Part.LineSegment(App.Vector(x1,y1,0), App.Vector(x2,y2,0)),False) #make branches
        
        if j == branch_num-1 and i%2 == 0:
            root_tip = tree_thickness/2
        elif j == 0 and i%2 == 1:
            root_tip = -tree_thickness/2
        else:
            root_tip = 0
        
        if i == 0:
            x1 = x_start+x_tree_spacing     
        f1 = x1+branch_length
        f2 = x1+branch_length
        g1 = y1
        g2 = y1+branch_spacing*((-1)**i)+root_tip
        sketch_branch.addGeometry(Part.LineSegment(App.Vector(f1,g1,0), App.Vector(f2,g2,0)),False) #make trunk

# branch_height = abs(branch_height)
# sketch_main.addGeometry(Part.LineSegment(App.Vector(tree_spacing_dis,0,0),App.Vector(tree_spacing_dis,(branch_num*branch_height)+(height_start + tree_thickness/2),0)),False)


# flow_distributor = (tree_num-1)*tree_spacing+tree_spacing/2+tree_thickness/2

# sketch_distributor.addGeometry(Part.LineSegment(App.Vector(0-tree_thickness/2,branch_height*branch_num+branch_height*0.5,0),
#                                               App.Vector(flow_distributor,branch_height*branch_num+branch_height*0.5,0)),False)
# sketch_distributor.addGeometry(Part.LineSegment(App.Vector(0-tree_thickness/2,0,0),
#                                               App.Vector(flow_distributor,0,0)),False)

doc.recompute()

# main_obj = Arch.makeWall(sketch_main)
# Draft.autogroup(main_obj)
# main_obj.Height = thickness_z  #mm
# main_obj.Width = tree_thickness   #mm
# main_obj.Label = "wall_tree_main"

# branch_obj = Arch.makeWall(sketch_branch)
# Draft.autogroup(branch_obj)
# branch_obj.Height = thickness_z  #mm
# branch_obj.Width = branch_thickness   #mm
# branch_obj.Label = "wall_tree_branch"
# doc.recompute()

# distributor_obj = Arch.makeWall(sketch_distributor)
# Draft.autogroup(distributor_obj)
# distributor_obj.Height = thickness_z  #mm
# distributor_obj.Width = tree_thickness   #mm
# distributor_obj.Label = "wall_tree_distributor"
# doc.recompute()

# bp = BOPFeatures.BOPFeatures(App.activeDocument())
# whole_tree = bp.make_multi_fuse([main_obj.Name, branch_obj.Name, distributor_obj.Name])
# whole_tree.Refine = True
doc.recompute()
