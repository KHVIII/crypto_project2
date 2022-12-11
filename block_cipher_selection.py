import sys
import time
try:
    from prettytable import PrettyTable
except:
    print('Please run "pip3 install prettytable"')
    sys.exit(0)

class Block_Cipher_Selector:
    def __init__(self):
        self.modes = {'ECB': 0,
                      'OFB': 5,
                      'CBC': 10,
                      'CWC': 5,
                      'GCM': 10, #Start counter with highest bias
                      'XTS': 5}
    
    def current_answer(self):
        return sorted(self.modes.items(), key=lambda item:item[1], reverse=True)[0][0]
    
    def ask(self, text, valid_answers=['1','2']):
        ans = None
        while ans not in valid_answers:
            ans = input(f'{text} > ')
            print('')
        return ans

    '''Check the level of security
    
    '''
    def security(self):
        answer = self.ask('Would confidentiality be important to the system (e.g. To prevent the possibility of an attacker accessing the unencrypted information)? 1: Yes 2: No')
        if answer == '1':
            self.modes['ECB'] -= 50
            answer = self.ask('Would message integrity (e.g. the possibility of an attacker forging a message) be important to the system? (if not sure, answer yes unless the system is for some form of disk encryption) 1: Yes 2: No')
            if answer == '1':
                self.modes['GCM'] += 50
                self.modes['CWC'] += 50
                answer = self.ask('Would occasional/rare instances of forgeries or implementation mistakes be tolerable within the system as long as it does not entirely compromise the system? (answer no if not sure) 1: Yes 2: No')
                if answer == '1':
                    self.modes['CWC'] += 5
            else:
                self.modes['CBC'] += 40
                self.modes['XTS'] += 50
                self.modes['OFB'] += 40






    '''Check the importance of speed
    ECB is made most relevant or least relevant depending on answer'''
    def speed(self):
        answer = self.ask('Is speed of the operations an important factor? 1: Yes, 2: No')
        if answer == '1':
            self.modes['GCM'] += 10
            self.modes['CBC'] += 10

            answer = self.ask('Are you willing to sacrifice message confidentiality and integrity for maximum efficiency? 1: Yes, 2: No')
            if answer == '1':
                self.modes['ECB'] += 150
        
        answer = self.ask('Do you expect the system to scale hard in the future (growth in the size of throughput of the operation)? 1: Yes, 2: No')
        if answer == "1":
            self.modes["GCM"] += 10
        
    
    '''Check if user desires random data access'''
    def data_access(self):
        answer = self.ask('How do you want to access your encrypted data? 1: In the order that it was encrypted, 2: Randomly')
        if answer == '1':
            self.modes['CBC'] += 10
            self.modes['XTS'] += 10
        else:
            for mode in self.modes:
                if mode != 'CBC' and mode != 'XTS':
                    self.modes[mode] += 10



    
    
    '''Check if user needs to be able to stream data'''
    def stream(self):
        answer = self.ask('Do you need the versatility of stream cipher mode on top of the block cipher mode? 1: Yes, 2: No')
        if answer == '1':
            self.modes['GCM'] += 10
            self.modes['CWC'] += 10
        
    '''Check if NIST standardization matters'''
    def standardization(self):
        answer = self.ask('Do you need your mode to be a NIST recommendation? (answer yes if this is for corporate / auditing exists) 1: Yes, 2: No') 
        if answer == '1':
            self.modes['CWC'] -= 15

    '''Check if parallelization matters... almost the same as speed but not quite'''
    def parallel(self):
        answer = self.ask('Does your system have the capabilities to parallelize parts of the encryption or decryption? 1: Yes, 2: No')
        
        if answer == '1':
            for mode in self.modes:
                if mode != 'OFB' and mode != 'CBC':
                    self.modes[mode] += 10
            self.modes['CBC'] += 5
    
    '''Print table using pretty print libraries'''
    def print(self):
        '''To add columns, just add an entry to the list for headers
        to add a row, add an entry to the dict'''
        contents = {
            'headers': ['Rank', 'Mode of Operation', 'Block/Stream', 'Runtime Efficiency', 'Confidentiality', 'Integrity/Authenticity', 'Decrypted data Access', 'NIST Recommended?', 'Parallelizability'],
            'ECB': ['ECB', 'Block', 'Fastest', 'No', 'No', 'Random', 'Yes', 'Yes'],
            'CBC': ['CBC', 'Block', 'Fast enough for almost all applications', 'Yes', 'No', 'Sequential', 'Yes', 'Partial (Decryption Only)'],
            'OFB': ['OFB', 'Stream', 'Fast enough for almost all applications', 'Yes', 'No', 'Random', 'Yes', 'No'],
            'GCM': ['GCM', 'Stream', 'Faster for almost all applications', 'Yes', 'Yes', 'Random, O[data]', 'Yes', 'Yes'],
            'CWC': ['CWC', 'Stream', 'Fast enough for almost all applications', 'Yes', "Yes", 'Random', 'No', 'Yes'],
            'XTS': ['XTS', 'Block', 'Fast enough for almost all applications', "Yes", "No", "Sequential", "Yes", "Yes"]
        }
            
        table = PrettyTable()
        table.field_names = contents['headers']
        
        #Sort the modes by score
        sort = sorted(self.modes.items(), key=lambda item:item[1], reverse=True)
        rank = 1
        for item in sort:         
            row = contents[item[0]]
            row.insert(0, rank)
            table.add_row(contents[item[0]])
            rank+=1
        
        print(table)
        
    def run(self, test=False):
        print('Welcome to our Block Cipher Mode of Operation Selection Tool, developed by: Robert Frost and Yin Tian Chen')
        if not test:
            time.sleep(2)
        
        print('Throughout, we will ask you a series of questions, you will answer by typing 1 or 2 and hitting enter')
        if not test:
            time.sleep(2)
            
        print('We recommend maximizing your terminal window for best viewing experience.')
        if not test:
            time.sleep(2)

        print('*Note: This selection tool assumes that your symmetric encryption scheme uses Pseudo-Random Function ciphers e.g. AES')
        if not test:
            time.sleep(2)
            
        print('')
        print('')
        self.security()
        self.speed()
        self.data_access()
        self.stream()
        self.standardization()
        self.parallel()
        
        self.print()
        print('')
        print('Thank you for using our advisor!')

        if (test):
            print(self.modes)

bcs = Block_Cipher_Selector()
bcs.run(test=True)
