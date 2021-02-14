
class HappyPrime:

    def __init__(self,num):
        self.num = num
        self.main()

    def main(self):
        '''
        ask user for input to determine if a number is happy/sad and prime/non-prime number
        
        :user_input num: any interger
        :return: print whether a number is happy/sad and prime/non-prime number
        '''
        if self.num == None or self.num == '':
            self.result = None
        else:
            self.result = self.get_result(int(self.num))

    def get_result(self, num):
        '''
        pass num into functions to determine whether or not it is happy/sad and prime or not prime
        print a result string to describe the number
        
        :param num: original user input value
        :return: print whether a number is happy/sad and prime/non-prime number
        '''
        prime_check = self.is_prime(num)
        num_emotion = self.happy_sad_check(num)
        str_result = str(num) + ' is a ' + num_emotion + ' ' + prime_check
        return str_result

    def is_prime(self, num):
        '''
        check if num is a prime number
        
        :param num: original user input integer
        :return prime: string value describing whether or not the number is prime
        '''
        prime = 'prime'
        for test_num in range(2, num):
            if num%test_num == 0: # if remainder = 0, then not prime
                prime = 'non-prime'
        return prime

    def happy_sad_check(self, num):
        '''
        check if num is a happy or sad number by taking the squaring each digit of the input value and summing those values
        until the loop either repeats itself or the sum of squared digits is 1
        
        :param num: original user input integer
        :return prime: string value describing whether or not the number is happy or sad
        '''
        num_emotion = 'happy'
        res_dict = {}

        while num_emotion != 'sad':
            digit_sum = self.sum_sq_digits(num)

            if digit_sum in res_dict.keys(): # check if key already exists in dictionary
                num_emotion = 'sad'
                return num_emotion
            elif digit_sum == 1:
                return num_emotion 
            else:
                res_dict[num] = digit_sum # add key to dict if not already in dict
                num = digit_sum # use sum of square digits value for next iteration

    def sum_sq_digits(self, num):
        '''
        create a list of digits from the input number and calculate the sum of squared digit value by interating
        over a list of those digits
        
        :param num: original user input integer or most recent return value of this function (digit_sum)
        :return digit sum: sum of square digits of num input
        '''
        
        digit_list = [int(x) for x in str(num)] # create a list of all the digits in the num input

        digit_sum = 0
        for digit in digit_list:
            digit_sum += digit**2 
        
        return digit_sum
