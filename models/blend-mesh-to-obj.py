#!/usr/bin/env python

#based on 'export-sprites.py' and 'glsprite.py' from TCHOW Rainbow; code used is released into the public domain.

#Note: Script meant to be executed from within blender, as per:
#blender --background --python blend-mesh-to-obj.py -- <infile.blend> <meshname> <outfile.obj>


import sys

args = []
for i in range(0,len(sys.argv)):
	if sys.argv[i] == '--':
		args = sys.argv[i+1:]

if len(args) != 3:
	print("\n\nUsage:\nblender --background --python blend-mesh-to-obj.py -- <infile.blend> <objname> <outfile.obj>\nExport a obj file with vertex positions and triangulated faces corresponding to a named mesh object.\n")
	exit(1)

infile = args[0]
objname = args[1]
outfile = args[2]


import bpy, bmesh

bpy.ops.wm.open_mainfile(filepath=infile)

if not objname in bpy.data.objects:
	print("Object named '" + objname + "' does not seem to exist.")
	for obj in bpy.data.objects:
		print(obj.name)
	exit(1)

obj = bpy.data.objects[objname]

if obj.type != 'MESH':
	print("Object named '" + objname + "' is a " + obj.type + ", not a MESH.")
	exit(1)

if bpy.context.mode == 'EDIT':
	bpy.ops.object.mode_set(mode='OBJECT') #get out of edit mode (just in case)

#make sure object is on a visible layer:
bpy.context.scene.layers = obj.layers
#select the object and make it the active object:
bpy.ops.object.select_all(action='DESELECT')
obj.select = True
bpy.context.scene.objects.active = obj

mesh = obj.to_mesh(scene=bpy.context.scene, apply_modifiers=True, settings='PREVIEW')
bm = bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=3, ngon_method=1)
bm.to_mesh(mesh)
bm.free()

##subdivide object's mesh into triangles:
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
#bpy.ops.object.mode_set(mode='OBJECT')

#compute normals (respecting face smoothing):
mesh.calc_normals_split()

vert_lines = []
face_lines = []
written_verts = dict()

for poly in mesh.polygons:
	assert(len(poly.loop_indices) == 3)
	face_line = "f"
	for i in range(0,3):
		assert(mesh.loops[poly.loop_indices[i]].vertex_index == poly.vertices[i])
		loop = mesh.loops[poly.loop_indices[i]]

		if not loop.vertex_index in written_verts:
			written_verts[loop.vertex_index] = len(written_verts)
			#write vertex:
			vertex = mesh.vertices[loop.vertex_index]
			vert_lines.append("v " + str(vertex.co.x) + " " + str(vertex.co.y) + " " + str(vertex.co.z))
		face_line += " " + str(written_verts[loop.vertex_index] + 1)
		#	for x in loop.normal:
		#		data += struct.pack('f', x)
		#if filetype.texcoord:
		#	if uvs != None:
		#		uv = uvs[poly.loop_indices[i]].uv
		#		data += struct.pack('ff', uv.x, uv.y)
		#	else:
		#		data += struct.pack('ff', 0, 0)
	face_lines.append(face_line)

blob = open(outfile, 'wb')
blob.write(("\n".join(vert_lines)).encode('utf8'))
blob.write(b'\n\n')
blob.write(("\n".join(face_lines)).encode('utf8'))
blob.close()
