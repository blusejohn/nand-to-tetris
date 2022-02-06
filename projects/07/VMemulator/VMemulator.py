#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 20:33:02 2022

@author: john
"""

ARGUMENT = 'argument'
CONSTANT = 'constant'
LOCAL = 'local'
POINTER = 'pointer'
STATIC = 'static'
TEMP = 'temp'
THAT = 'that'
THIS = 'this'

ARITHMETIC = 'C_ARITHMETIC'
PUSH = 'C_PUSH'
POP = 'C_POP'
GOTO = 'C_GOTO'
IF = 'C_IF'
FUNCTION = 'C_FUNCTION'
LABEL = 'C_LABEL'
CALL = 'C_CALL'
RETURN = 'C_RETURN'



Memory_Segments = {
    ARGUMENT: 'ARG',
    LOCAL: 'LCL',
    THAT: 'THAT',
    THIS: 'THIS'
}

label_counter = 0

# Push or Pop to stack

def push_stack_top():
    return('@SP\n'+
    'A=M\n'+
    'M=D\n'+
    '@SP\n'+
    'M=M+1\n')

def pop_stack_top():
    return('@SP\n'+
    'AM=M-1\n'+
    'D=M\n'+
    'M=0\n')




def push_const_value_to_stack(index):
    return ('@{}\n'.format(index) +
    'D=A\n'+
    '@SP\n'+
    'A=M\n'+
    'M=D\n'+
    '@SP\n'+
    'M=M+1\n')


def push_static_value(index, file):
    return('@{}_{}\n'.format(file,index) +
    'D=M\n' +
    push_stack_top())

def pop_static_value(index, file):
    return(pop_stack_top()+
    '@{}_{}\n'.format(file,index)+
    'M=D\n')
    
def push_register_value(register):
    return('@{}\n'.format(register) +
    'D=M\n' +
    push_stack_top())
    
    
def pop_register_value(register):
    return(pop_stack_top()+
    '@{}\n'.format(register)+
    'M=D\n')
    
def push_segment_value_to_stack(segment,index):
    return ('@{}\n'.format(index)+
    'D=A\n'+
    '@{}\n'.format(segment)+
    'A=M+D\n'+
    'D=M\n'+
    push_stack_top())

def pop_stack_value_to_segment(segment,index):
    return ('@{}\n'.format(index)+
    'D=A\n'+
    '@{}\n'.format(segment)+
    'D=D+M\n'+
    '@R13\n'+
    'M=D\n'+
    pop_stack_top()+
    '@R13\n'+
    'A=M\n'+
    'M=D\n')



def push_handler(segment, val, file):
    if segment == CONSTANT:
        return push_const_value_to_stack(val)
    index = val
    if segment in [LOCAL, ARGUMENT, THIS, THAT]:
        bin_segment = Memory_Segments[segment]
        return push_segment_value_to_stack(bin_segment, index)
    elif segment == POINTER:
        register = str(3 + int(index))
        return push_register_value(register)
    elif segment == TEMP:
        register = str(5 + int(index))
        return push_register_value(register)
    elif segment == STATIC:
        return push_static_value(index, file)
    else:
        raise Exception('Incorrect segment {}'.format(segment))
        

def pop_handler(segment, index, file):
    if segment == CONSTANT:
        raise Exception('Incorrect segment {} for pop command'.format(segment))
    if segment in [LOCAL, ARGUMENT, THIS, THAT]:
        bin_segment = Memory_Segments[segment]
        return pop_stack_value_to_segment(bin_segment, index)
    elif segment == POINTER:
        register = str(3 + int(index))
        return pop_register_value(register)
    elif segment == TEMP:
        register = str(5 + int(index))
        return pop_register_value(register)
    elif segment == STATIC:
        return pop_static_value(index, file)
    else:
        raise Exception('Incorrect segment {}'.format(segment))


#Arithmetic operation



def add_function():
    return('@SP\n'+
            'AM=M-1\n'+
            'D=M\n'+
            'M=0\n'+
            '@SP\n'+
            'A=M-1\n'+
            'M=D+M\n')

def sub_function():
    return('@SP\n'+
            'AM=M-1\n'+
            'D=M\n'+
            'M=0\n'+
            '@SP\n'+
            'A=M-1\n'+
            'M=D-M\n')

def and_function():
    return('@SP\n'+
            'AM=M-1\n'+
            'D=M\n'+
            'M=0\n'+
            '@SP\n'+
            'A=M-1\n'+
            'M=D&M\n')

def or_function():
    return('@SP\n'+
            'AM=M-1\n'+
            'D=M\n'+
            'M=0\n'+
            '@SP\n'+
            'A=M-1\n'+
            'M=D|M\n')

def neg_function():
    return('@SP\n'+
    'A=M-1\n'+
    'M=-M\n')

def not_function():
    return('@SP\n'+
    'A=M-1\n'+
    'M=!M\n')

def _compare(assembly_comp):
    """
    """
    # Use label_counter to create different labels
    global label_counter

    true_label = 'TRUE_{}'.format(label_counter)
    false_label = 'FALSE_{}'.format(label_counter)
    continue_label = 'CONTINUE_{}'.format(label_counter)
    label_counter += 1
    return (_prepare_for_binary() +
            'D=M-D\n' +
            '@{}\n'.format(true_label) +
            'D;{}\n'.format(assembly_comp) +
            '@{}\n'.format(false_label) +
            '0;JMP\n' +
            '(' + true_label + ')\n' +
            '@SP\n' +
            'A=M-1\n' +
            'M=-1\n' +
            '@{}\n'.format(continue_label) +
            '0;JMP\n' +
            '(' + false_label + ')\n' +
            '@SP\n' +
            'A=M-1\n' +
            'M=0\n' +
            '@{}\n'.format(continue_label) +
            '0;JMP\n' +
            '(' + continue_label + ')\n')


def eq_handler():
    return _compare('JEQ')


def gt_handler():
    return _compare('JGT')


def lt_handler():
    return _compare('JLT')

def arithmetic_handler(type):
    return '// {} \n{}'.format(type, {
        'add': add_function,
        'sub': sub_function,
        'neg': neg_function,
        'eq': eq_handler,
        'gt': gt_handler,
        'lt': lt_handler,
        'and': and_function,
        'or': or_function,
        'not': not_function
    }[type]())

def goto_function(label):
    return('@{}\n'.format(label)+
    '0;JMP\n')

def if_goto_function(label):
    return('@{}\n'.format(label)+
    'D;JNE\n')

def label_function(label):
    return('({})\n'.format(label))


def function_handler(function_name, num_locals):
    initialize_locals = ''
    for local in range(int(num_locals)):
        initialize_locals += push_const_value_to_stack(0)
        initialize_locals += pop_stack_value_to_segment('LCL',
                                                               str(local))

    return ('// declare {} with locals {}'.format(function_name, num_locals) +
            label_function(function_name) +
            initialize_locals)




def call_handler(function_name, num_args):
    global label_counter
    continuation_address = 'continuation_{}_{}'.format(function_name,
                                                       label_counter)
    label_counter += 1
    return ('// call fn {} with locals {}\n'.format(function_name, num_args) +
            '@{}\n'.format(continuation_address) +
            'D=A\n' +
            push_stack_top() +  # Store return address (caller) in stack
            '@LCL\n' +
            'D=M\n' +
            push_stack_top() +  # Store LCL address (caller) in stack
            '@ARG\n' +
            'D=M\n' +
            push_stack_top() +  # Store ARG address (caller) in stack
            '@THIS\n' +
            'D=M\n' +
            push_stack_top() +  # Store THIS address (caller) in stack
            '@THAT\n' +
            'D=M\n' +
            push_stack_top() +  # Store THAT address (caller) in stack
            '@SP\n' +
            'D=M\n' +
            '@5\n' +
            'D=D-A\n' +
            '@{}\n'.format(num_args) +
            'D=D-A\n' +
            '@ARG\n' +  # NOQA Set current ARG address to stack head -5 (state of caller) - num_args (prev pushed to stack)
            'M=D\n' +
            '@SP\n' +
            'D=M\n' +
            '@LCL\n' +
            'M=D\n' +  # Set current LCL address to stack head
            goto_function(function_name) +
            label_function(continuation_address)
            )


def return_handler():
    frame_address_pointer = 'R13'  # NOQA temp address used to store the base frame address
    continue_address_pointer = 'R14'  # NOQA temp address used to store the address of
    return ('// return\n'
            '@LCL\n'
            'D=M\n'
            '@{}\n'.format(frame_address_pointer) +
            'M=D\n'  # NOQA Store in frame_address_pointer (temp) the value of LCL (head of stack at beginning of call execution)
            '@5\n'
            'D=D-A\n'  # D now holds the address of return pointer
            'A=D\n'
            'D=M\n'
            '@{}\n'.format(continue_address_pointer) +
            'M=D\n' +  # NOQA Store continuation_address in continue_address_pointer (return address was previously set in call_handler)
            pop_stack_top() +
            '@ARG\n'
            'A=M\n'
            'M=D\n'  # Set ARG [0] to return value of function
            'D=A+1\n'  # Next stack head should be the value of ARG[0] + 1
            '@SP\n'
            'M=D\n'  # NOQA Set stack head to point to one address above where we store the returned value
            '@{}\n'.format(frame_address_pointer) +
            'A=M-1\n'
            'D=M\n'
            '@THAT\n'
            'M=D\n'  # Set the caller's THAT to its previous value
            '@2\n'
            'D=A\n'
            '@{}\n'.format(frame_address_pointer) +
            'D=M-D\n'
            'A=D\n'
            'D=M\n'
            '@THIS\n'
            'M=D\n'  # Set the caller's THIS to its previous value
            '@3\n'
            'D=A\n'
            '@{}\n'.format(frame_address_pointer) +
            'D=M-D\n'
            'A=D\n'
            'D=M\n'
            '@ARG\n'
            'M=D\n'  # Set the caller's ARG to its previous value
            '@4\n'
            'D=A\n'
            '@{}\n'.format(frame_address_pointer) +
            'D=M-D\n'
            'A=D\n'
            'D=M\n'
            '@LCL\n'
            'M=D\n'  # Set the caller's LCL to its previous value
            '@{}\n'.format(continue_address_pointer) +
            'A=M\n'  # Load the return address to continue executing caller
            '0;JMP\n'
            )





def get_command_type(split_command):
    try:
        return{
            'add': ARITHMETIC,
            'sub': ARITHMETIC,
            'neg': ARITHMETIC,
            'eq': ARITHMETIC,
            'gt': ARITHMETIC,
            'lt': ARITHMETIC,
            'and': ARITHMETIC,
            'or': ARITHMETIC,
            'not': ARITHMETIC,
            'push': PUSH,
            'pop': POP,
            'goto': GOTO,
            'label': LABEL,
            'if-goto': IF,
            'function': FUNCTION,
            'call': CALL,
            'return': RETURN
        }[split_command[0]]
    except (KeyError, IndexError):
        raise Exception(
            'Invalid vm command: {}'.format(' '.join(split_command)))
        
def get_first_arg(split_command, command_type):
    if command_type == RETURN:
        return None
    elif command_type == ARITHMETIC:
        return split_command[0]
    try:
        return split_command[1]
    except IndexError:
        raise Exception(
            'Invalid vm command: {}'.format(' '.join(split_command)))


def get_second_arg(split_command, command_type):
    if command_type in [PUSH, POP, CALL, FUNCTION]:
        try:
            return split_command[2]
        except (IndexError, ValueError):
            raise Exception(
                'Invalid vm command: {}'.format(' '.join(split_command)))
        
def _remove_comments_and_whitespace(line):
    without_comments = line.split('/')[0]
    return without_comments.replace('\r\n', '').strip()        
        

def input_preprcess(inputFile):
    lines = inputFile.readlines()
    parse_result = []
    ##Take away '//' and empty line
    for line in lines:
        if(line == '\n'):
            continue
        elif(line[0]=='/'):
            continue
        line = line.replace("\n", "")
        line = line.split('//', 1)[0]
        parse_result.append(line)
    return parse_result


def parser(file_name):
    file_input = open(file_name, "r")
    for line in file_input.readlines():
        command = _remove_comments_and_whitespace(line)
        if not command:
            continue
        split_command = command.split(' ')
        command_type = get_command_type(split_command)
        arg1 = get_first_arg(split_command, command_type)
        arg2 = get_second_arg(split_command, command_type)
        yield command_type, arg1, arg2
    
    
def write_command_function(command_type, arg1, arg2, file):
    try:
        return {
            ARITHMETIC: lambda: arithmetic_handler(arg1),
            PUSH: lambda: push_handler(arg1, arg2, file),
            POP: lambda: pop_handler(arg1, arg2, file),
            GOTO: lambda: goto_function(arg1),
            IF: lambda: if_goto_function(arg1),
            FUNCTION: lambda: function_handler(arg1, arg2),
            LABEL: lambda: label_function(arg1),
            CALL: lambda: call_handler(arg1, arg2),
            RETURN: lambda: return_handler()
        }[command_type]()
    except KeyError:
        raise Exception('Invalid command_type {} for '
                        'assembly_command_constructor'.format(command_type))



        
    