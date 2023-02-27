import xml.etree.ElementTree as ET 
import time
import random

tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/a1_adv.xml')

root = tree.getroot()

size_ratio = {}


"""name_list = ["torso_geom","aux_1_geom","aux_2_geom","aux_3_geom","aux_4_geom"
			,"front_left_leg_geom","front_right_leg_geom","back_left_leg_geom","back_right_leg_geom"
			,"front_left_ankle_geom","front_right_ankle_geom","back_left_ankle_geom","back_right_ankle_geom"]"""
			
"""name_list = ["trunk_geom1","trunk_geom2","trunk_geom3"
			,"FR_hip_geom","FR_thigh_geom","FR_calf_geom","FR_toe_geom1","FR_toe_geom2"
			,"FL_hip_geom","FL_thigh_geom","FL_calf_geom","FL_toe_geom1","FL_toe_geom2"
			,"RR_hip_geom","RR_thigh_geom","RR_calf_geom","RR_toe_geom1","RR_toe_geom2"
			,"RL_hip_geom","RL_thigh_geom","RL_calf_geom","RL_toe_geom1","RL_toe_geom2"]"""
			
name_list = ["FR_hip_geom","FR_thigh_geom","FR_calf_geom","FR_toe_geom1","FR_toe_geom2"
			,"FL_hip_geom","FL_thigh_geom","FL_calf_geom","FL_toe_geom1","FL_toe_geom2"
			,"RR_hip_geom","RR_thigh_geom","RR_calf_geom","RR_toe_geom1","RR_toe_geom2"
			,"RL_hip_geom","RL_thigh_geom","RL_calf_geom","RL_toe_geom1","RL_toe_geom2"] #len

"""size = 		{"torso_geom":0.25,"aux_1_geom":0.08,"aux_2_geom":0.08,"aux_3_geom":0.08,"aux_4_geom":0.08
			,"front_left_leg_geom":0.08,"front_right_leg_geom":0.08,"back_left_leg_geom":0.08,"back_right_leg_geom":0.08
			,"front_left_ankle_geom":0.08,"front_right_ankle_geom":0.08,"back_left_ankle_geom":0.08,"back_right_ankle_geom":0.08}"""

size = {"FR_hip_geom":[0.04,0.04],"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008]
		,"FL_hip_geom":[0.04,0.04],"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008]
		,"RR_hip_geom":[0.04,0.04],"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008]
		,"RL_hip_geom":[0.04,0.04],"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008]}
			
"""size = {"trunk_geom1":[0.1335,0.066,0.057],"trunk_geom2":[0.0005,0.0005,0.0005],"trunk_geom3":[0.0005,0.0005,0.0005]
			,"FR_hip_geom":[0.04,0.04],"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008],"FR_toe_geom1":0.01,"FR_toe_geom2":0.02
			,"FL_hip_geom":[0.04,0.04],"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008],"FL_toe_geom1":0.01,"FL_toe_geom2":0.02
			,"RR_hip_geom":[0.04,0.04],"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008],"RR_toe_geom1":0.01,"RR_toe_geom2":0.02
			,"RL_hip_geom":[0.04,0.04],"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008],"RL_toe_geom1":0.01,"RL_toe_geom2":0.02}"""

size_epsilon = 0.5

def set_size(epsilon):
	seed = time.time() 
	r = random.random()	
	#ratio = 1.0 - epsilon + r*(epsilon*2)
	ratio = 1.0 #サイズ初期化したい時
	#new_size = size * ratio

	return ratio
	
def make_xml(my_list):
	my_xml = ""
	for i in range(len(my_list)):
		my_xml += str(my_list[i])
		my_xml += " "
	return my_xml

for geom in root.iter("geom"):
	for name in name_list:
		if name in str(geom.attrib):
		
			if name in size.keys():	
				size_ratio[name] = set_size(size_epsilon)#
				#print(size_ratio[name])
				size[name][-1] = size_ratio[name]*size[name][-1]
				xml = make_xml(size[name])
				geom.set("size",xml)
				#geom.set("size",str(size_ratio[name]*size[name][-1]))

#print("size_ratio",size_ratio)	

tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/a1_adv.xml',encoding='UTF-8')







def set_adv_length(length_ratio): # lists

	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/a1_adv.xml')

	root = tree.getroot()


	"""name_list = ["torso_geom","aux_1_geom","aux_2_geom","aux_3_geom","aux_4_geom"
				,"front_left_leg_geom","front_right_leg_geom","back_left_leg_geom","back_right_leg_geom"
				,"front_left_ankle_geom","front_right_ankle_geom","back_left_ankle_geom","back_right_ankle_geom"]"""
				
	"""name_list = ["trunk_geom1","trunk_geom2","trunk_geom3"
				,"FR_hip_geom","FR_thigh_geom","FR_calf_geom","FR_toe_geom1","FR_toe_geom2"
				,"FL_hip_geom","FL_thigh_geom","FL_calf_geom","FL_toe_geom1","FL_toe_geom2"
				,"RR_hip_geom","RR_thigh_geom","RR_calf_geom","RR_toe_geom1","RR_toe_geom2"
				,"RL_hip_geom","RL_thigh_geom","RL_calf_geom","RL_toe_geom1","RL_toe_geom2"]"""
				
	""""name_list = ["FR_hip_geom","FR_thigh_geom","FR_calf_geom"
				,"FL_hip_geom","FL_thigh_geom","FL_calf_geom"
				,"RR_hip_geom","RR_thigh_geom","RR_calf_geom"
				,"RL_hip_geom","RL_thigh_geom","RL_calf_geom"] #len"""
	name_list = ["FR_hip_geom","FR_thigh_geom","FR_calf_geom"
				,"FL_hip_geom","FL_thigh_geom","FL_calf_geom"
				,"RR_hip_geom","RR_thigh_geom","RR_calf_geom"
				,"RL_hip_geom","RL_thigh_geom","RL_calf_geom"]

	"""size = 		{"torso_geom":0.25,"aux_1_geom":0.08,"aux_2_geom":0.08,"aux_3_geom":0.08,"aux_4_geom":0.08
				,"front_left_leg_geom":0.08,"front_right_leg_geom":0.08,"back_left_leg_geom":0.08,"back_right_leg_geom":0.08
				,"front_left_ankle_geom":0.08,"front_right_ankle_geom":0.08,"back_left_ankle_geom":0.08,"back_right_ankle_geom":0.08}"""

	"""length = {"FR_hip_geom":[0.04,0.04],"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008]
			,"FL_hip_geom":[0.04,0.04],"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008]
			,"RR_hip_geom":[0.04,0.04],"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008]
			,"RL_hip_geom":[0.04,0.04],"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008]}"""
			
	length = {"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008]
			,"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008]
			,"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008]
			,"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008]}
				
	"""size = {"trunk_geom1":[0.1335,0.066,0.057],"trunk_geom2":[0.0005,0.0005,0.0005],"trunk_geom3":[0.0005,0.0005,0.0005]
				,"FR_hip_geom":[0.04,0.04],"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008],"FR_toe_geom1":0.01,"FR_toe_geom2":0.02
				,"FL_hip_geom":[0.04,0.04],"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008],"FL_toe_geom1":0.01,"FL_toe_geom2":0.02
				,"RR_hip_geom":[0.04,0.04],"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008],"RR_toe_geom1":0.01,"RR_toe_geom2":0.02
				,"RL_hip_geom":[0.04,0.04],"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008],"RL_toe_geom1":0.01,"RL_toe_geom2":0.02}"""
				
	geom_size = {"FR_hip_geom":[0.04,0.04],"FR_thigh_geom":[0.1,0.01225,0.017],"FR_calf_geom":[0.1,0.008,0.008]
				,"FL_hip_geom":[0.04,0.04],"FL_thigh_geom":[0.1,0.01225,0.017],"FL_calf_geom":[0.1,0.008,0.008]
				,"RR_hip_geom":[0.04,0.04],"RR_thigh_geom":[0.1,0.01225,0.017],"RR_calf_geom":[0.1,0.008,0.008]
				,"RL_hip_geom":[0.04,0.04],"RL_thigh_geom":[0.1,0.01225,0.017],"RL_calf_geom":[0.1,0.008,0.008]}
				
	geom_pos = {"FR_hip_geom":[0, -0.055, 0],"FR_thigh_geom":[0, 0, -0.1],"FR_calf_geom":[0, 0, -0.1],"FR_toe_geom1":[0, 0, -0.2],"FR_toe_geom2":[0, 0, -0.2]
				,"FL_hip_geom":[0, 0.055, 0],"FL_thigh_geom":[0,0, -0.1],"FL_calf_geom":[0, 0, -0.1],"FL_toe_geom1":[0, 0, -0.2],"FL_toe_geom2":[0, 0, -0.2]
				,"RR_hip_geom":[0, -0.055, 0],"RR_thigh_geom":[0, 0, -0.1],"RR_calf_geom":[0, 0, -0.1],"RR_toe_geom1":[0, 0, -0.2],"RR_toe_geom2":[0, 0, -0.2]
				,"RL_hip_geom":[0, 0.055, 0],"RL_thigh_geom":[0, 0, -0.1],"RL_calf_geom":[0, 0, -0.1],"RL_toe_geom1":[0, 0, -0.2],"RL_toe_geom2":[0, 0, -0.2]}
				
	body_pos = {"FR_thigh":[0,-0.08505,0],"FR_calf":[0,0,-0.2]
			,"FL_thigh":[0,0.08505,0],"FL_calf":[0,0,-0.2]
			,"RR_thigh":[0,-0.08505,0],"RR_calf":[0,0,-0.2]
			,"RL_thigh":[0,0.08505,0],"RL_calf":[0,0,-0.2]}
			
	depend = {"FR_hip_geom":["FR_thigh"],"FR_thigh_geom":["FR_calf"],"FR_calf_geom":["FR_toe_geom1","FR_toe_geom2"]
			,"FL_hip_geom":["FL_thigh"],"FL_thigh_geom":["FL_calf"],"FL_calf_geom":["FL_toe_geom1","FL_toe_geom2"]
			,"RR_hip_geom":["RR_thigh"],"RR_thigh_geom":["RR_calf"],"RR_calf_geom":["RR_toe_geom1","RR_toe_geom2"]
			,"RL_hip_geom":["RL_thigh"],"RL_thigh_geom":["RL_calf"],"RL_calf_geom":["RL_toe_geom1","RL_toe_geom2"]}

	length_epsilon = 0.05

	def set_size(epsilon):
		seed = time.time() 
		r = random.random()	
		ratio = 1.0 - epsilon + r*(epsilon*2)
		#ratio = 1.0 #サイズ初期化したい時
		#new_size = size * ratio

		return ratio
		
	def make_xml(my_list):
		my_xml = ""
		for i in range(len(my_list)):
			my_xml += str(my_list[i])
			my_xml += " "
		return my_xml

	length_ratio_dict = {}
	i = 0
	for name in name_list:# list=>dict
		length_ratio_dict[name] = length_ratio[i]
		i += 1

	for geom in root.iter("geom"):
		for name in name_list:
			if name in str(geom.attrib):
			
				if name in geom_size.keys():
					if len(geom_size[name]) == 2:
					
						geom_size[name][1] = geom_size[name][1] * length_ratio_dict[name]
						xml = make_xml(geom_size[name])
						geom.set("size",xml)
						
						body_pos[depend[name][0]][1] = body_pos[depend[name][0]][1] + geom_size[name][1] * (length_ratio_dict[name]-1.0)
						for body in root.iter("body"):
							if depend[name][0] in str(body.attrib):
								xml = make_xml(body_pos[depend[name][0]])
								body.set("pos",xml)
					
					elif len(geom_size[name]) == 3:
					
						geom_size[name][0] = geom_size[name][0] * length_ratio_dict[name]
						xml = make_xml(geom_size[name])
						geom.set("size",xml)
						
						geom_pos[name][2] = geom_pos[name][2] * length_ratio_dict[name]
						xml = make_xml(geom_pos[name])
						geom.set("pos",xml)
						
						if len(depend[name])==2:
							geom_pos[depend[name][0]][2] = geom_pos[depend[name][0]][2] * length_ratio_dict[name]
							geom_pos[depend[name][1]][2] = geom_pos[depend[name][1]][2] * length_ratio_dict[name]
							for geom2 in root.iter("geom"):
								if depend[name][0] in str(geom2.attrib) or depend[name][1] in str(geom2.attrib) :
									xml0 = make_xml(geom_pos[depend[name][0]])
									xml1 = make_xml(geom_pos[depend[name][1]])
									geom2.set("pos",xml0)
									geom2.set("pos",xml1)
								
						elif len(depend[name])==1:
							body_pos[depend[name][0]][2] = body_pos[depend[name][0]][2] * length_ratio_dict[name]
							for body in root.iter("body"):
								if depend[name][0] in str(body.attrib):
									xml = make_xml(body_pos[depend[name][0]])
									body.set("pos",xml)
					# rgb 見たいときは以下のプログラム
					#####
					length_epsilon = 0.05
					if length_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-length_ratio_dict[name])/length_epsilon)*0.5
						other1 = 0.5 - ((1-length_ratio_dict[name])/length_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) # rgb in boxes 
						#for geom3 in root.iter("geom"): # rgb in stl
						#		if depend[name][0] in str(geom3.attrib):
						#			geom3.set("rgba",xml0)
					else: # big
						blue = 0.5 + ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						other2  = 0.5 - ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1")) # rgb in boxes
					#####ssss	
						
					#length_ratio_dict[name] = set_size(length_epsilon)#
					#print(length_ratio_dict[name])
					#length[name][0] = length_ratio_dict[name]*length[name][0]
					#xml = make_xml(length[name])
					#geom.set("size",xml)
					#geom.set("size",str(length_ratio[name]*size[name][-1]))

	#print("size_ratio",size_ratio)	

	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/a1_adv.xml',encoding='UTF-8')
