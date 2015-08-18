print "|--------------------------------------------|"
print "|       Batch Offline Retargetting Demo      |"
print "|              20150818                      |"
print "|--------------------------------------------|"


import os


def setMotionNameSkeleton(motionName, skelName):
	motion = scene.getMotion(motionName)
	if motion != None:		
		motion.setMotionSkeletonName(skelName)
	
def createRetargetInstance(srcSkelName, tgtSkelName):
	# replace retarget each animation with just a simple retarget instance
	
	# these joints and their children are not retargeted
	endJoints = StringVec();
	endJoints.append('l_forefoot')
	endJoints.append('l_toe')
	endJoints.append('l_wrist')
	endJoints.append('r_forefoot')	
	endJoints.append('r_toe')	
	endJoints.append('r_wrist')

	# these joints are skipped during skeleton alignment
	relativeJoints = StringVec();
	relativeJoints.append('spine1')
	relativeJoints.append('spine2')
	relativeJoints.append('spine3')
	relativeJoints.append('spine4')
	relativeJoints.append('spine5')
	relativeJoints.append('r_sternoclavicular')
	relativeJoints.append('l_sternoclavicular')
	relativeJoints.append('r_acromioclavicular')
	relativeJoints.append('l_acromioclavicular')	
	
	retargetManager = scene.getRetargetManager()
        retarget = retargetManager.getRetarget(srcSkelName,tgtSkelName)
	if retarget == None:
		retarget = 	retargetManager.createRetarget(srcSkelName,tgtSkelName)
		retarget.initRetarget(endJoints,relativeJoints)
		
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

#scene.run('motion-retarget.py')
#start retarget
folder = '../bin'#output folder
for i in range(0,len(retargetMotionsNames)):
# Retarget motion
	print 'About to run retargetting for animation : '+ retargetMotionsNames[i]
	motion = scene.getMotion(retargetMotionsNames[i])
	#retargetMotionWithGuessMap(retargetMotionsNames[i], sourceName+'.sk', targetName+'.sk', scene.getMediaPath() + '/' + 'sbm-common/common-sk/retargetMotion/')
	#retargetMotionWithMap(rachelMotions[i], sourceMesh, sourceMesh, outDir, srcMapName, tgtMapName)
	#online retarget
	output = targetName+'_'+retargetMotionsNames[i]
	#setMotionNameSkeleton("ChrBrad@Idle01", "ChrBrad.sk")
	setMotionNameSkeleton(retargetMotionsNames[i],sourceName+'.sk')
createRetargetInstance(sourceName+'.sk', targetName+'.sk')		
