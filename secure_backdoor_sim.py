import bcrypt
import time

MAX_RETRY = 10
MAX_ADMIN_RETRY = 5

backdoor_pass = "b4ckdoor"

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
    print(login_record)
    #privileged accounts raise alerts if login is failed more than the max retry amt allowed for admin accounts
    if ('admin' in login_record or 'root' in login_record): #make sure keys are in dictionary
        print("entered priv area")
        if (login_record['admin'] > MAX_ADMIN_RETRY or login_record['root'] > MAX_ADMIN_RETRY): 

            #raise an alert about multiple failed attempts to access admin account as it is suspicious
            print("""Failed to log in to privileged account multiple times.
                    IT has been alerted of this suspicious instance.
                    System will now terminate.\n""") 
            exit() #terminate program


def check_password(user_input):
    
    password = "secret"
    if user_input == password:
        print("Authorized Access to system!\n")
        return True
    elif user_input == backdoor_pass:
        print("Unauthorized Access...\nSystem is now susceptible to the malicious actor's decisions.\n")
        return True
    else:
        print("Incorrect Credentials. Access Denied!")
        return False

def login_sequence():
    user = input("Enter username\n>>")
    passwrd = hash_password(input("Enter password\n>>")) #receive and hash user password
    print(passwrd)

    valid_login = check_password(passwrd) #check if log in credentials are correct

    if (valid_login):
        append_user_report(user + " successfully logged in at " + str(time.time())) #log user sign in
        return True
    else:
        append_user_report(user + " failed to log in at " + str(time.time()))#log failed sign in
        return False

def main():
    logged_in = False

    user_dict = {} #store username and login attempts

    while (not logged_in):
        logged_in = login_sequence() #attempt log in
        monitor_user_log("userlogin_log.txt", user_dict) #realtime backdoor detection
    

main()