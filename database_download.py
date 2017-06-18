import os
os.chdir("/home/tyron/wget")


beginning="http://crashdb.agu.ch/"
#url="http://crashdb.agu.ch/showfolder.php?directory=HS_09/asc/SAE_J211/NA32_(stossend)&type=asc%20pdf%20jpg%20txt%20pr"
#False#
test=""

def brackets(word):
	new_word=word
	if word.find("(")!=-1:
		new_word=word.replace("(","")
		new_word=new_word.replace(")","")
		print "nnnnnnnnnnn",new_word
		
	if word.find(" ")!=-1:
		new_word=word.replace(" ","_")
		print "nnnnnnnnnnn",new_word
		
	return new_word
	
def recursive(url,ext):
	global test
	global done
	
	os.system("wget \"" +url+ "\" -P /home/tyron/wget -O temp.html")
	with open ("./temp.html", "r") as myfile:
		root=myfile.read().replace('\n', '')
		
	if not done:
		start=root.find("javascript:show_dir(\'")+len("javascript:show_dir(\'")
		end=root.find("/",start)
		test=root[start:end]
		print test
		done=True
		
	start=0
	end=0
	for folder in range(0, root.count("javascript:show_dir(\'")):
		start= root.find("javascript:show_dir(\'",start) + 21
		end=root.find("\'", start)
		#print start
		#print end
		folder=root[start:end]  
		print folder   
		print "http://crashdb.agu.ch/showfolder.php?directory="+folder+"&type=asc%20pdf%20jpg%20txt%20pr"
		recursive("http://crashdb.agu.ch/showfolder.php?directory="+folder+"&type=asc%20pdf%20jpg%20txt%20pr",ext)  
		 
	start=0
	end=0
	istart=0
	iend=0
	for pic in range (0, root.count("./datafiles/")):
		
		print "in"
		start= root.find("./datafiles/",start) + 12
		end=root.find("\"", start)
		#print start
		#print end
		pic=root[start:end] 
		if pic.find("avi")==-1:
			istart= root.find(test+"/"+ext+"/") + len(test+"/"+ext+"/")
			iend=root.find(".",istart)
			name= root[istart:iend]  
			iend= name.rfind("/")
			name=name[:iend]
			print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" , name
			print "/home/tyron/8/"+test+"/"+name     
			print pic 
			name=brackets(name)
			#pic=brackets(pic)
			print name 	
			os.system("wget \"http://crashdb.agu.ch/datafiles/"+pic+"\" -P /home/tyron/8/"+test+"/"+name)#+"/"+name+"/")#+"/"+name)
		
	return	
	

#196,197
inc=[65,81]#,,199,200,201,202,203,204,205,206,207,208] # #restart 202
for i in inc:
	done=False      	
	#recursive("http://crashdb.agu.ch/details.php?crash_id="+str(i),"jpg")
	recursive("http://crashdb.agu.ch/details.php?crash_id="+str(i),"asc")
	

		
		
'''start=len("http://crashdb.agu.ch/showfolder.php?directory=")
end=url.find("/",start)
name=url[start:end]
print name
start=end+1
end=start+3
ext=url[start:end]
print ext


start=url.find(ext+"/")+len(ext+"/")
end=url.find("&")
directories=url[start:end]
print directories


#print root		            
#length=len(start)
for pic in range (0, root.count("./datafiles/"+name+"/"+ext+"/"+directories)):
	print "in"
	start= root.find("./datafiles/"+name+"/"+ext+"/"+directories,start) + 12 + len(name) + len(directories)+len("/"+ext+"/")
        end=root.find("\"", start)
	#print start
	#print end
	pic=root[start:end]              	
	os.system("wget \"http://crashdb.agu.ch/datafiles/"+name+"/"+ext+"/"+directories+"/"+pic+"\" -P /home/tyron/wget/folder")
'''
