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
                      'CBC': 5,
                      'OFB': 5,
                      'Counter': 10, #Start counter with highest bias
                      'CWC': 5}
    
    def current_answer(self):
        return sorted(self.modes.items(), key=lambda item:item[1], reverse=True)[0][0]
    
    def ask(self, text, valid_answers=['1','2']):
        ans = None
        while ans not in valid_answers:
            ans = input(f'{text} > ')
            print('')
        return ans
    
    '''Check the importance of speed
    ECB is made most relevant or least relevant depending on answer'''
    def speed(self):
        answer = self.ask('Which is most important? 1: speed, 2: security')
        if answer == '1':
            answer = self.ask('Are you SURE speed is most important? 1: yes, 2: no')
            if answer == '1':
                self.modes['ECB'] += 100
                self.modes['Counter'] += 50
        else:
            self.modes['ECB'] -= 100
            answer = self.ask('Ok, speed isn\'t most important, but do you still care? 1: yes, 2: no')
            if answer == '1':
                self.modes['ECB'] += 50
            else:
                for mode in self.modes:
                    if mode != 'ECB':
                        self.modes[mode] += 10
    
    '''Check if user desires random data access'''
    def data_access(self):
        answer = self.ask('How do you want to access your encrypted data? 1: in order that it was encrypted, 2: access any data you choose')
        if answer == '1':
            self.modes['CBC'] += 10
        else:
            self.modes['OFB'] += 10
            self.modes['Counter'] += 10
            self.modes['CWC'] += 10
            self.modes['ECB'] += 10
    
    
    '''Check if user needs to be able to stream data'''
    def stream(self):
        answer = self.ask('Do you plan to be streaming your encrypted data, or will it be kept at rest (like on a hard drive? 1: Stream, 2: At rest')
        if answer == '1':
            self.modes['ECB'] += 10
            self.modes['CBC'] += 10
        else:
            self.modes['OFB'] += 10
            self.modes['Counter'] += 10
            self.modes['CWC'] += 10
        
    '''Check if NIST standardization matters'''
    def standardization(self):
        answer = self.ask('Do you want your mode to be a NIST recommendation? 1: yes, 2: don\'t care') 
        if answer == '1':
            for mode in self.modes:
                if mode != 'CWC':
                    self.modes[mode] += 10

    '''Check if parallelization matters... almost the same as speed but not quite'''
    def parallel(self):
        answer = self.ask('Would you like to be able to parrallelize some parts of encryption or decryption? 1: yes, 2: no')
        
        if answer == '1':
            for mode in self.modes:
                if mode != 'OFB':
                    self.modes[mode] += 10
    
    '''Print table'''
    def print(self):
        contents = {
            'headers': ['Rank', 'Mode of Operation', 'Block/Stream', 'Runtime Efficiency', 'Security', 'Decrypted data Access', 'NIST Recommended?'],
            'ECB': ['Electronic Code Book', 'Block', 'Fastest', 'Leaks block equality, may leak image', 'Random', 'Yes'],
            'CBC': ['Cipher Block Chaining', 'Block', 'Fast enough for almost all applications', 'Supports IND-CPA if cipher is a Psuedo-Random Function', 'Sequential', 'Yes'],
            'OFB': ['Output Feedback', 'Stream', 'Fast enough for almost all applications', 'Supports IND-CPA if cipher is a Psuedo-Random Function', 'Random', 'Yes'],
            'Counter': ['Galois/Counter Mode', 'Stream', 'Faster for almost all applications', 'Supports IND-CPA if cipher is a Psuedo-Random Function', 'Random, O[data]', 'Yes'],
            'CWC': ['Carter-Wegman Counter Mode', 'Stream', 'Fast enough for almost all applications', 'Supports IND-CPA if cipher is a Psuedo-Random Function', 'Random', 'No']
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
        print('Welcome to our Block Cipher Selection Tool')
        print('')
        if not test:
            time.sleep(2)
        
        print('Throughout, we will ask you a series of questions, you will answer by typing 1 or 2 and hitting enter')
        print('')
        if not test:
            time.sleep(2)
            
        print('We recommend maximizing your terminal window for best viewing experience.')
        if not test:
            time.sleep(2)
            
        print('')
        print('')
        self.speed()
        self.data_access()
        self.stream()
        self.standardization()
        self.parallel()
        
        self.print()
        print('')
        print('Thank you for using our advisor!')

bcs = Block_Cipher_Selector()
bcs.run(test=True)
