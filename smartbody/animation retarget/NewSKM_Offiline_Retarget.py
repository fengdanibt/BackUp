print "|--------------------------------------------|"
print "|       Batch Offline Retargetting Demo      |"
print "|              20150818                      |"
print "|--------------------------------------------|"

# Add asset paths
targetName= 'ChrConnor'
sourceName= 'ChrEllieDcaps'
#retargetMotionsNames = StringVec();#'ChrEllieDcaps@Idle01_BeatLowBt01'

#put the mesh in mesh folder // only .dae works 
scene.addAssetPath('mesh', 'mesh')
# add the motions and .sk files
scene.addAssetPath('motion', targetName)
scene.addAssetPath('motion', sourceName)
# add the dirt for retarget file
scene.addAssetPath('script', 'scripts')
scene.loadAssets()

#get the name of all the retargeting motions 
motionNames =  scene.getAssetManager().getMotionNames()
retargetMotionsNames = [ani for ani in motionNames if 'ChrEllieDcaps@Idle01_' in ani]
print str(len(retargetMotionsNames))+' motions for retargeting'

scene.run('motion-retarget.py')
#start retarget
folder = '../bin'#output folder
for i in range(0,len(retargetMotionsNames)):
# Retarget motion
	print 'About to run retargetting for animation : '+ retargetMotionsNames[i]
	motion = scene.getMotion(retargetMotionsNames[i])
	retargetMotionWithGuessMap(retargetMotionsNames[i], sourceName+'.sk', targetName+'.sk', scene.getMediaPath() + '/' + 'sbm-common/common-sk/retargetMotion/')
	#retargetMotionWithMap(rachelMotions[i], sourceMesh, sourceMesh, outDir, srcMapName, tgtMapName)
	print "Finish the retargeting.................."
	
	output = targetName+'_'+retargetMotionsNames[i]
	retargetedMotion = scene.getMotion(output)
	if (retargetedMotion == None):
		print "Cannot find the output gesture!!!!!!!!!!!!!!"
	else:
		print "The skeleton name of this motion is "+ retargetedMotion.getMotionFileName() 
		removeJoints = StringVec();
		removeJoints.append('JtJaw')
		retargetedMotion.removeMotionChannels(removeJoints)
		retargetedMotion.saveToSkm(output)
		infilename = os.path.join(folder,output)
		if not os.path.isfile(infilename): continue
		newname = infilename + '.skm'
		if os.path.isfile(newname): continue
		#print newname
		output = os.rename(infilename, newname)
		


'''# Runs the default viewer for camera
print 'Configuring scene parameters and camera'
scene.setScale(1.0)
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


# Add Character script
target = scene.createCharacter('target', '')
targetSkeleton = scene.createSkeleton(targetName+'.sk')
target.setSkeleton(targetSkeleton)
targetPos = SrVec(-0.50, 0, 0)
target.setPosition(targetPos)
target.createStandardControllers()
#set the scale of 3D model, normally is 0.01/ the model size is m, but smartbody is cm
target.setDoubleAttribute('deformableMeshScale', .01)
target.setStringAttribute('deformableMesh', targetName+'.dae')
#bml.execBML('target', '<body posture="ChrRachel@Idle02"/>')

source = scene.createCharacter('source', '')
sourceSkeleton = scene.createSkeleton(sourceName+'.sk')
#rescale the skeleton if it do not work // sourceSkeleton.rescale(100)
source.setSkeleton(sourceSkeleton)
sourcePos = SrVec(0.50, 0, 0)
source.setPosition(sourcePos)
source.createStandardControllers()
# Deformable mesh
source.setDoubleAttribute('deformableMeshScale', .01)
source.setStringAttribute('deformableMesh', sourceName+'.dae')
#bml.execBML('source', '<body posture="ChrBrad@Idle01"/>')

# Turn on GPU deformable geometry
target.setStringAttribute("displayType", "GPUmesh")
source.setStringAttribute("displayType", "GPUmesh")


# Run motion retarget script
scene.run('motion-retarget.py')

# Retarget motion
print 'About to run retargetting'
motion = scene.getMotion(retargetMotionsNames)

#motion.scale(100)
retargetMotionWithGuessMap(retargetMotionsNames, sourceName+'.sk', targetName+'.sk', scene.getMediaPath())
#retargetMotionWithMap('ChrBrad@Guitar01', 'ChrBrad.sk', 'ChrRachel.sk', scene.getMediaPath() + '/' + 'sbm-common/common-sk/retargetMotion/','zebra2','zebra2')
#output = 'ChrRachel.skChrBrad@WalkTightCircleRt01'
#retargetedMotion = scene.getMotion(output)
#retargetedMotion.scale(.01)
#remapMotion('ChrBrad.sk',output,'zebra2')
	
last = 0
canTime = True
delay = 10
class RetargettingDemo(SBScript):
	def update(self, time):
		global canTime, last, output
		diff = time - last
		if diff >= delay:
			canTime = True
			diff = 0
		if canTime:
			last = time
			canTime = False
			# Play non retargetted and retargetted add delay
			bml.execBML('target', '<animation name="'+targetName+'.sk'+retargetMotionsNames+'"/>')
			bml.execBML('source', '<animation name="'+retargetMotionsNames+'"/>')
			
scene.removeScript('retargettingdemo')
retargettingdemo = RetargettingDemo()
scene.addScript('retargettingdemo', retargettingdemo)'''
