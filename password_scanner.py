import re
import sys

def scan_pwd_names_file(pwd_file, pwd_id_list):
    for name in pwd_file: 
        name = name.strip()
        if (name not in pwd_id_list):
            if (name[-1::] == '\n'):
                pwd_id_list.append(name[:-1:]) #do not include newline char in list
            else:
                pwd_id_list.append(name) #last name in file does not have a newline char

def find_hardcoded_pwds(dictionary, target_file, password_id_list):

    code = target_file.read() # store the code that is going to be analyzed

    #iterate through the possible password name list and check code for them.
    for id in password_id_list:
        #regex to match hardcoded passwords
        '''
        \b{id}\b - capture any variable names that match the possible password variable list
        \s*=\s* - assignment will have an equal sign with an unknown amount of whitespace before and after it
        \" - a quotation will follow if it is a hardcoded string
        (.*?) - . matches any token other than newline, * means it can be 0 or more tokens,
                 and ? makes it non-greedy so it stops after the first match of the string pattern
        \" - ending quotation for assignment

        ex: should match something like pwd = "my_password"
        '''
        pwd_re = rf"\b{id}\b\s*=\s*\"(.*?)\"" 

        #search the file for regex matches
        match = re.search(pwd_re, code)
        
        #if a match is found then store it in the dictionary 
        if match:
            pwd = match.group(1) # hardcoded password that was found by regex
            dictionary[id] = (pwd, match.start()) # store variable and password in dictionary
            print(f"Found: {match.group()} at position {match.start()}") #output message when a match is found
    
def log_results(results):

    #store number of hardcoded passwords found in code
    pwd_list_size = len(results) 

    #only write a log if a hardcoded password was found
    if (pwd_list_size > 0):
        #open new file to store log for results
        hardcoded_pwds = open("hardcoded_pwds_output.txt", "w")

        #write the total number of passwords found at the top of the file
        hardcoded_pwds.write( str(pwd_list_size) + " hardcoded passwords found!\n")

        #iterate through dict and write results of search for hardcoded passwords
        for key, (value, code_pos) in results.items():
            #write the var_name the password and the position in the code it was found
            hardcoded_pwds.write(key + " = \"" + value + "\" at code position " + str(code_pos) + "\n")

        #close file when finished    
        hardcoded_pwds.close()

def main(*args):
    #create list to store possible var names for hardcoded passwords
    password_id_list = [] 

    #catch file not found errors
    try:
        #file contains possible password variable names to search for
        pwd_id_file = open("possible_pwd_identifiers.txt", "r") 
    except:
        raise FileNotFoundError

    #build an iterable list of possible variable names for hardcoded pwds
    scan_pwd_names_file(pwd_id_file, password_id_list) 

    #close file when finished using
    pwd_id_file.close() 

    #get file name from arguments
    if len(sys.argv) > 2:
        print("Too many cmd line arguments provided.\nFormat is 'py ./password_scanner.py <file_name>'")
    else:
        file_name = sys.argv[1] # second cmd line arg should be target file since first is the program name


    #catch file not found errors
    if not file_name:
        print("No file provided to analyze. Format is 'py ./password_scanner.py <file_name>'")
    try:
        target_file = open(file_name, "r")
    except:
        raise FileNotFoundError
    else:

        #dictionary to store any hardcoded passwords that are found.
        #Value is a tuple of the password and the position in thecode it was found.
        #Format is {var_name: (hardcoded_pwd, code_position)}
        found_pwds = {}

        #search target file for hardcoded passwords
        find_hardcoded_pwds(found_pwds, target_file, password_id_list) 

        #close file when finished
        target_file.close()

        #log results of search for hardcoded passwords
        log_results(found_pwds)

if __name__ == '__main__':
    main()