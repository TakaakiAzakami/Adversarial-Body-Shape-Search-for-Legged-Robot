import xml.etree.ElementTree as ET 
import time
import random

tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/ant_adv.xml')

root = tree.getroot()

size_ratio = {}


name_list = ["torso_geom","aux_1_geom","aux_2_geom","aux_3_geom","aux_4_geom"
			,"front_left_leg_geom","front_right_leg_geom","back_left_leg_geom","back_right_leg_geom"
			,"front_left_ankle_geom","front_right_ankle_geom","back_left_ankle_geom","back_right_ankle_geom"]

size = 		{"torso_geom":0.25,"aux_1_geom":0.08,"aux_2_geom":0.08,"aux_3_geom":0.08,"aux_4_geom":0.08
			,"front_left_leg_geom":0.08,"front_right_leg_geom":0.08,"back_left_leg_geom":0.08,"back_right_leg_geom":0.08
			,"front_left_ankle_geom":0.08,"front_right_ankle_geom":0.08,"back_left_ankle_geom":0.08,"back_right_ankle_geom":0.08}

size_epsilon = 0.05

def set_size(size,epsilon):
	seed = time.time() 
	seed = 1
	random.seed(time.time())
	r = random.random()	
	ratio = 1.0 - epsilon + r*(epsilon*2)
	#ratio = 1.0 #サイズ初期化したい時
	new_size = size * ratio

	return ratio

for geom in root.iter("geom"):
	for name in name_list:
		if name in str(geom.attrib):
		
			if name in size.keys():	
				size_ratio[name] = set_size(size[name],size_epsilon)#
				geom.set("size",str(size_ratio[name]*size[name]))

				if size_ratio[name] < 1: #small
					red = 0.5 + ((1-size_ratio[name])/size_epsilon)*0.5
					other1 = 0.5 - ((1-size_ratio[name])/size_epsilon)*0.5
					geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
				else: # big
					blue = 0.5 + ((size_ratio[name]-1)/size_epsilon)*0.5
					other2  = 0.5 - ((size_ratio[name]-1)/size_epsilon)*0.5
					geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))
					
print("size_ratio",size_ratio)	

tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/ant_adv.xml',encoding='UTF-8')







def set_adv_size(size_ratio): # lists

	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/ant_adv.xml')

	root = tree.getroot()


	name_list = ["torso_geom","aux_1_geom","aux_2_geom","aux_3_geom","aux_4_geom"
				,"front_left_leg_geom","front_right_leg_geom","back_left_leg_geom","back_right_leg_geom"
				,"front_left_ankle_geom","front_right_ankle_geom","back_left_ankle_geom","back_right_ankle_geom"] # 13

	size = 		{"torso_geom":0.25,"aux_1_geom":0.08,"aux_2_geom":0.08,"aux_3_geom":0.08,"aux_4_geom":0.08
				,"front_left_leg_geom":0.08,"front_right_leg_geom":0.08,"back_left_leg_geom":0.08,"back_right_leg_geom":0.08
				,"front_left_ankle_geom":0.08,"front_right_ankle_geom":0.08,"back_left_ankle_geom":0.08,"back_right_ankle_geom":0.08}
				
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
					
					#geom.set("rgba",str(1.5)+str(" ")+str(1.5)+str(" ")+str(1.5)+str(" ")+str(1))
					
					
					size_epsilon = 0.05
					"""if size_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-size_ratio_dict[name])/size_epsilon)*0.5
						other1 = 0.5 - ((1-size_ratio_dict[name])/size_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
					else: # big
						blue = 0.5 + ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						other2  = 0.5 - ((size_ratio_dict[name]-1)/size_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))"""
						
						
	#print("size_ratio",size_ratio)	

	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/ant_adv.xml',encoding='UTF-8')	

