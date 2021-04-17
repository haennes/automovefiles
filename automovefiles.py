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
    ignore_upper_and_lower_case = bool(int(input("should upper and lower case be ignored (1 Yes, 0 No)")))
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
    change_what = input("What do you want to change: classes , source, dest, ignore_upper_and_lower_case  (seperate multiple with spaces)").split()
    
    if  "classes" in change_what:
        print("current classes",current_classes)
        classes_to_change_indexes = input("what class(es) do you want to change ? (seperate them by a space) (enter the indexes (0 = first))").split()
        for i in classes_to_change_indexes:
            delete_class = bool(int(input("do you want to delete this class ? (Yes 1 ,No 0)")))
            if delete_class:
                current_classes.pop(int(i))
            else:
                aliases_to_change_indexes = input("what aliases do you want to change ? (seperate them by a space) (0 for Foldername)").split()
                for ii in aliases_to_change_indexes:
                    delete_alias = bool(int(input("do you want to delete this alias ? (Yes 1 ,No 0)")))
                    if delete_alias:
                        current_classes[int(i)].pop(int(ii))
                        continue
                    new_alias = input("Enter the name you want "+ ii +"to change to.").split()[0]
                    if new_alias == "":
                        current_classes[i].pop(ii)
                    else:
                        current_classes[int(i)][int(ii)] = new_alias


    if "source" in change_what:
        current_source = make_config_path("please enter the folder that should be scanned")

    if "dest" in change_what:
        current_dest = make_config_path("please enter the folder the files should be moved to (parent of class names)")

    if "ignore_upper_and_lower_case" in change_what or "ignore_case" in change_what:
        current_ignore_upper_and_lower_case = make_config_case()

    save_config(current_classes,current_source,current_dest,current_ignore_upper_and_lower_case)

classes, source, dest, ignore_upper_and_lower_case = load_config()

if bool(int(input("would you like to change the current config ? (1 Yes, 0 No)"))):
    change_config()
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
                print(source+"/"+i,"->",dest+"/"+classes[ii][0]+"/"+i)
                shutil.move(source+"/"+i,dest+"/"+classes[ii][0]+"/"+i) # move it

