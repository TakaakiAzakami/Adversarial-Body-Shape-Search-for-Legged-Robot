# humanoid 太さ(size)変更攻撃
import xml.etree.ElementTree as ET 
import time
import random

tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml')



root = tree.getroot()

size_ratio = {}

name_list = ["torso1","uwaist1","lwaist1","butt1",
			"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
			"right_uarm1","right_larm1","left_uarm1","left_larm1",
			"right_hand1","left_hand1","head1"]#19

size = {"torso1":0.07,"uwaist1":0.06,"lwaist1":0.06,"butt1":0.09,
		"right_thigh1":0.06,"right_shin1":0.049,"right_foot1":0.035,"right_foot2":0.035,
		"left_thigh1":0.06,"left_shin1":0.049,"left_foot1":0.035,"left_foot2":0.035,
		"right_uarm1":0.04,"right_larm1":0.031,"left_uarm1":0.04,"left_larm1":0.031,
		"right_hand1":0.04,"left_hand1":0.04 ,"head1":0.09}#19

size_epsilon = 0.2

def set_size(size,epsilon):
	seed = time.time() 
	r = random.random()	
	ratio = 1.0 - epsilon + r*(epsilon*2)
	#ratio = 1.0 #サイズ初期化したい.
	new_size = size * ratio

	return ratio

for geom in root.iter("geom"):
	for name in name_list:
		if name in str(geom.attrib):
		
			if name in size.keys():	
				size_ratio[name] = set_size(size[name],size_epsilon)#
				geom.set("size",str(size_ratio[name]*size[name]))
				
				#rgb
				"""if size_ratio[name] < 1: #small
					red = 0.5 + ((1-size_ratio[name])/size_epsilon)*0.5
					other1 = 0.5 - ((1-size_ratio[name])/size_epsilon)*0.5
					geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
				else: # big
					blue = 0.5 + ((size_ratio[name]-1)/size_epsilon)*0.5
					other2  = 0.5 - ((size_ratio[name]-1)/size_epsilon)*0.5
					geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))"""
					
					
					
					
				"""if size_ratio[name] < 1: #small
					rgb = 0.5 - ((1-size_ratio[name])/size_epsilon)*0.5
					geom.set("rgba",str(rgb)+str(" ")+str(rgb)+str(" ")+str(rgb)+str(" 1")) 
				else: # big
					rgb = 0.5 + ((size_ratio[name]-1)/size_epsilon)*0.5
					geom.set("rgba",str(rgb)+str(" ")+str(rgb)+str(" ")+str(rgb)+str(" 1"))
					
				if size_ratio[name] < 1:
					red = 0.333 + (1-size_ratio[name])/size_epsilon *0.667
					geom.set("rgba",str(red)+str(" ")+str((1-red)*0.5)+str(" ")+str((1-red)*0.5)+str(" 1")) # red
				else:
					blue = 0.333 + (size_ratio[name]-1)/size_epsilon *0.667
					geom.set("rgba",str((1-blue)*0.5)+str(" ")+str((1-blue)*0.5)+str(" ")+str(blue)+str(" 1")) # blue"""

				
#print("size_ratio",size_ratio)				
				
tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml',encoding='UTF-8')		




def set_adv_size(size_ratio): # lists


	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml')

	root = tree.getroot()

	name_list = ["torso1","uwaist1","lwaist1","butt1",
				"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
				"right_uarm1","right_larm1","left_uarm1","left_larm1",
				"right_hand1","left_hand1","head1"]#19

	size = {"torso1":0.07,"uwaist1":0.06,"lwaist1":0.06,"butt1":0.09,
			"right_thigh1":0.06,"right_shin1":0.049,"right_foot1":0.035,"right_foot2":0.035,
			"left_thigh1":0.06,"left_shin1":0.049,"left_foot1":0.035,"left_foot2":0.035,
			"right_uarm1":0.04,"right_larm1":0.031,"left_uarm1":0.04,"left_larm1":0.031,
			"right_hand1":0.04,"left_hand1":0.04 ,"head1":0.09}#19

	size_ratio_dict = {}
	i = 0
	for name in name_list:# list=>dict
		size_ratio_dict[name] = size_ratio[i]
		i += 1
	
	for geom in root.iter("geom"):
		for name in name_list:
			if name in str(geom.attrib):
			
				if name in size.keys():	
					#size_ratio[name] = set_size(size[name],size_epsilon)#
					geom.set("size",str(size_ratio_dict[name]*size[name]))
					
					# rgb 見たいときは以下のプログラム
					#####					
					size_epsilon = 0.05
					if size_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-size_ratio_dict[name])/size_epsilon)*0.5
						other1 = 0.5 - ((1-size_ratio_dict[name])/size_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
					else: # big
						blue = 0.5 + ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						other2  = 0.5 - ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))
					#####
					
	#print("size_ratio",size_ratio)				
					
	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml',encoding='UTF-8')
	
	
	
	
	
def set_adv_size_multi(size_ratio): # lists


	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(multi).xml')

	root = tree.getroot()

	name_list = ["torso1","uwaist1","lwaist1","butt1",
				"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
				"right_uarm1","right_larm1","left_uarm1","left_larm1",
				"right_hand1","left_hand1","head1"]#19

	size = {"torso1":0.07,"uwaist1":0.06,"lwaist1":0.06,"butt1":0.09,
			"right_thigh1":0.06,"right_shin1":0.049,"right_foot1":0.035,"right_foot2":0.035,
			"left_thigh1":0.06,"left_shin1":0.049,"left_foot1":0.035,"left_foot2":0.035,
			"right_uarm1":0.04,"right_larm1":0.031,"left_uarm1":0.04,"left_larm1":0.031,
			"right_hand1":0.04,"left_hand1":0.04 ,"head1":0.09}#19

	size_ratio_dict = {}
	i = 0
	for name in name_list:# list=>dict
		size_ratio_dict[name] = size_ratio[i]
		i += 1
	
	for geom in root.iter("geom"):
		for name in name_list:
			if name in str(geom.attrib):
			
				if name in size.keys():	
					#size_ratio[name] = set_size(size[name],size_epsilon)#
					geom.set("size",str(size_ratio_dict[name]*size[name]))
					
					# rgb 見たいときは以下のプログラム
					#####
					size_epsilon = 0.01
					geom.set("rgba",str(1.0)+str(" ")+str(1.0)+str(" ")+str(1.0)+str(" 1")) 
					"""if size_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-size_ratio_dict[name])/size_epsilon)*0.5
						other1 = 0.5 - ((1-size_ratio_dict[name])/size_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
					else: # big
						blue = 0.5 + ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						other2  = 0.5 - ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))"""
					#####
					
	#print("size_ratio",size_ratio)				
					
	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(multi).xml',encoding='UTF-8')		
