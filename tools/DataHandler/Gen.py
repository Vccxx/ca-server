from DataDefine import MAX_SERIAL_NUM
import os
def next_sn():
    sn = 0
    number = ""
    file_path = os.path.abspath(__file__)
    file_path =  "/".join(file_path.split("/")[:-1])
    with open(file_path + "/serial_number","r") as sn_file:
        number = sn_file.read().strip()
        if len(number) > MAX_SERIAL_NUM:
            number = "0"
        sn = int(number,10)
        number = str(sn+1)
    with open(file_path + "/serial_number","w") as sn_file:
        sn_file.write(number)
    return str(sn)

if __name__ == "__main__":
    print next_sn()