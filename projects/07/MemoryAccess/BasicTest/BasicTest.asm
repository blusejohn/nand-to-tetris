@10
D=A
@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@LCL
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@21
D=A
@SP
A=M
M=D
@SP
M=M+1

@22
D=A
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@ARG
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@1
D=A
@ARG
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@36
D=A
@SP
A=M
M=D
@SP
M=M+1

@6
D=A
@THIS
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@42
D=A
@SP
A=M
M=D
@SP
M=M+1

@45
D=A
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@THAT
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@2
D=A
@THAT
D=D+M
@R13
M=D
@SP
AM=M-1
D=M
M=0
@R13
A=M
M=D

@510
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
M=0
@11
M=D

@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add 
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M

@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub 
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D-M

@6
D=A
@THIS
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@6
D=A
@THIS
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add 
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M

// sub 
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D-M

@11
D=M
@SP
A=M
M=D
@SP
M=M+1

// add 
@SP
AM=M-1
D=M
M=0
@SP
A=M-1
M=D+M

