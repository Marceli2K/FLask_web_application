class editOrg(object):
    """description of class"""
    import re
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    UsrLoginCreds=[1,1,"TEST","test@wp.pl"]
    UsrDataBase=[[1,1,"TEST","test@wp.pl"],[2,0,"User","testdsada@wp.pl"]]
    UsrNewUsername=input("Podaj nowa nazwe uzytkownika:")
    testEmail=0
    while testEmail==0:
        UsrNewEmail=input("Wprowadz nowy adres email:");
        if (re.search(regex,UsrNewEmail)):
            testEmail=1;
        else:
                print("Podany email jest nieprawidlowy")
    
    PendingChangeUsr=[UsrLoginCreds[0],UsrLoginCreds[1],UsrNewUsername,UsrNewEmail]
    print("PRZEKAZANO DO WERYFIKACJI\n*****STRONA ADMINISTRATORA******")
    print(PendingChangeUsr[2],PendingChangeUsr[3])
    test=input("Zatwierdzic Y/N?")
    if test == "Y" or test == "y":
        print("Wprowadzanie zmian")
        UsrDataBase.remove(UsrLoginCreds)
        UsrDataBase.append(PendingChangeUsr)
    else:
        print("Odrzucono zmiany")

    print(UsrDataBase)