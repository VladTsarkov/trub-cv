import bpy
from mathutils import Vector
import random
from math import cos,sin,radians
def data_gen(circles=3,step_angl=3,rds=200,err_rds=2):
    angl = 0
    #img = create_img()
    z = 0
    cnt = 0
    list_data = []
    for i in range(circles):
        while angl<=360:
            temp_err = random.uniform(-err_rds,err_rds)
            x = (rds+temp_err) * cos(radians(angl))  #+ 400
            y = (rds+temp_err) * sin(radians(angl))  #+ 400
            z += 1
            list_data.append([x,y,z,cnt])
            #cv.circle(img,(int(x),int(y)), 2, (0,0,0),-1)
            angl+=step_angl
            cnt += 1
        cnt = 0
        angl = 0
        #show_img(img)
        #blank_img(img)
    return list_data

jsn = 'data/scan-01.json'
#data_from_json(jsn)
list_data = data_gen()
print(list_data)

for obj in bpy.data.objects:
    print(obj.name)
'''
#vertices = [{0,0,0},]
vertices = [Vector((0,0,0)),
            Vector((0,1,0)),
            Vector((1,1,0)),
            Vector((1,0,0)),
            ]
edges = []
faces = [[0,1,2,3]]
new_mesh = bpy.data.meshes.new('mesh_test')
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()

new_object = bpy.data.objects.new('new_obj', new_mesh)

#print(getattr(bpy.data,'collections'))

bpy.context.scene.objects.link(new_object)
'''
vert2 = []
edges2 = []
faces2 = []

for x,y,z,c in list_data:
    vert2.append(Vector((x/10.,y/10.,z/10.)))
print(vert2)

temp = 0
while temp+121<len(vert2):
    faces2.append([temp,temp+1,temp+121,temp+120])
    temp += 1
print(faces2)

new_mesh = bpy.data.meshes.new('mesh_test')
new_mesh.from_pydata(vert2, edges2, faces2)
new_mesh.update()

new_object = bpy.data.objects.new('new_obj', new_mesh)

#print(getattr(bpy.data,'collections'))

bpy.context.scene.objects.link(new_object)

#new_collection = bpy.data.collections.new('new_collection')
#bpy.context.scene.colletions.children.link(new_collection)

#new_collection.objects.link(new_object)