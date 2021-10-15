# Imports
# Functions :
# Roles Manager :

def Roles(user,roles):
    for perm in user.perm:
        if perm.perm in roles :
            return True
    return False 


