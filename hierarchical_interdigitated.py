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
sketch_spreader = doc.addObject('Sketcher::SketchObject', 'tree_spreader')
doc.recompute()

branch_height = 2
branch_length = 2.8
tree_spacing = 8
branch_num = 5
tree_num = 3
thickness_z = 1 #mm
branch_thickness = 0.5
tree_thickness = 1.5

branch_height_start = 0
for k in (0,1):
    if k == 1: # Parameter inverted when branch flipped
        branch_height_start = branch_height_start = branch_height*branch_num + branch_height_start + branch_height*0.5
        branch_height = -branch_height
    for j in np.arange(0,tree_num,1):
        tree_spacing_dis = j*tree_spacing
        if k == 1:
            tree_spacing_dis = (j*tree_spacing)+(tree_spacing/2)
        for i in np.arange(0,branch_num,1):
            sketch_main.addGeometry(Part.LineSegment(App.Vector(tree_spacing_dis,(branch_height*i)+branch_height_start,0),
                                                     App.Vector(tree_spacing_dis,(branch_height*(i+1))+branch_height_start,0)),False)
            if j == 0 and k == 0: #First branch and the one not inverted
                if i == branch_num-1: # At the last branch, make it a bit longer to make seamless corner
                    extra_len = tree_thickness/2
                else:
                    extra_len = 0
                sketch_branch.addGeometry(Part.LineSegment(App.Vector(tree_spacing_dis+branch_length,(branch_height*(i+1))+branch_height_start),
                                                           App.Vector(tree_spacing_dis-extra_len,(branch_height*(i+1))+branch_height_start,0)),False)
            elif j == tree_num-1 and k == 1: #Last branch that is also inverted
                if i == branch_num-1: # At the last branch, make it a bit longer to make seamless corner
                    extra_len = tree_thickness/2
                else:
                    extra_len = 0
                sketch_branch.addGeometry(Part.LineSegment(App.Vector(tree_spacing_dis-branch_length,(branch_height*(i+1))+branch_height_start),
                                                           App.Vector(tree_spacing_dis+extra_len,(branch_height*(i+1))+branch_height_start,0)),False)
            else:
                sketch_branch.addGeometry(Part.LineSegment(App.Vector(tree_spacing_dis-branch_length,(branch_height*(i+1))+branch_height_start),
                                                           App.Vector(tree_spacing_dis+branch_length,(branch_height*(i+1))+branch_height_start,0)),False)

branch_height = abs(branch_height)
flow_distributor = branch_length*2+(tree_spacing/2)*tree_num
sketch_spreader.addGeometry(Part.LineSegment(App.Vector(0,branch_height*branch_num+branch_height*0.5,0),
                                             App.Vector(flow_distributor,branch_height*branch_num+branch_height*0.5,0)),False)


doc.recompute()

main_obj = Arch.makeWall(sketch_main)
Draft.autogroup(main_obj)
main_obj.Height = thickness_z  #mm
main_obj.Width = tree_thickness   #mm
main_obj.Label = "wall_tree_main"

branch_obj = Arch.makeWall(sketch_branch)
Draft.autogroup(branch_obj)
branch_obj.Height = thickness_z  #mm
branch_obj.Width = branch_thickness   #mm
branch_obj.Label = "wall_tree_branch"
doc.recompute()

bp = BOPFeatures.BOPFeatures(App.activeDocument())
whole_tree = bp.make_multi_fuse([main_obj.Name, branch_obj.Name])
whole_tree.Refine = True
doc.recompute()
