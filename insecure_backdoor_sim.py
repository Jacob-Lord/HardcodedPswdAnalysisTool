backdoor_pass = "b4ckdoor"

def check_password(user_input):
    password = "secret"
    if user_input == password:
        print("Authorized Access to system!\n")
    elif user_input == backdoor_pass:
        print("Unauthorized Access...\nSystem is now susceptible to the malicious actor's decisions.\n")
    else:
        print("Incorrect Credentials. Access Denied!")

def main():
    user = input("Enter username\n>>")
    passwrd = input("Enter password\n>>")
    check_password(passwrd)

main()