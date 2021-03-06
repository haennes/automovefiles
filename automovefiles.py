import os
import shutil
import pickle

def print_list_pretty(bullet_char : str,_list : list,indent_level: int = 0):
    for i in _list:
        if i is list or i is set or i is tuple:
            print_list_pretty(bullet_char,i,indent_level+1)
        else:
            tabs = ""
            for ii in range(indent_level):
                tabs += "\t"
            print(tabs+bullet_char+str(i))


def save_config(_classes,_source,_dest,_ignore_upper_and_lower_case,_confimation_needed):
    f = open("automovefiles_config.pckl","wb")
    pickle.dump([_classes,_source,_dest,_ignore_upper_and_lower_case,_confimation_needed],f)
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
    print("next you can enter aliases for the subject"+current_class_name)
    while not all_aliases_for_class_entered:
        current_alias_for_current_class = input("Please enter another alias for the subject (if you are done press enter)").strip()
        all_aliases_for_class_entered = not (current_alias_for_current_class and current_alias_for_current_class.strip())
        if not all_aliases_for_class_entered:
            all_aliases_for_class.append(current_alias_for_current_class)
            print("entered aliases for ",current_class_name,":" , all_aliases_for_class)
        else: print("all aliases for ",current_class_name,"entered :",all_aliases_for_class)
    all_aliases_for_class.insert(0,current_class_name)
    return all_aliases_for_class

def make_config_confirmation_needed():
    confirmation_needed = bool(int(input("Should you be asked before moving the file ? (1 Yes, 0 No)")))
    return confirmation_needed

def make_config():
    config_source = make_config_path("please enter the folder that should be scanned")

    config_dest = make_config_path("please enter the folder the files should be moved to (parent of class names)")

    config_ignore_upper_and_lower_case = make_config_case()

    all_classes = make_config_classes()

    config_confirmation_needed = make_config_confirmation_needed()
    print("setup done")

    save_config(all_classes,config_source,config_dest,config_ignore_upper_and_lower_case,config_confirmation_needed)

def change_config():
    current_config = load_config()
    current_classes , current_source, current_dest, current_ignore_upper_and_lower_case, current_confirmation_needed = current_config
    print("current config:")
    print(current_config)
    change_what = input("What do you want to change: classes , source, dest, ignore_upper_and_lower_case, confirmation_needed  (seperate multiple with spaces)").split()
    
    if  "classes" in change_what:
        print("current classes",current_classes)
        add_class = bool(int(input("do you want to add a class ? (Yes 1,No 0)")))
        if add_class:
            class_name = input("What should the class be called ?")
            aliases = make_config_classes(class_name)
            current_classes.append(aliases)
        classes_to_change_indexes = input("what class(es) do you want to change ? (seperate them by a space) (enter the indexes (0 = first))").split()
        for i in classes_to_change_indexes:
            delete_class = bool(int(input("do you want to delete the class "+current_classes[int(i)][0]+"? (Yes 1 ,No 0)")))
            if delete_class:
                current_classes.pop(int(i))
            else:
                add_alias = bool(int(input("do you want to add a alias ? (Yes 1,No 0)")))
                if add_alias:
                    alias_names = input("what aliases should be added (seperate by spaces)").split()
                    for alias_name in alias_names:
                        current_classes[int(i)].append(alias_name)
                aliases_to_change_indexes = input("what aliases do you want to change ? current aliases: "+str(current_classes[int(i)])+" (seperate them by a space) (0 for Foldername)").split()
                for ii in aliases_to_change_indexes:
                    delete_alias = bool(int(input("do you want to delete the alias "+current_classes[int(i)][int(ii)]+" ? (Yes 1 ,No 0)")))
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
    
    if "confirmation_needed" in change_what:
        current_confirmation_needed = make_config_confirmation_needed()

    save_config(current_classes,current_source,current_dest,current_ignore_upper_and_lower_case,current_confirmation_needed)

classes, source, dest, ignore_upper_and_lower_case, confirmation_needed = load_config()
save_config(classes,source,dest,ignore_upper_and_lower_case,confirmation_needed)

if bool(int(input("would you like to change the current config ? (1 Yes, 0 No)"))):
    change_config()
    classes, source, dest, ignore_upper_and_lower_case, confirmation_needed = load_config()

print_list_pretty("-",load_config(),0)
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
                if confirmation_needed:
                    moving = bool(int(input("should " + source+"/"+i +" be moved to "+ dest +"/"+classes[ii][0]+"/"+i+" (1 Yes, 0 No)" )))
                else:
                    moving = True
                if moving:
                    print(source+"/"+i,"->",dest+"/"+classes[ii][0]+"/"+i)
                    shutil.move(source+"/"+i,dest+"/"+classes[ii][0]+"/"+i) # move it

