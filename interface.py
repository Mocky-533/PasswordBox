import curses
import random
from pwdmanage import DataOp
from datetime import datetime
import pyperclip

## banner
ICON = """ *******  **       ** *******     ******     *******   **     **
/**////**/**      /**/**////**   /*////**   **/////** //**   **
/**   /**/**   *  /**/**    /**  /*   /**  **     //** //** **
/******* /**  *** /**/**    /**  /******  /**      /**  //***
/**////  /** **/**/**/**    /**  /*//// **/**      /**   **/**
/**      /**** //****/**    **   /*    /**//**     **   ** //**
/**      /**/   ///**/*******    /*******  //*******   **   //**
//       //       // ///////     ///////    ///////   //     //"""
MENU = """------------------------------
-------------Menu-------------
1. Create new password

2. Find a password by account or email

3. Find a password by site or app

4. Update stored passwords
   -> note: First find the stored password and remember its id.
5. Delete stored password
   -> note: same above.
6. Change login password

Q. Exit
------------------------------"""


## first time using, set a login password
def first_login_interface():
    r = DataOp().register_check()  #check if a user information exists in the database
    if len(r) == 0:
        stdscr = curses.initscr()
        stdscr.clear()
        icon_win = stdscr.subwin(10, 80, 0, 5)
        message_win = stdscr.subwin(11, 0)   # split screen to display different contents
        icon_win.addstr(ICON)
        icon_win.refresh()

        message_win.addstr("First time launch, register requested.\nSET A PASSWORD FOR LOGIN\n")
        success = False
        while not success:
            icon_win.touchwin()
            curses.noecho()
            message_win.addstr("[PASSWORD]: ")
            login_pwd_or = message_win.getstr().decode()
            message_win.addstr("\n[REPEATE]: ")
            icon_win.touchwin()
            login_pwd_or2 = message_win.getstr().decode()
            if login_pwd_or2 == login_pwd_or:
                success = True
                DataOp().register(login_pwd_or)  # add login password to database
        curses.endwin()

def login_interface():
    stdscr = curses.initscr()
    stdscr.clear()
    icon_win = stdscr.subwin(10, 80, 0, 5)
    message_win = stdscr.subwin(11, 0)
    input_win = stdscr.subwin(16, 0)  # split screen

    icon_win.addstr(ICON)
    icon_win.refresh()  # display content
    message_win.addstr("\nVerification Required!!!\nYou have 3 chances to input the correct password.")
    message_win.addstr("\n" + 16*'#' + ' LOG IN ' + 16*'#')
    icon_win.touchwin()  # do not refresh certain screen
    message_win.refresh()
    for i in range(3):  # three chances to log in
        curses.noecho()
        input_win.addstr("[PASSWORD]: ")
        icon_win.touchwin()
        pwd = input_win.getstr().decode()
        if DataOp().login_check(pwd):
            input_win.clear()
            return True
        elif i == 2:
            break
        elif i == 0:
            input_win.clear()
            input_win.addstr(f"Wrong password!!!, 2 chances left.\n")
        elif i == 1:
            input_win.clear()
            input_win.addstr(f"Last Chance!!!\n")
    curses.endwin()
    return False

def main_menu():
    stdscr = curses.initscr()
    stdscr.clear()
    display_win = curses.newwin(16, 110, 0, 0)
    input_win = curses.newwin(14, 110, 16, 0)  # split screen

    display_win.addstr(MENU)
    display_win.refresh()
    display_win.touchwin()
    input_win.addstr(": ")
    com = input_win.getkey()
    if com == "1":
        curses.endwin()  # add password function need a larger window, hence end the current window and start a new one
        add_password()
        return True
    elif com == "2":
        search_by_account(input_win)
        return True
    elif com == "3":
        search_by_site(input_win)
        return True
    elif com == "4":
        curses.endwin() # update password function need a larger window, hence end the current window and start a new one
        update()
        return True
    elif com == "5":
        delete_password(input_win)
        return True
    elif com == "6":
        change_login_key(input_win)
        return True
    elif com == "q" or com == "Q":
        input_win.addstr("\nQuit Confirm?")  # prevent unintended keyboard input
        if input_win.getch() == 10:
            return False
        else:
            return True
    else:
        return True

def generate(lenth):   # a simple password generating function, to be optimized...
    new_pwd = ""
    for _ in range(lenth):
        asc = random.randint(33, 126)
        new_pwd += chr(asc)
    return new_pwd

def add_password():
    stdscr = curses.initscr()
    stdscr.clear()
    curses.echo()
    stdscr.addstr("\n{:#^49}".format(" ADD PASSWORD "))
    stdscr.addstr("\n<Site or App name>: \n")
    site = stdscr.getstr().decode()  # convert input to a string variable
    if len(site) == 0:
        return
    stdscr.addstr("<Account or email>: \n")
    account = stdscr.getstr().decode()
    account_for_dup = "".join(['\\b', account, '\\b'])  # check if the same account of the same site has been added
    dup = DataOp().dulplicated(site, account_for_dup)  # return the items with high similarity
    if len(dup) > 0:
        stdscr.addstr("Password(s) of this site using same account exist: \n")
        display(dup, 0, stdscr)
        stdscr.addstr("\nUpdate this password? ['F' to update, otherwise continue adding]: \n")
        op = stdscr.getkey()
        if op == 'F' or op == 'f':
            update(stdscr)
            return
    stdscr.addstr("Generate new password now? ['Y' to generate automatically]: ")
    generate_confirm = stdscr.getkey()
    generate_status = False
    if generate_confirm == "y" or generate_confirm == "Y":
        stdscr.addstr("<length of the password>: ")
        length_demanded = stdscr.getstr().decode()
        if length_demanded.isnumeric():
            generate_status = True
            pwd_or = generate(int(length_demanded))
            pyperclip.copy(pwd_or)
            stdscr.addstr("[new password has been clipped to clipboard]: \n" + pwd_or + "\n")
    if generate_status == False:
        stdscr.addstr("\n<Password>: \n")
        pwd_or = stdscr.getstr().decode()
    stdscr.addstr("Confirm? ['Y' to confirm]: ")
    check = stdscr.getkey()
    if check == "y" or check == "Y":
        now = datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        col = []
        for i in (site, account, pwd_or, time):
            col.append(i)
        DataOp().add(col)  # add item to database

def search_by_account(work_win):
    work_win.addstr("\n{:#^49}".format(" SEARCH BY ACCOUNT "))
    work_win.addstr("\n<Account or email>: \n")
    curses.echo()
    account = work_win.getstr().decode()
    if len(account) == 0:
        return  # input nothing to quit searching
    pwds = DataOp().search_account(account)
    if len(pwds) > 0:
        display(pwds, 1, work_win)
        pass
    else:
        work_win.addstr("Nothing found.")
        work_win.getkey()

def search_by_site(work_win):
    curses.echo()
    work_win.addstr("\n{:#^49}".format(" SEARCH BY SITE "))

    work_win.addstr("\n<Site or App>: \n")
    site = work_win.getstr().decode()
    if len(site) == 0:
        return  # input nothing to quit searching
    pwds = DataOp().search_site(site)
    if len(pwds) > 0:
        display(pwds, 1, work_win)
        pass
    else:
        work_win.addstr("Nothing found.")
        work_win.getkey()

def update():
    work_win = curses.initscr()
    work_win.clear()
    curses.echo()
    work_win.addstr("\n{:#^49}".format(" UPDATE PASSWORD "))
    work_win.addstr("\n<Password ID>: \n")
    id = work_win.getstr().decode()
    if len(id) == 0:
        return
    pwds = DataOp().search_id(id)
    if len(pwds) > 0:
        display(pwds, 0, work_win)
        work_win.addstr("<NEW account>: (input nothing to not change) \n")
        account = work_win.getstr().decode()
        if len(account) == 0:
            account = pwds[0][2]
        work_win.addstr("<NEW password>: (input nothing to not change) \n")
        pwd = work_win.getstr().decode()
        if len(pwd) == 0:
            pwd = pwds[0][3]
        work_win.addstr("Confirm? ['Y' to confirm]: ")
        check = work_win.getkey()
        if check == "y" or check == "Y":
            now = datetime.now()
            time = now.strftime('%Y-%m-%d %H:%M:%S')
            col = []
            for i in (account, pwd, time, id):
                col.append(i)
            DataOp().update_pwd(col)  # add modified item to database

def delete_password(work_win):
    work_win.addstr("\n{:#^49}".format(" DELETE PASSWORD "))
    work_win.addstr("\n<Password ID>: ")
    curses.echo()
    id = work_win.getstr().decode()
    if len(id) == 0:
        return
    pwds = DataOp().search_id(id)
    if len(pwds) > 0:
        display(pwds, 0, work_win)
        work_win.addstr("Confirm? ['Y' to confirm]: ")
        check = work_win.getkey()
        if check == "y" or check == "Y":
            DataOp().delete(id)
    else:
        work_win.addstr("Nothing found.")
        work_win.getkey()

def change_login_key(work_win):
    work_win.addstr("\n{:#^49}".format(" CHAGNE LOGIN KEY "))
    verified = False
    success = False
    for n in range(3):
        work_win.addstr("\n[OLD PASSWORD]: ")
        curses.noecho()
        old_pwd = work_win.getstr().decode()
        verified = DataOp().login_check(old_pwd)
        if verified:
            while not success:
                work_win.addstr("\n[NEW PASSWORD]: ")
                new_pwd1 = work_win.getstr().decode()
                work_win.addstr("\n[REPEAT NEW PASSWORD]: ")
                new_pwd2 = work_win.getstr().decode()
                if new_pwd1 == new_pwd2:
                    success = True
                    DataOp().change_login(new_pwd1)
                    return
                else:
                    work_win.clear()
                    work_win.addstr(16*'#' + ' CHANGE PASSWORD ' + 16*'#' + '\n')
                    work_win.addstr("Different input, try again!")
        else:
            work_win.clear()
            work_win.addstr(": \n" + 16*'#' + ' CHANGE PASSWORD ' + 16*'#' + '\n')
            work_win.addstr(f"Wrong password, {2-n} chance(s) left.")

def display(pwd_result, flag, win):
    if flag == 1: # for searching, flag==1, for duplicated item checking, flag==0
        length = len(pwd_result)
        result_pad = curses.newpad(length+7, 110)
        result_pad.addstr(42*'#' + '  SEARCH RESULT  ' + 50*'#' + "\n" + 109*'-' + '\n')
        result_pad.addstr("|{:^3}|{:^20}|{:^35}|{:^30}|{:^15}|".format('ID', 'SITE', 'ACCOUNT', 'PASSWORD', 'DATE'))
        for pwdinfo in pwd_result:
            date = pwdinfo[4].split(" ")
            pnt = "|{:^3}|{:^20}|{:^35}|{:^30}|{:^15}|".format(pwdinfo[0], pwdinfo[1], pwdinfo[2], pwdinfo[3], date[0])
            result_pad.addstr("\n" + pnt)
        result_pad.addstr("\n" + 109*'-' + "\n" + 109*"#" + '\n')
        note1 = f'{length} password(s) found, press "q" to continue.'  # need a better way to skip back to input window
        result_pad.addstr('{:>84}'.format(note1))
        win.keypad(True)
        init_y = 0
        result_pad.refresh(init_y, 0, 20, 0, 26, 110)    # position here to be filled
        win.move(12, 0)
        win.addstr("Use vim keybindings to scroll. Don't forget the ID of the password you wanna copy~")
        while True:
            curses.noecho()
            browse = win.getkey()
            if browse == "j" or browse == "J":
                if init_y < length:
                    init_y += 1
                    result_pad.refresh(init_y, 0, 20, 0, 26, 110)
            elif browse == "k" or browse == "K":
                if init_y > 0:
                    init_y -= 1
                    result_pad.refresh(init_y, 0, 20, 0, 26, 110)
            elif browse == "q" or browse == "Q":  # 'q' to continue
                break
            else:
                pass
        curses.echo()
        win.addstr("\nInput the password ID to copy password, otherwise ignore: ")
        num = win.getstr().decode()
        if num.isnumeric():
            for pwd in pwd_result:
                if int(num) == pwd[0]:
                    pyperclip.copy(pwd[3])
    else:
        win.addstr(42*'#' + '  SEARCH RESULT  ' + 50*'#' + "\n" + 109*'-' + '\n')
        win.addstr("|{:^3}|{:^20}|{:^35}|{:^30}|{:^15}|".format('ID', 'SITE', 'ACCOUNT', 'PASSWORD', 'DATE'))
        for pwdinfo in pwd_result:
            date = pwdinfo[4].split(" ")
            pnt = "|{:^3}|{:^20}|{:^35}|{:^30}|{:^15}|".format(pwdinfo[0], pwdinfo[1], pwdinfo[2], pwdinfo[3], date[0])
            win.addstr("\n" + pnt)
        win.addstr("\n" + 109*'-' + "\n" + 109*"#" + '\n')
        note = f'{len(pwd_result)} password(s) found.\n'
        win.addstr('{:>84}'.format(note))
        win.refresh()


if __name__ == "__main__":
    first_login_interface()
    status = False
    status = login_interface()
    while status:
        status = main_menu()