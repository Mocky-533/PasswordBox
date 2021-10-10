import os
import getpass
import pyperclip
from datetime import datetime
from pwdmanage import (add, search_site, search_account, update_pwd,
     change_login, register_check, register, login_check, delete)

def main_menu():
    print('-'*30)
    print(('-'*13) + 'Menu'+ ('-' *13))
    print('1. Create new password\n')
    print('2. Find a password by account or email\n')
    print('3. Find a password by site or app\n')
    print('4. Update stored passwords\n   -> note: First find the stored password and remember its id.')
    print('5. Delete stored password\n   -> note: same above.')
    print('6. Change login password\n')
    print('Q. Exit')
    print('-'*30)
    return input(': ')

def add_password():
    print()
    site = input("<Site or App name>: \n")
    account = input("<Account or email>: \n")
    pwd_or = input("<Password>: \n")
    check = input("Confirm? [Y to confirm]: ")
    if check == "y" or check == "Y":
        now = datetime.now() # time stamp
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        col = []
        for i in (site, account, pwd_or, time, account.lower()):
            col.append(i)
        add(col)

def search_by_account():
    print()
    account = input("<Account or email>: \n")
    pwds = search_account(account.lower())
    if len(pwds) > 0:
        print()
        display(pwds)
    else:
        print("Nothing found")
        input() # display results until "enter" is pressed again

def search_by_site():
    print()
    site = input("<Site or App>: \n")
    pwds = search_site(site.lower())
    if len(pwds) > 0:
        print()
        display(pwds)
    else:
        print("Nothing Found")
        input()

def update():
    print()
    id = input('<Password ID>: \n')
    pwd = input('<NEW password>: ')
    check = input("Confirm? [Y to confirm]: ")
    if check == "y" or check == "Y":
        now = datetime.now() # time stamp
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        col = []
        for i in (pwd, time, id):
            col.append(i)
        update_pwd(col)

def delete_password():
    print()
    id = input("<Password ID>: \n")
    check = input("Confirm? [Y to confirm]: ")
    if check == "y" or check == "Y":
        delete(id)

def display(pwd_result):
    print(42*'#' + '  SEARCH RESULT  ' + 50*'#')
    print(109*'-')
    print("|{:^3}|{:^15}|{:^40}|{:^30}|{:^15}|".format('ID', 'SITE', 'ACCOUNT', 'PASSWORD', 'DATE'))
    for pwdinfo in pwd_result:
        date = pwdinfo[4].split(" ") # display only the day this column was added
        pnt = "|{:^3}|{:^15}|{:^40}|{:^30}|{:^15}|".format(pwdinfo[0], pwdinfo[1], pwdinfo[2], pwdinfo[3], date[0])
        print(pnt)
    print(109*'-')
    print(109*"#")
    note = f'{len(pwd_result)} password(s) found.'
    print('{:>84}'.format(note))
    num = input("\nInput a number n to copy the n(th) password to clipboard, letters to ignore: ")
    if num.isnumeric():
        pyperclip.copy(pwd_result[int(num)-1][3])
        print("Password Copied!")

def change_password():
    print('\n' + 16*'#' + ' CHANGE PASSWORD ' + 16*'#' + '\n')
    verified = False
    success = False
    while not verified:
        old_pwd = getpass.getpass('[OLD PASSWORD]: ')
        verified = login_check(old_pwd)
    while not success:
        new_pwd1 = getpass.getpass('[NEW PASSWORD]: ')
        new_pwd2 = getpass.getpass('[REPEAT NEW PASSWORD]: ')
        if new_pwd1 == new_pwd2:
            success = True
            change_login(new_pwd1)
        else:
            print("Different Input, Try Again!")

def first_login():
    r = register_check()
    if len(r) == 0:
        print("""
    *******  **       ** *******     ******     *******   **     **
    /**////**/**      /**/**////**   /*////**   **/////** //**   **
    /**   /**/**   *  /**/**    /**  /*   /**  **     //** //** **
    /******* /**  *** /**/**    /**  /******  /**      /**  //***
    /**////  /** **/**/**/**    /**  /*//// **/**      /**   **/**
    /**      /**** //****/**    **   /*    /**//**     **   ** //**
    /**      /**/   ///**/*******    /*******  //*******   **   //**
    //       //       // ///////     ///////    ///////   //     //
        """)
        print("First time launch, register requested.\n")
        print("SET A PASSWORD FOR LOGIN")
        success = False
        while not success:
            login_pwd_or = getpass.getpass("[PASSWORD]: ")
            login_pwd_or2 = getpass.getpass("[REPEAT]: ")
            if login_pwd_or == login_pwd_or2:
                success = True
                os.system("cls")
                register(login_pwd_or)

def login():
    print("\n" + 16*'#' + ' LOG IN ' + 16*'#' + "\n")
    pwd = getpass.getpass("[PASSWORD]：") # hide input
    return login_check(pwd)
