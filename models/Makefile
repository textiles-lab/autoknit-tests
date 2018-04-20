.PHONY : all


HOSTNAME := $(shell hostname -s)

#n.b. the '-y' sets autoexec scripts to 'on' so that driver expressions will work (robot leg animation)
ifeq ($(HOSTNAME), incepchow)
	BLENDER = ~/blender-2.78a-linux-glibc211-x86_64/blender -y
else ifeq ($(HOSTNAME), retchow)
	BLENDER = /Applications/Blender/blender.app/Contents/MacOS/blender -y
else
	BLENDER = blender
endif

BLEND_MESH_TO_OBJ=./blend-mesh-to-obj.py

all : \
	simple-capsule.obj \
	simple-cone.obj \
	simple-cube.obj \
	simple-cylinder.obj \
	simple-eight.obj \
	simple-elbow.obj \
	simple-sphere.obj \



simple-%.obj : simple.blend $(BLEND_MESH_TO_OBJ)
	$(BLENDER) --background --python $(BLEND_MESH_TO_OBJ) -- '$<' '$(@:simple-%.obj=%)' '$@'

