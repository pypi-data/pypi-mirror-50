class PasswordChecker:

    def __init__(self,password):
        self.password = password
    
    def isvulnerable(self):
        with open('passwords.txt') as f:
            for i in f:
                i = i.strip()
                if(i == self.password):
                    return True
        return False

    def isstong(self):
        special = '!@#$%^&*()?'
        password_list = self.password.split(" ")
        if(len(password_list) > 1):
            count = len(password_list)
            for i in password_list:
                if (len(i) >= 8 or not i.lower() or not i.upper() or i.isalpha() or  any((char in special) for char in self.password)):
                    count += 1
                if(count > 4):
                    return True
                else:
                    return False
        elif len(self.password) >= 8 and not self.password.islower() and not self.password.isupper() and not self.password.isalpha() and not self.password.isdigit() and any((char in special) for char in self.password):
            return True
        else:
            return False