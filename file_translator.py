#!/usr/bin/env python2

import sys
import os
import shutil
import time
import re
import glob

'''def extract_implant(directory):
	
	folders=os.listdir(directory)
	#print folders
	for folder in folders:
		directory="/home/tyron/AGU_Database"
		if not os.path.exists(directory+"/"+folder+"/Data"): 
			os.makedirs(directory+"/"+folder+"/Data")
			
		#os.makedirs(directory+"/"+folder+"/Videos")
		#.makedirs(directory+"/"+folder+"/PDF")
			
		moves= os.listdir(directory+"/"+folder+"/crashdb.agu.ch/datafiles/"+folder+"/avi")
		#print moves
		for move in moves:
			os.rename(directory+"/"+folder+"/crashdb.agu.ch/datafiles/"+folder+"/avi/"+move, directory+"/"+folder+"/"+move)
		
		moves= os.listdir(directory+"/"+folder+"/crashdb.agu.ch/datafiles/"+folder+"/pdf")	
		#print moves
		for move in moves:
			os.rename(directory+"/"+folder+"/crashdb.agu.ch/datafiles/"+folder+"/pdf/"+move, directory+"/"+folder+"/"+move)	
		
		shutil.rmtree(directory+"/"+folder+"/crashdb.agu.ch")
						


extract_implant()'''
 


german_triple=["nach_dem_Unfall","vor_dem_Unfall"]
german_double=["nach_dem","vor_dem","Bilder_10ms","Bilder_20ms","20ms_Bilder","10ms_Bilder"]

german_single = ["vorschaden","Stossstangenaufbau","mit","Stossstange","ohne","stossend","gestossen","Versuchsaufbau","Testkonfiguration","heck","Proband","Endstellung",
"Kollisionsendlage","Kollisionsstellung","Versuchseinrichtung","Schadenkalkulation","Messprotokolle","Messprotokoll","Vermessung",
"Zusaetzliche","Bilder","Vergleich","Laservermessung","messdaten","Bildsequenzen","Videoanalyse","uebersicht","oben","Schadenbeschrieb",
"Echtzeit","links","recht","gebremst","ungebremst","Skizzen","beide","Fahrzeuge","vorne","vor","nach","seite","Graphen","Konstellation",
"dummybelastung","detail","Kollisionsablauf","crashformular","daten","kopie","unten","auspuff","hinten","kupplung","versuch","fluegel",
"schaden","konfiguration","kofferraum","Geschwindigkeit-Messung","fahrerdummy","von","standlicht","heckansicht","heckblech","innen",
"offen","heckklappe","fahrzeugzusammenstellung","versuchskonstellation","postkoll","heckpartie","frontpartie","draufsicht","dach",
"bodenblech","schnitt","ansichten","haube","schminke","neu","bremsversuche","auswertung","unbeladen","fahrer","dummydaten","fahrzeug",
"becken","kopf","zusammenfassung","nackenmomente","brust","hinter"]

english_triple=["Post_Test","Pre_Test"]
english_double=["Post","Pre","Images_10ms_Interval","Images_20ms_Interval","Images_20ms_Interval","Images_10ms_Interval"]
english_single=["Pre_Test_Damage","Bumper_Design","With","Bumper","Without","Impinging","Impinged","Testhall","Test_Setup","Rear","Experimentee","End_Position",
"End_Position","Collision_Setup","Test_Equipment","Damage_Calculation","Measurement_Protocols","Measurement_Protocols","Measurements","Additional",
"Images","Comparison","Laser_Measurement","Data","High_Speed_Images","Video_Analysis","Overview","Top","Damage","Real_Time","left","right",
"Braked","Unbraked","Sketches","Both","Vehicles","Front","Pre","Post","Side","Graphs","Car_Line_Up","Dummy_Load","Close_Up","Collision_Sequence",
"Crash_Analysis","Data","Copy","Underside","Exhaust","Rear","Towbar","Test","Side","Damage","Setup","Boot","Speed_Measurement","Dummy",
"from","sidelight","Rear_View","Rear_Panel","Inside","Open","Hatchback","Vehicle_Arrangement","Test_Setup","Post_Test","Rear_End_Collision",
"Front_End_Collision","Top_View","Roof","Floor_Panel","Section","Views","Hood","Liner","new","Brake_Test","Analysis","No_Load","Driver",
"Dummy_Data","Vehicle","Pelvis","Nose","Summary","Neck_Moments","Chest","Rear"]

#### stick in 3 folders
def delete_list(lst,mylist):
	lst.sort(reverse=True)
	print mylist
	for index in lst:
	    del mylist[index]

def search(target,word):
	for char in word:
		if char==" ":
			return True
	return False
	
def parse(word):
	
	if word.find(" ")!=-1:
		word=word.replace(" ","_")
	if word.find("%20")!=-1:
		word=word.replace("%20","_")
		
	wrds=word.split(".")
	if len(wrds)>1:
		ext="."+wrds[-1]
	else:
		ext=""
	
	words=wrds[0].split("_")
	
	'''for word in old_words:
		'''
	
	length = len(words)
	delete=[]
	if length>2:
		for j in range(len(words)-2):
			for i in range(len(german_triple)):
				if re.search(german_triple[i],words[j]+"_"+words[j+1]+ "_"+words[j+2], re.IGNORECASE):
						words[j]=english_triple[i]
				    		delete.extend((j+1,j+2))
						j+=2
					 	break 
				elif re.search(german_triple[i]+"*",words[j]+"_"+words[j+1]+ "_"+words[j+2], re.IGNORECASE): 
					
					match = re.match(r"([a-z]+)([0-9]+)", words[j]+"_"+words[j+1]+ "_"+words[j+2], re.I)
					if match:
				    		parts=match.groups()
				    		if re.search(german_triple[i],parts[0], re.IGNORECASE):
				    			words[j]=english_triple[i]+parts[1]
				    			delete.extend((j+1,j+2))
							j+=2
					 		break
		
		for j in range(len(words)-1):
			for i in range(len(german_double)): 
				if re.search(german_double[i],words[j]+"_"+words[j+1], re.IGNORECASE):
					words[j]=english_double[i]
		    			delete.append(j+1)
					j+=1
					break
				elif re.search(german_double[i]+"*",words[j]+"_"+words[j+1], re.IGNORECASE):
					
					match = re.match(r"([a-z]+)([0-9]+)", words[j]+"_"+words[j+1], re.I)
					if match:
				    		parts=match.groups()
				    		if re.search(german_double[i],parts[0], re.IGNORECASE):
				    			words[j]=english_double[i]+parts[1]
				    			delete.append(j+1)
							j+=1
							break
					 
					 #print words[j]+"_"+words[j+1]
					 #print german_double[i]
					 #words[j]=english_double[i]
					 #print words
					 
					 	
		for k in range(len(words)):
			for i in range(len(german_single)):
				if re.search(german_single[i],words[k], re.IGNORECASE):
					words[k]=english_single[i]
					break
				elif re.search(german_single[i]+"*",words[k], re.IGNORECASE):
					
					match = re.match(r"([a-z]+)([0-9]+)", words[k], re.I)
					if match:
				    		parts=match.groups()
				    		if re.search(german_single[i],parts[0], re.IGNORECASE):
				    			words[k]=english_single[i]+parts[1]
							break
				
					
					
		
		#print delete
		if delete:			
			delete_list(delete,words)		
		return "_".join(words)+ ext
		
		
	elif length>1:
		#print "length>1"
		for j in range(len(words)-1):
			for i in range(len(german_double)): 
				if re.search(german_double[i],words[j]+"_"+words[j+1], re.IGNORECASE):
					words[j]=english_double[i]
		    			delete.append(j+1)
					j+=1
					break
				elif re.search(german_double[i]+"*",words[j]+"_"+words[j+1], re.IGNORECASE):
					
					match = re.match(r"([a-z]+)([0-9]+)", words[j]+"_"+words[j+1], re.I)
					if match:
				    		parts=match.groups()
				    		if re.search(german_double[i],parts[0], re.IGNORECASE):
				    			words[j]=english_double[i]+parts[1]
				    			delete.append(j+1)
							j+=1
							break
					 	
		for k in range(len(words)):
			for i in range(len(german_single)):
				if re.search(german_single[i],words[k], re.IGNORECASE):
					words[k]=english_single[i]
					break
				elif re.search(german_single[i]+"*",words[k], re.IGNORECASE):
					
					match = re.match(r"([a-z]+)([0-9]+)", words[k], re.I)
					if match:
				    		parts=match.groups()
				    		if re.search(german_single[i],parts[0], re.IGNORECASE):
				    			words[k]=english_single[i]+parts[1]
							break
					
		if delete:			
			delete_list(delete,words)		
		return "_".join(words)+ ext
	else:
		for k in range(len(words)):
			for i in range(len(german_single)):
				if(words[k]=="Stossstangenaufbau"):
					print german_single[i]
				if re.search(german_single[i],words[k], re.IGNORECASE):
					words[k]=english_single[i]
					break
				elif re.search(german_single[i]+"*",words[k], re.IGNORECASE):
					print"what"
					match = re.match(r"([a-z]+)([0-9]+)", words[k], re.I)
					if match:
						print"what"
				    		parts=match.groups()
				    		if re.search(german_single[i],parts[0], re.IGNORECASE):
				    			words[k]=english_single[i]+parts[1]
							break
					
		if delete:			
			delete_list(delete,words)		
		return "_".join(words) + ext
				
####test with strings
def recursive_rename(directory):
		folders=os.listdir(directory)
		print folders
		if folders:
			#i=0
			original=[]
			do=False
			for folder in folders:
				print folder
				new_name=parse(folder)
				
				if new_name != folder and os.path.exists(directory+"/"+new_name):
					#print "a"
					try:
						original.index(new_name)
					except:
						original.append(new_name)
					#print "b"
					parts=new_name.split(".")
					#print parts
					counter = len(glob.glob1(directory+"/",parts[0]+"*"))+1
					#print len(parts)
					if len(parts)>1:
						#print "d"
						num=str(counter)
						parts[0]+=num.zfill(3)
						#print "e"
						#i+=1
					new_name=".".join(parts)
					#print "f"
					do=True
					#print "g"
				
				os.rename(directory+"/"+folder, directory+"/"+new_name)	
				print new_name	
				
				try:
					os.chdir(directory+"/"+new_name)
					recursive_rename(directory+"/"+new_name)
				except:
					print "out"
			if do:
				for name in original:
					names=name.split(".")
					os.rename(directory+"/"+name, directory+"/"+names[0]+"001"+names[1])
					if len(original)>1: #meaning there's different picture types in one folder e.g. oben,close_up etc
						lst=(glob.glob1(directory+"/",names[0]+"*"))
						os.makedirs(directory+"/"+names[0])
						for l in lst:
							os.rename(directory+"/"+l, directory+"/"+names[0]+"/"+l)
			return
exts=["/PDFs","/Videos","/Pictures","/Data"]
def implant(directory):
	folders=os.listdir(directory)
	for folder in folders:
		for i in exts:
			if not os.path.exists(directory+"/"+folder+i): 
				os.makedirs(directory+"/"+folder+i)
			
			
def vermessung(directory):
	folders=os.listdir(directory)
	for folder in folders:
		if os.path.exists(directory+"/"+folder+"/Measurements"): 
			vermess=os.listdir(directory+"/"+folder+"/Measurements")
			for i in vermess:
				try:
					os.listdir(directory+"/"+folder+"/Measurements/"+i)
					txt=(glob.glob1(directory+"/"+folder+"/Measurements/"+i,"*txt"))
					print txt
					print len(txt)
					if len(txt)>0:
						if not os.path.exists(directory+"/"+folder+"/Data/Measurements/"+i): 
							os.makedirs(directory+"/"+folder+"/Data/Measurements/"+i)
						print "in"
						for t in txt:
							print "in"
							print directory+"/"+folder+"/Measurements/"+i+"/"+t
							print directory+"/"+folder+"/Data/Measurements/"+i
							os.rename(directory+"/"+folder+"/Measurements/"+i+"/"+t, directory+"/"+folder+"/Data/Measurements/"+i+"/"+t)
				except:
					print "boo"
			

recursive_rename("/home/tyron/6")
implant("/home/tyron/6")
vermessung("/home/tyron/6")

