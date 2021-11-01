import os
from menu import menu

if __name__ == "__main__":
    m = menu()
    m.first_login()
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
        verified = m.login()
        if verified:
            break
        elif i == 4:
            break
        else:
            print(f"Wrong password!!!, You have {4-i} chances left.")
    if verified:
        while True:
            os.system('cls') # clear screen
            com = m.main_menu()
            if com == '1':
                m.add_password()
            elif com == '2':
                m.search_by_account()
            elif com == '3':
                m.search_by_site()
            elif com == '4':
                m.update()
            elif com == '5':
                m.delete_password()
                pass
            elif com == '6':
                m.change_password()
            elif com == 'Q' or com == 'q':
                break