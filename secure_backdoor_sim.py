import bcrypt
import time

MAX_RETRY = 10
MAX_ADMIN_RETRY = 5

backdoor_pass = "backdoor"

def hash_password(password):
    if (password != None):
        bytes_pass = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(bytes_pass, salt)
    return hashed_pass

def append_user_report(string):
    user_log_name = "userlogin_log.txt"

    try:
        user_log_file = open(user_log_name, "a")
    except: 
        raise FileNotFoundError

    user_log_file.write(string + "\n")

def monitor_user_log(user_log, login_record):
    
    #try to open user login log file
    try:
        log = open(user_log, "r")
    except:
        raise FileNotFoundError

    #read the log file
    for line in log:
        words = line.split() #split the file line into words

        user = words[0] # the user is always the first string in the log
        if user not in login_record:
            login_record[user] = 1
        else:
            login_record[user] += 1 #increment number of times user has attempted login

    #if the number of logins exceeds the maximum number of allowed retries lock the account
    if (login_record[user] > MAX_RETRY):  
        print("Number of login attempts exceeded allowed amoun. The account has been locked. Contact IT to reset password.\n")

    #privileged accounts raise alerts if login is failed more than the max retry amt allowed for admin accounts
    if ('admin' in login_record): #make sure keys are in dictionary
        if (login_record['admin'] > MAX_ADMIN_RETRY): 

            #raise an alert about multiple failed attempts to access admin account as it is suspicious
            print("""Failed to log in to privileged account multiple times.
                    IT has been alerted of this suspicious instance.
                    System will now terminate.\n""") 
            exit() #terminate program

def check_password(user, pwd):

    spwd_hash = retrieve_pass_hash(user)

    if (spwd_hash):
    
        pwd_bytes = pwd.encode('utf-8')

        if bcrypt.checkpw(pwd_bytes, spwd_hash):
            print("Authorized Access to system!\n")
            return True
        elif pwd == backdoor_pass:
            print("Unauthorized Access...\nSystem is now susceptible to the malicious actor's decisions.\n")
            return True
        else:
            print("Incorrect Credentials. Access Denied!")
            return False
    else:
        print("Incorrect Credentials. Access Denied!") #could specify that user is not in sys but that reveals info
        return False
    
#store username and hashed password for new accounts
def store_password(user, hashed_pass):
    storage_file = open("pwd_storage.txt", "a") # would be appended normally, but for simulation purposes file should be deleted before reuse
    storage_file.write(user + " " + hashed_pass.decode('utf-8') + "\n")
    storage_file.close()

def retrieve_pass_hash(user):
    try:
        storage_file = open("pwd_storage.txt", "r")
    except:
        raise FileNotFoundError
    

    for line in storage_file:
        name_pass = line.split()
        if(name_pass):
            uname = name_pass[0]
            pwd_hash = name_pass[1]

            if uname == user: #check if provided username has a pwd on file
                return pwd_hash.encode('utf-8') #return password hash for comparison
    return False

def login_sequence(user_dict):
    user = input("Enter username\n>>")
    passwrd = input("Enter password\n>>") #receive and hash user password

    valid_login = check_password(user, passwrd) #check if log in credentials are correct

    if (valid_login):
        append_user_report(user + " successfully logged in at " + str(time.time())) #log user sign in
        user_dict[user] = 0
        return True
    else:
        append_user_report(user + " failed to log in at " + str(time.time()))#log failed sign in
        return False

def main():
    
    #start of simulation -------------------------------------------------------------------
    logged_in = False
    user_dict = {} #store username and login attempts

    while (not logged_in):
        logged_in = login_sequence(user_dict) #attempt log in
        monitor_user_log("userlogin_log.txt", user_dict) #realtime backdoor detection
    

main()