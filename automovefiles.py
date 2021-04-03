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

def make_config_path(message):
    while True:
        path = input(message)
        if os.path.isdir(path):
            return path

def make_config_case():
    ignore_upper_and_lower_case = bool(input("should upper and lower case be ignored (1 Yes, 0 No)"))
    return ignore_upper_and_lower_case

def make_config_classes():
    all_classes_entered = False
    all_classes = []
    while not all_classes_entered:
        current_class_name = input("type the folder-name of the class (Example: English) (if you are done press enter)").strip()
        all_classes_entered = not (current_class_name and current_class_name.strip())
        if not all_classes_entered:
            all_classes.append(make_config_classes_aliases(current_class_name))
    return all_classes

def make_config_classes_aliases(current_class_name):
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
    return all_aliases_for_class

def make_config():
    config_source = make_config_path("please enter the folder that should be scanned")

    config_dest = make_config_path("please enter the folder the files should be moved to (parent of class names)")

    config_ignore_upper_and_lower_case = make_config_case()

    all_classes = make_config_classes()
    print("setup done")

    save_config(all_classes,config_source,config_dest,config_ignore_upper_and_lower_case)

def change_config():
    current_config = load_config()
    current_classes , current_source, current_dest, current_ignore_upper_and_lower_case = current_config
    print("current config:")
    print(current_config)
    change_what = input("What do you want to change: classes , source, dest, ignore upper and lower case")
    if  change_what == "classes":
        pass
    elif change_what == "source":
        pass
    elif change_what == "dest":
        pass
    elif change_what == "ingore upper and lower case" or change_what == "ingore case":
        pass

classes, source, dest, ignore_upper_and_lower_case = load_config()
if bool(input("would you like to change the current config ? (1 Yes, 0 No)").strip()):
    change_config()
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
                print(source+"/"+i,dest+"/"+classes[ii][0]+"/"+i)
                shutil.move(source+"/"+i,dest+"/"+classes[ii][0]+"/"+i) # move it

