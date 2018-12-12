# 设置起始阻值\每次变化量\变化次数\变化间隔时间,实现电阻值自动变化输出


import serial
import time
import json
import os

# 串口速率\检验位\起始位均采用默认值
ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 9600
print(ser)
"""

参数输入
input_res: 起始阻值
change_size: 变化量
change_times: 变化次数
change_intervals: 变化间隔时间

"""
def stable_res(flag):
    while flag == True:
        try:
            output_res = input('\n请输入固定阻值:')
            if output_res == 'exit':
                raise Exception()
            else:
                output_res = 'OUTP:RES {}'.format(output_res) + '\n'
                ser.write(output_res.encode())
                time.sleep(0.1)
                if ser.in_waiting:
                    print('\n无效数字,请重新输入!')
                    ser.read_all()
                    continue
                else:
                    print('设置成功!')
                    continue
        except Exception:
            flag = False
    return flag
    

def input_argus(flag): 
    argus_name = ('input_res', 'change_size', 'change_times', 'change_intervals')
    argus_chinese = {'input_res':'起始阻值', 'change_size':'变化量', 'change_times':'变化次数', 'change_intervals':'变化间隔时间'}
    argus = {}
    for item in argus_name:
        while flag == True:
            try:
                argus[item] = input('\n请输入 {}:'.format(argus_chinese[item]))
                if argus[item] == 'exit':
                    raise Exception()
                else:
                    try:
                        argus[item] = float(argus[item])
                    except:
                        print('\n无效数字,请重新输入!')
                        continue
                break
            except Exception:
                flag = False
        if flag == False:
            break
    return flag, argus

def run_box(argus):
    output_res = argus['input_res']
    output = 'OUTP:RES {}'.format(output_res) + '\n' 
    # 设置电阻初始值
    ser.write(output.encode())
    # 循环更新电阻值
    for i in range(int(argus['change_times'])): 
        time.sleep(argus['change_intervals']) 
        output_res = output_res + argus['change_size']
        output = 'OUTP:RES {}'.format(output_res) + '\n'
        ser.write(output.encode())
    print("\nend!") 

def save_argus(argus):
    flag = True
    while flag == True:
        save_command = input('\n是否保存当前参数?(Y/n):')
        if save_command == 'Y':
            while True:
                file_address = input('\n请输入保存地址:')
                if file_address == 'exit':
                    break
                else:
                    try:
                        with open(file_address+'.json','w') as outfile:
                            json.dump(argus,outfile,ensure_ascii=False)
                            outfile.write('\n')
                    except:
                        print('\n地址无效,请重新输入!')
                        continue
                    print('\n文件已成功保存在{}'.format(file_address+'.json'))
                    flag = False
                    break
        elif save_command == 'n':
            flag = False
        else:
            print('\n请重新输入字母Y或n')
            continue

def read_argus(flag):
    argus = {}
    while True:
        file_address = input('\n请输入文件地址:')
        if file_address == 'exit':
            flag = False
            break
        else:
            try:
                with open(file_address, 'r') as infile:
                    argus = json.load(infile)
            except:
                print('\n无效地址,请重新输入!')
                continue
            print('\n文件已成功读取!')
            print('起始阻值:{} 变化量:{} 变化次数:{} 变化间隔时间:{}'.format(argus['input_res'],argus['change_intervals'],argus['change_times'],argus['change_size']))
            break
    return flag, argus

def run():
    while True:
        mode_layer_1 = input('\n请选择 1:固定阻值 2:自动变化阻值:')
        if mode_layer_1 == '1':
            while True:
                flag = True
                flag = stable_res(flag)    
                if flag == False:
                    break
        if mode_layer_1 == '2':
            while True:
                mode_layer_2 = input('\n请选择 1:手动输入 2:读取文件:')
                if mode_layer_2 == '1':
                    while True:
                        flag = True
                        flag, argus = input_argus(flag)
                        if flag == False:
                            break    
                        run_box(argus)
                        save_argus(argus)
                elif mode_layer_2 == '2':
                    while True:
                        flag = True
                        flag, argus = read_argus(flag)
                        if flag == False:
                            break
                        run_box(argus)
                elif mode_layer_2 == 'exit':
                    break
                else:
                    print('\n请输入数字1或数字2,按回车结束')
                    continue
        elif mode_layer_1 == 'exit':
            os._exit(0)        
        else:
            print('\n请输入数字1或数字2,按回车结束')
            continue
 
if __name__ == '__main__':
    run()
