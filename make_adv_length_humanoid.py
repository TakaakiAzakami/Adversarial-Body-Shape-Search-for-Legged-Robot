# humanoid 長さ(length)変更攻撃
import xml.etree.ElementTree as ET 
import time
import random

tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml')


root = tree.getroot()
	
len_ratio = {} # 結果保存用
			
name_list = ["torso1","lwaist1","uwaist1","butt1",
			"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
			"right_uarm1","right_larm1","left_uarm1","left_larm1",
			"right_hand1","left_hand1","head1"] # 19

fromto = {"torso1":[0,-.07,0,0,.07,0],
		"uwaist1":[-.01,-.06,-.12,-.01,.06,-.12],
		"lwaist1":[0,-.06,0,0,.06,0],
		"butt1":[-.02,-.07,0,-.02,.07,0],
		
		"right_thigh1":[0,0,0,0,0.01,-.34],
		"right_shin1":[0,0,0,0,0,-.3],
		"right_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
		"right_foot2":[-0.04,0.01,0,0.16,0.040,0],
		"left_thigh1":[0,0,0,0,-0.01,-.34],
		"left_shin1":[0,0,0,0,0,-.3],
		"left_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
		"left_foot2":[-0.04,0.01,0,0.16,0.040,0],
		
		"right_uarm1":[0,0,0,.16,-.16,-.16],
		"right_larm1":[0.01,0.01,0.01,.17,.17,.17],
		"left_uarm1":[0,0,0,.16,.16,-.16],
		"left_larm1":[0.01,-0.01,0.01,.17,-.17,.17]} # 16

body_b = {"torso_b":[0,0,1.4],
		"lwaist_b":[-.01,0,-0.260],
		"pelvis_b":[0,0,-0.165],
		
		"right_thigh_b":[0,-0.1,-0.04],
		"right_shin_b":[0,0.01,-0.403],
		"right_foot_b":[0,0,-0.35],
		"left_thigh_b":[0,0.1,-0.04],
		"left_shin_b":[0,-0.01,-0.403],
		"left_foot_b":[0,0,-0.35],
		
		"right_upper_arm_b":[0,-0.17,0.06],
		"right_lower_arm_b":[.18,-.18,-.18],
		"left_upper_arm_b":[0,0.17,0.06],
		"left_lower_arm_b":[.18,.18,-.18],
				
		"right_hand1":[.18,.18,.18],
		"left_hand1":[.18,-.18,.18],} # 15
		
		
depend = {"left_thigh_b":"butt1",
		"left_shin_b":"left_thigh1",
		"left_foot_b":"left_shin1",	
		"right_thigh_b":"butt1",
		"right_shin_b":"right_thigh1",
		"right_foot_b":"right_shin1",
		
		"left_upper_arm_b":"torso1",
		"left_lower_arm_b":"left_uarm1",
		"right_upper_arm_b":"torso1",
		"right_lower_arm_b":"right_uarm1",
		
		"right_hand1":"right_larm1",
		"left_hand1":"left_larm1"} # 12 # torso1*2 butt1*2 例外処理 順番も左＝＞右が重要。
	
def set_geom(geom,epsilon):#geom = [0,0,0,0,0,0],epsilon=0.01
	new_geom = []
	dlt_geom = []
	
	seed = time.time() 
	r = random.random()	
	ratio = 1.0 - epsilon + r*(epsilon*2)
	#ratio = 1.0 # 戻す時
	
	new_geom.append(geom[0])#not need
	new_geom.append(geom[1])#not need
	new_geom.append(geom[2])#not need
	new_geom.append(geom[0] + (geom[3]-geom[0])*ratio)
	new_geom.append(geom[1] + (geom[4]-geom[1])*ratio)
	new_geom.append(geom[2] + (geom[5]-geom[2])*ratio)		
	
	for i in range(6):
		dlt_geom.append(new_geom[i] - geom[i])
	
	xml_geom = make_xml(new_geom)
	
	return ratio, dlt_geom, xml_geom
	
def set_geom2(geom,epsilon):
	new_geom = []
	dlt_geom = []
	
	seed = time.time() 
	r = random.random()	
	#ratio = 1.0 - epsilon + r*(epsilon*2)
	ratio = 1.0 # 戻す時
	
	new_geom.append(geom[0])
	new_geom.append(geom[1]*ratio)
	new_geom.append(geom[2])
	new_geom.append(geom[3])
	new_geom.append(geom[4]*ratio)
	new_geom.append(geom[5])
	
	for i in range(6):
		dlt_geom.append(new_geom[i] - geom[i])
	
	xml_geom = make_xml(new_geom)
	
	return ratio, dlt_geom, xml_geom

def set_body(body,dlt_geom):
	new_body = []
	for i in range(3):
		new_body.append(body[i] + dlt_geom[i+3])
	xml_body = make_xml(new_body)
	return xml_body
	
def set_body2(body,dlt_geom):
	new_body = []
	for i in range(3):
		new_body.append(body[i] + dlt_geom[i])
	xml_body = make_xml(new_body)
	return xml_body
	
def make_xml(my_list):
	my_xml = ""
	for i in range(len(my_list)):
		my_xml += str(my_list[i])
		my_xml += " "
	return my_xml

def get_body_from_geom(depend,value):
	keys = [k for k,v in depend.items() if v == value]
	return keys

len_epsilon = 0.1

for geom in root.iter("geom"):
	for name in name_list:
		if name in str(geom.attrib):
		
			if name in fromto.keys():
				if name == "butt1":
					len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),len_epsilon)#
					#print("*")
					geom.set("fromto",xml_geom)
				elif name == "uwaist1":
					len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),len_epsilon)#
					#print("**")
					geom.set("fromto",xml_geom)
				elif name == "lwaist1":
					len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),len_epsilon)#
					#print("**")
					geom.set("fromto",xml_geom)
				elif name == "torso1":
					len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),len_epsilon)#
					#print("**")
					geom.set("fromto",xml_geom)
				else:
					len_ratio[name], dlt_geom, xml_geom = set_geom(fromto.get(name),len_epsilon)#
					geom.set("fromto",xml_geom)
				
				
				
				for body in root.iter("body"):
					tmp_depend = get_body_from_geom(depend,name)	
					if len(tmp_depend) >= 1:
						if tmp_depend[0] in str(body.attrib):
							#print(name,"=>",tmp_depend[0])
							xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
							body.set("pos",xml_body)
					if len(tmp_depend) >= 2:
						if tmp_depend[1] in str(body.attrib):
							#print(name,"2","=>",tmp_depend[1])
							xml_body = set_body2(body_b[tmp_depend[1]],dlt_geom)#
							body.set("pos",xml_body)
							
				for geom in root.iter("geom"): # right_hand left_handでしか入らない
					tmp_depend = get_body_from_geom(depend,name)		
					if len(tmp_depend) == 1:
						if tmp_depend[0] in str(geom.attrib):
							#print(name,"=>",tmp_depend[0])
							xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
							geom.set("pos",xml_body)
							
			
#print("len_ratio",len_ratio,"\n") # length 比率　確認用

tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml',encoding='UTF-8')		

		
		
		
		
		
		
		
		
		
		
		
		
def set_adv_length(length_ratio): # length_list

	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml')

	root = tree.getroot()
				
	name_list = ["torso1","lwaist1","uwaist1","butt1",
				"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
				"right_uarm1","right_larm1","left_uarm1","left_larm1"] # 16

	fromto = {"torso1":[0,-.07,0,0,.07,0],
			"uwaist1":[-.01,-.06,-.12,-.01,.06,-.12],
			"lwaist1":[0,-.06,0,0,.06,0],
			"butt1":[-.02,-.07,0,-.02,.07,0],
			
			"right_thigh1":[0,0,0,0,0.01,-.34],
			"right_shin1":[0,0,0,0,0,-.3],
			"right_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
			"right_foot2":[-0.04,0.01,0,0.16,0.040,0],
			"left_thigh1":[0,0,0,0,-0.01,-.34],
			"left_shin1":[0,0,0,0,0,-.3],
			"left_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
			"left_foot2":[-0.04,0.01,0,0.16,0.040,0],
			
			"right_uarm1":[0,0,0,.16,-.16,-.16],
			"right_larm1":[0.01,0.01,0.01,.17,.17,.17],
			"left_uarm1":[0,0,0,.16,.16,-.16],
			"left_larm1":[0.01,-0.01,0.01,.17,-.17,.17]} # 16

	body_b = {"torso_b":[0,0,1.4],
			"lwaist_b":[-.01,0,-0.260],
			"pelvis_b":[0,0,-0.165],
			
			"right_thigh_b":[0,-0.1,-0.04],
			"right_shin_b":[0,0.01,-0.403],
			"right_foot_b":[0,0,-0.35],
			"left_thigh_b":[0,0.1,-0.04],
			"left_shin_b":[0,-0.01,-0.403],
			"left_foot_b":[0,0,-0.35],
			
			"right_upper_arm_b":[0,-0.17,0.06],
			"right_lower_arm_b":[.18,-.18,-.18],
			"left_upper_arm_b":[0,0.17,0.06],
			"left_lower_arm_b":[.18,.18,-.18],
					
			"right_hand1":[.18,.18,.18],
			"left_hand1":[.18,-.18,.18],} # 15
			
			
	depend = {"left_thigh_b":"butt1",
			"left_shin_b":"left_thigh1",
			"left_foot_b":"left_shin1",	
			"right_thigh_b":"butt1",
			"right_shin_b":"right_thigh1",
			"right_foot_b":"right_shin1",
			
			"left_upper_arm_b":"torso1",
			"left_lower_arm_b":"left_uarm1",
			"right_upper_arm_b":"torso1",
			"right_lower_arm_b":"right_uarm1",
			
			"right_hand1":"right_larm1",
			"left_hand1":"left_larm1"} # 12 # torso1*2 butt1*2 例外処理 順番も左＝＞右が重要。
			
	length_ratio_dict = {}
	i = 0
	for name in name_list: # list=>dict
		length_ratio_dict[name] = length_ratio[i]
		i += 1
	
	def set_geom(geom,ratio):#geom = [0,0,0,0,0,0],epsilon=0.01
		new_geom = []
		dlt_geom = []

		#ratio = 1.0 # 戻す時
		
		new_geom.append(geom[0])#not need
		new_geom.append(geom[1])#not need
		new_geom.append(geom[2])#not need
		new_geom.append(geom[0] + (geom[3]-geom[0])*ratio)
		new_geom.append(geom[1] + (geom[4]-geom[1])*ratio)
		new_geom.append(geom[2] + (geom[5]-geom[2])*ratio)		
		
		for i in range(6):
			dlt_geom.append(new_geom[i] - geom[i])
		
		xml_geom = make_xml(new_geom)
		
		return ratio, dlt_geom, xml_geom
		
	def set_geom2(geom,ratio):
		new_geom = []
		dlt_geom = []
		
		#ratio = 1.0 # 戻す時
		
		new_geom.append(geom[0])
		new_geom.append(geom[1]*ratio)
		new_geom.append(geom[2])
		new_geom.append(geom[3])
		new_geom.append(geom[4]*ratio)
		new_geom.append(geom[5])
		
		for i in range(6):
			dlt_geom.append(new_geom[i] - geom[i])
		
		xml_geom = make_xml(new_geom)
		
		return ratio, dlt_geom, xml_geom

	def set_body(body,dlt_geom):
		new_body = []
		for i in range(3):
			new_body.append(body[i] + dlt_geom[i+3])
		xml_body = make_xml(new_body)
		return xml_body
		
	def set_body2(body,dlt_geom):
		new_body = []
		for i in range(3):
			new_body.append(body[i] + dlt_geom[i])
		xml_body = make_xml(new_body)
		return xml_body
		
	def make_xml(my_list):
		my_xml = ""
		for i in range(len(my_list)):
			my_xml += str(my_list[i])
			my_xml += " "
		return my_xml

	def get_body_from_geom(depend,value):
		keys = [k for k,v in depend.items() if v == value]
		return keys

	for geom in root.iter("geom"):
		for name in name_list:
			if name in str(geom.attrib):
			
				if name in fromto.keys():
					if name == "butt1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("*")
						geom.set("fromto",xml_geom)
					elif name == "uwaist1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					elif name == "lwaist1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					elif name == "torso1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					else:
						len_ratio[name], dlt_geom, xml_geom = set_geom(fromto.get(name),length_ratio_dict[name])#
						geom.set("fromto",xml_geom)
					
					# rgb 見たいときは以下のプログラム
					#####
					"""length_epsilon = 0.05
					
					if length_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-length_ratio_dict[name])/length_epsilon)*0.5
						other1 = 0.5 - ((1-length_ratio_dict[name])/length_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
					else: # big
						blue = 0.5 + ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						other2  = 0.5 - ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))"""
					####
					
					for body in root.iter("body"):
						tmp_depend = get_body_from_geom(depend,name)	
						if len(tmp_depend) >= 1:
							if tmp_depend[0] in str(body.attrib):
								#print(name,"=>",tmp_depend[0])
								xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
								body.set("pos",xml_body)
						if len(tmp_depend) >= 2:
							if tmp_depend[1] in str(body.attrib):
								#print(name,"2","=>",tmp_depend[1])
								xml_body = set_body2(body_b[tmp_depend[1]],dlt_geom)#
								body.set("pos",xml_body)
								
					for geom in root.iter("geom"): # right_hand left_handでしか入らない
						tmp_depend = get_body_from_geom(depend,name)		
						if len(tmp_depend) == 1:
							if tmp_depend[0] in str(geom.attrib):
								#print(name,"=>",tmp_depend[0])
								xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
								geom.set("pos",xml_body)
				
	#print("len_ratio",len_ratio,"\n") # length 比率　確認用

	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(memo).xml',encoding='UTF-8')	







def set_adv_length_multi(length_ratio): # length_list

	tree = ET.parse('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(multi).xml')

	root = tree.getroot()
				
	name_list = ["torso1","lwaist1","uwaist1","butt1",
				"right_thigh1","right_shin1","right_foot1","right_foot2","left_thigh1","left_shin1","left_foot1","left_foot2",
				"right_uarm1","right_larm1","left_uarm1","left_larm1"] # 16

	fromto = {"torso1":[0,-.07,0,0,.07,0],
			"uwaist1":[-.01,-.06,-.12,-.01,.06,-.12],
			"lwaist1":[0,-.06,0,0,.06,0],
			"butt1":[-.02,-.07,0,-.02,.07,0],
			
			"right_thigh1":[0,0,0,0,0.01,-.34],
			"right_shin1":[0,0,0,0,0,-.3],
			"right_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
			"right_foot2":[-0.04,0.01,0,0.16,0.040,0],
			"left_thigh1":[0,0,0,0,-0.01,-.34],
			"left_shin1":[0,0,0,0,0,-.3],
			"left_foot1":[-0.04,-0.01,0,0.16,-0.040,0],
			"left_foot2":[-0.04,0.01,0,0.16,0.040,0],
			
			"right_uarm1":[0,0,0,.16,-.16,-.16],
			"right_larm1":[0.01,0.01,0.01,.17,.17,.17],
			"left_uarm1":[0,0,0,.16,.16,-.16],
			"left_larm1":[0.01,-0.01,0.01,.17,-.17,.17]} # 16

	body_b = {"torso_b":[0,0,1.4],
			"lwaist_b":[-.01,0,-0.260],
			"pelvis_b":[0,0,-0.165],
			
			"right_thigh_b":[0,-0.1,-0.04],
			"right_shin_b":[0,0.01,-0.403],
			"right_foot_b":[0,0,-0.35],
			"left_thigh_b":[0,0.1,-0.04],
			"left_shin_b":[0,-0.01,-0.403],
			"left_foot_b":[0,0,-0.35],
			
			"right_upper_arm_b":[0,-0.17,0.06],
			"right_lower_arm_b":[.18,-.18,-.18],
			"left_upper_arm_b":[0,0.17,0.06],
			"left_lower_arm_b":[.18,.18,-.18],
					
			"right_hand1":[.18,.18,.18],
			"left_hand1":[.18,-.18,.18],} # 15
			
			
	depend = {"left_thigh_b":"butt1",
			"left_shin_b":"left_thigh1",
			"left_foot_b":"left_shin1",	
			"right_thigh_b":"butt1",
			"right_shin_b":"right_thigh1",
			"right_foot_b":"right_shin1",
			
			"left_upper_arm_b":"torso1",
			"left_lower_arm_b":"left_uarm1",
			"right_upper_arm_b":"torso1",
			"right_lower_arm_b":"right_uarm1",
			
			"right_hand1":"right_larm1",
			"left_hand1":"left_larm1"} # 12 # torso1*2 butt1*2 例外処理 順番も左＝＞右が重要。
			
	length_ratio_dict = {}
	i = 0
	for name in name_list: # list=>dict
		length_ratio_dict[name] = length_ratio[i]
		i += 1
	
	def set_geom(geom,ratio):#geom = [0,0,0,0,0,0],epsilon=0.01
		new_geom = []
		dlt_geom = []

		#ratio = 1.0 # 戻す時
		
		new_geom.append(geom[0])#not need
		new_geom.append(geom[1])#not need
		new_geom.append(geom[2])#not need
		new_geom.append(geom[0] + (geom[3]-geom[0])*ratio)
		new_geom.append(geom[1] + (geom[4]-geom[1])*ratio)
		new_geom.append(geom[2] + (geom[5]-geom[2])*ratio)		
		
		for i in range(6):
			dlt_geom.append(new_geom[i] - geom[i])
		
		xml_geom = make_xml(new_geom)
		
		return ratio, dlt_geom, xml_geom
		
	def set_geom2(geom,ratio):
		new_geom = []
		dlt_geom = []
		
		#ratio = 1.0 # 戻す時
		
		new_geom.append(geom[0])
		new_geom.append(geom[1]*ratio)
		new_geom.append(geom[2])
		new_geom.append(geom[3])
		new_geom.append(geom[4]*ratio)
		new_geom.append(geom[5])
		
		for i in range(6):
			dlt_geom.append(new_geom[i] - geom[i])
		
		xml_geom = make_xml(new_geom)
		
		return ratio, dlt_geom, xml_geom

	def set_body(body,dlt_geom):
		new_body = []
		for i in range(3):
			new_body.append(body[i] + dlt_geom[i+3])
		xml_body = make_xml(new_body)
		return xml_body
		
	def set_body2(body,dlt_geom):
		new_body = []
		for i in range(3):
			new_body.append(body[i] + dlt_geom[i])
		xml_body = make_xml(new_body)
		return xml_body
		
	def make_xml(my_list):
		my_xml = ""
		for i in range(len(my_list)):
			my_xml += str(my_list[i])
			my_xml += " "
		return my_xml

	def get_body_from_geom(depend,value):
		keys = [k for k,v in depend.items() if v == value]
		return keys

	for geom in root.iter("geom"):
		for name in name_list:
			if name in str(geom.attrib):
			
				if name in fromto.keys():
					if name == "butt1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("*")
						geom.set("fromto",xml_geom)
					elif name == "uwaist1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					elif name == "lwaist1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					elif name == "torso1":
						len_ratio[name], dlt_geom, xml_geom = set_geom2(fromto.get(name),length_ratio_dict[name])#
						#print("**")
						geom.set("fromto",xml_geom)
					else:
						len_ratio[name], dlt_geom, xml_geom = set_geom(fromto.get(name),length_ratio_dict[name])#
						geom.set("fromto",xml_geom)
					
					# rgb 見たいときは以下のプログラム
					#####
					"""length_epsilon = 0.005
					if length_ratio_dict[name] < 1: #small
						red = 0.5 + ((1-length_ratio_dict[name])/length_epsilon)*0.5
						other1 = 0.5 - ((1-length_ratio_dict[name])/length_epsilon)*0.5
						geom.set("rgba",str(red)+str(" ")+str(other1)+str(" ")+str(other1)+str(" 1")) 
					else: # big
						blue = 0.5 + ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						other2  = 0.5 - ((length_ratio_dict[name]-1)/length_epsilon)*0.5
						geom.set("rgba",str(other2)+str(" ")+str(other2)+str(" ")+str(blue)+str(" 1"))"""
					#####
					
					for body in root.iter("body"):
						tmp_depend = get_body_from_geom(depend,name)	
						if len(tmp_depend) >= 1:
							if tmp_depend[0] in str(body.attrib):
								#print(name,"=>",tmp_depend[0])
								xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
								body.set("pos",xml_body)
						if len(tmp_depend) >= 2:
							if tmp_depend[1] in str(body.attrib):
								#print(name,"2","=>",tmp_depend[1])
								xml_body = set_body2(body_b[tmp_depend[1]],dlt_geom)#
								body.set("pos",xml_body)
								
					for geom in root.iter("geom"): # right_hand left_handでしか入らない
						tmp_depend = get_body_from_geom(depend,name)		
						if len(tmp_depend) == 1:
							if tmp_depend[0] in str(geom.attrib):
								#print(name,"=>",tmp_depend[0])
								xml_body = set_body(body_b[tmp_depend[0]],dlt_geom)#
								geom.set("pos",xml_body)
				
	#print("len_ratio",len_ratio,"\n") # length 比率　確認用

	tree.write('/home/takaaki/.local/lib/python3.8/site-packages/gym/envs/mujoco/assets/humanoid4(multi).xml',encoding='UTF-8')	




