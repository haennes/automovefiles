import os
import shutil
import pickle


def save_config(_classes,_source,_dest,_ignore_upper_and_lower_case):
    f = open("automovefiles_config.pckl","wb")
    pickle.dump([_classes,_source,_dest,_ignore_upper_and_lower_case],f)
    f.close()


def load_config():
    try:
        f = open("automovefiles_config.pckl","rb")
    except:
        make_config()
        f = open("automovefiles_config.pckl","rb")
    to_return = pickle.load(f)
    f.close()
    return to_return

def make_config():
    while True:
        config_source = input("please enter the folder that should be scanned")
        if os.path.isdir(config_source):
            break
    while True:
        config_dest = input("please enter the folder the files should be moved to (parent of class names)")
        if os.path.isdir(config_dest):
            break
    config_ignore_upper_and_lower_case = bool(input("should upper and lower case be ignored (1 Yes, 0 No)"))
    all_classes_entered = False
    all_classes = []
    while not all_classes_entered:
        current_class_name = input("type the folder-name of the class (Example: English) (if you are done press enter)").strip()
        all_classes_entered = not (current_class_name and current_class_name.strip())
        if all_classes_entered:
            break
        all_aliases_for_class_entered = False
        all_aliases_for_class = []
        print("next you can enter aliases for the subject")
        while not all_aliases_for_class_entered:
            current_alias_for_current_class = input("Please enter another alias for the subject (if you are done press enter)").strip()
            all_aliases_for_class_entered = not (current_alias_for_current_class and current_alias_for_current_class.strip())
            if not all_aliases_for_class_entered:
                all_aliases_for_class.append(current_alias_for_current_class)
                print("entered aliases for ",current_class_name,":" , all_aliases_for_class)
            else: print("all aliases for ",current_class_name,"entered :",all_aliases_for_class)
        all_aliases_for_class.insert(0,current_class_name)
        if not all_classes_entered:
            all_classes.append(all_aliases_for_class)
        else: print("setup done")



    save_config(all_classes,config_source,config_dest,config_ignore_upper_and_lower_case)




classes, source, dest, ignore_upper_and_lower_case = load_config()
print(load_config())
files = os.listdir(source)
print(files)


for i in files: 
    if i.find(".") != -1: # checking if file is not a folder
        b = i
        if ignore_upper_and_lower_case:
            b = i.lower()
        for ii in range(len(classes)): # going through each class
            found = False
            for iii in classes[ii]: #checking if any alias is contained in the filename
                if b.find(iii)!= -1 or b.find(iii.lower())!= -1: # if so
                    found = True
            if found:  
                print(source+"/"+i,source+"/"+classes[ii][0]+"/"+i)
                shutil.move(source+"/"+i,dest+"/"+classes[ii][0]+"/"+i) # move it

