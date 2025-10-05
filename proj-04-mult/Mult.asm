// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// Function: Multiply two positive integers m and n. 
// Precondition: m is stored in RAM[0] and n is stored in RAM[1] 
// Postcondition: m*n is stored in RAM[2] 
// Comment: Use Hack Assembly Language; Assume the input is correct and that m*n <= 2^15 

// Pseudo-Code
// i = 0
// R2 = 0
// LOOP:
// if i == R1:
    // goto END
// R2 = R2 + R0
// i = i + 1
// goto LOOP
// 
// END:
// goto END

// Hack Assembly
@i
M=0
@R2
M=0

(LOOP)
@i
D=M
@R1
D=D-M
@END
D;JEQ

@R0
D=M
@R2
M=D+M
@i
M=M+1
@LOOP
0;JMP

(END)
@END
