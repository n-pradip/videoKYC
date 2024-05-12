import random

# def generate_otp(len):
#     otp = ""
#     for _ in range(len):
#         otp += str(random.randint(0, 9))
#     return otp

def generate_otp_code(num):
    otp_code = ''.join(str(random.randint(0, 9)) for _ in range(num))    
    return otp_code