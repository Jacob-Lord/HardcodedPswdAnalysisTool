import re

def scan_pwd_names_file(pwd_file, pwd_id_list):
    for name in pwd_file: 
        name = name.strip()
        if (name not in pwd_id_list):
            if (name[-1::] == '\n'):
                pwd_id_list.append(name[:-1:]) #do not include newline char in list
            else:
                pwd_id_list.append(name) #last name in file does not have a newline char

def find_hardcoded_pwds(target_file, password_id_list):

    found_pwds = {} #dict to store hardcoded passwords
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
        
        #if a match is found then store it in the found_pwds dictionary
        if match:
            pwd = match.group(1) # hardcoded password that was found by regex
            found_pwds[id] = pwd # store variable and password in dictionary
            print(f"Found: {match.group()} at position {match.start()}") #output message when a match is found
    
def main():
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


    #catch file not found errors
    try:
        #open target file to search contents for hardcoded passwords
        target_file = open("secure_backdoor_sim.py", "r") 
    except:
        raise FileNotFoundError
    else:
        #search target file for hardcoded passwords
        find_hardcoded_pwds(target_file, password_id_list) 

        #close file when finished
        target_file.close()

if __name__ == '__main__':
    main()