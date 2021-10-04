import os
from menu import (main_menu, add_password, search_by_account, delete_password,
         update, search_by_site, change_password, login, first_login)

if __name__ == "__main__":
    first_login()
    icon = """
    *******  **       ** *******     ******     *******   **     **
    /**////**/**      /**/**////**   /*////**   **/////** //**   **
    /**   /**/**   *  /**/**    /**  /*   /**  **     //** //** **
    /******* /**  *** /**/**    /**  /******  /**      /**  //***
    /**////  /** **/**/**/**    /**  /*//// **/**      /**   **/**
    /**      /**** //****/**    **   /*    /**//**     **   ** //**
    /**      /**/   ///**/*******    /*******  //*******   **   //**
    //       //       // ///////     ///////    ///////   //     //
        """
    print(icon)
    print("\nVerification Required!!!\nYou have 5 chance to input the right password.")
    verified = False
    for i in range(5):
        verified = login()
        if verified:
            break
        elif i == 4:
            break
        else:
            print(f"Wrong password!!!, You have {4-i} chances left.")
    if verified:
        while True:
            os.system('cls') # clear screen
            com = main_menu()
            if com == '1':
                add_password()
            elif com == '2':
                search_by_account()
            elif com == '3':
                search_by_site()
            elif com == '4':
                update()
            elif com == '5':
                delete_password()
                pass
            elif com == '6':
                change_password()
            elif com == 'Q' or com == 'q':
                break