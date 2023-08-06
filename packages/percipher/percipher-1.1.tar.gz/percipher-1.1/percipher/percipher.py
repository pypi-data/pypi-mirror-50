from random import shuffle

def encrypt(string: str) -> tuple:
    '''
    function for encrypting strings
    
    arg string -- string which you want to encrypt
        (type must be str)
    
    returns: tuple. e.g: (encrypted_string,key_to_string).
    '''
    all_symbols = list(string)
    unique_symbols = list(set(all_symbols))
    unique_symbols_copy = unique_symbols[:]
    
    shuffle(unique_symbols)
    shuffle(unique_symbols_copy)
    
    key_dict = {
        unique_symbols[i] : unique_symbols_copy[i]
        for i in range(len(unique_symbols))
    }
    encrypted_string = ''.join([key_dict[i] for i in all_symbols])
    key_to_string = ''.join(
        list(key_dict.keys())[i] + list(key_dict.values())[i] 
        for i in range(len(key_dict))
    )
    return encrypted_string, key_to_string


def decrypt(encrypted: str, key: str) -> str:
    '''
    function for decrypting encrypted by 
        Permutation.Cipher strings
    
    arg encrypted -- encrypted string
        (type must be str)
    
    arg key -- key for encrypted string
        (type must be str)
     
    returns: str. decrypted string.
    '''
    decrypt_key = {}
    for i in range(0,len(key),2):
        decrypt_key[key[i+1]] = key[i]
    
    decrypted_string = ''.join(decrypt_key[i] for i in encrypted)
    return decrypted_string

        
if __name__ == '__main__':
    string = open('string.txt').read()
    e = encrypt(string)
    
    print('Encrypted String ->',[e[0]])
    print('\nKey to Encrypted String ->',[e[1]])