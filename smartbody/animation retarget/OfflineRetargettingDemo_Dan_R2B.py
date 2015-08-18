print "|------------------------------------------------------|"
print "|        Starting Rachel to Brad Mapping Demo          |"
print "|                   V 1.1  20150630                    |"
print "|------------------------------------------------------|"
# for file opening and revising 
import os,sys
# Add asset paths
scene.addAssetPath('script', 'scripts')
#scene.addAssetPath('script', 'behaviorsets')
scene.addAssetPath('mesh', 'mesh')
#scene.addAssetPath('mesh', 'retarget/mesh')
#scene.addAssetPath('motion', 'ChrBrad')
scene.addAssetPath('motion', 'ChrRachel')
#scene.addAssetPath('motion', 'retarget/motion')
#scene.addAssetPath('motion', 'sbm-common/common-sk')
scene.loadAssets()

print 'Configuring scene parameters and camera'

scene.run('default-viewer.py')
camera = getCamera()
camera.setEye(0, 1.71, 1.86)
camera.setCenter(0, 1, 0.01)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(1.0472)
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)
cameraPos = SrVec(0, 1.6, 10)
scene.getPawn('camera').setPosition(cameraPos)

# running the joint mapping 
scene.run('zebra2-map.py')
#scene.run('zebra2-map_test.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
#zebra2Map_test = scene.getJointMapManager().getJointMap('zebra2_test')

RachelSkeleton = scene.getSkeleton('ChrRachel_vhtk.sk')
zebra2Map.applySkeleton(RachelSkeleton)

bradSkeleton = scene.getSkeleton('ChrBrad.sk')
#zebra2Map_test.applySkeleton(bradSkeleton)

# Add Character script
taegetMesh = 'ChrBrad.sk'
tgtMapName = 'zebra2_test'
target = scene.createCharacter('target', '')
targetSkeleton = scene.createSkeleton(taegetMesh)
target.setSkeleton(targetSkeleton)
targetPos = SrVec(-0.5, 0, 0)
target.setPosition(targetPos)
target.createStandardControllers()
target.setDoubleAttribute('deformableMeshScale', .01)
target.setStringAttribute('deformableMesh', 'ChrBrad.dae')
#bml.execBML('target', '<body posture="ChrBrad@Idle02"/>')

sourceMesh = 'ChrRachel_vhtk.sk'
srcMapName = 'zebra2'
source = scene.createCharacter('source', '')
sourceSkeleton = scene.createSkeleton(sourceMesh)
#sourceSkeleton.rescale(100)
source.setSkeleton(sourceSkeleton)
sourcePos = SrVec(0.5, 0, 0)
source.setPosition(sourcePos)
source.createStandardControllers()
# Deformable mesh
source.setDoubleAttribute('deformableMeshScale', .01)
source.setStringAttribute('deformableMesh', 'ChrRachel.dae')
bml.execBML('source', '<body posture="ChrRachel@Idle02"/>')


motionNames =  scene.getAssetManager().getMotionNames()
rachelMotions = [ani for ani in motionNames if 'ChrRachel@Idle02_' in ani]
#bradMotions = [anim for anim in rachelMotions if '_retarget' in anim]


# Run motion retarget script
scene.run('motion-retarget_lowerbody.py')
outDir = scene.getMediaPath() + '/' + 'sbm-common/common-sk/retargetMotion/'
for i in range(0,len(rachelMotions)):
# Retarget motion
	print 'About to run retargetting for animation : '+ rachelMotions[i]
	motion = scene.getMotion(rachelMotions[i])
	retargetMotionWithGuessMap(rachelMotions[i], sourceMesh, sourceMesh, scene.getMediaPath() + '/' + 'sbm-common/common-sk/retargetMotion/')
	#retargetMotionWithMap(rachelMotions[i], sourceMesh, sourceMesh, outDir, srcMapName, tgtMapName)
	print "Finish the retargeting.................."
	output = rachelMotions[i]+'_retarget'
	retargetedMotion = scene.getMotion(output)
	if (retargetedMotion == None):
		print "Cannot find the output gesture!!!!!!!!!!!!!!"
	else:
		print "The skeleton name of this motion is "+ retargetedMotion.getMotionFileName() #str( retargetedMotion.getNumChannels())
	#retargetedMotion.scale(.01)
	remapMotion(sourceMesh,output,sourceMesh)

# change the extention of the skm files 
folder = '../bin'
skmFiles = [f for f in os.listdir(folder) if '_retarget' in f]
for filename in skmFiles:
	infilename = os.path.join(folder,filename)
	#print infilename
	if not os.path.isfile(infilename): continue
	newname = infilename + '.skm'
	if os.path.isfile(newname): continue
	#print newname
	output = os.rename(infilename, newname)
	
	
scene.addAssetPath('motion', folder)
#motionNames =  scene.getAssetManager().getMotionNames()
#bradMotions = [anim for anim in motionNames if '_retarget' in anim]
#scene.loadAssets()



# Turn on GPU deformable geometry

target.setStringAttribute("displayType", "GPUmesh")
#scene.run('AddCharacterDemo_test.py')
source.setStringAttribute("displayType", "GPUmesh")

last = 0
canTime = True
delay = 5
anim_count = 0
class RetargettingDemo(SBScript):
	def update(self, time):
		global canTime, last, output, anim_count
		diff = time - last
		if diff >= delay:
			canTime = True
			diff = 0
		if canTime:
			anim_count += 1
			last = time
			canTime = False
			# Play non retargetted and retargetted add delay
			bml.execBML('target', '<animation name="'+rachelMotions[anim_count%59]+'_retarget"/>')
			bml.execBML('source', '<animation name="'+rachelMotions[anim_count%59]+'"/>')
			
scene.removeScript('retargettingdemo')
retargettingdemo = RetargettingDemo()
scene.addScript('retargettingdemo', retargettingdemo)
