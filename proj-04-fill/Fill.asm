// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
// Functionality: Black the screen on keypres, whiten if no keypree
// LOOP:
// if RAM[KEYBOARD] = 0:
//   offset = 0
//   WHITEN:
//     if offset = 2^13
//       goto LOOP
//     RAM[SCREEN + offset] = 0
//     offset = offset + 1
//   goto WHITEN
// else if RAM[KEYBOARD] != 0:
//   offset = 0
//   BLACKEN:
//     if offset = 2^13
//       goto LOOP
//     RAM[SCREEN + offset] = -1
//     offset = offset + 1
//    goto BLACKEN

(LOOP)
@SCREEN
D=A
@pointer
M=D
@KBD
D=M
@BLACKEN
D;JGT

(WHITEN)
@KBD
D=A
@pointer
D=D-M
@LOOP
D;JEQ
@pointer
A=M
M=0
@pointer
M=M+1
@WHITEN
0;JMP

(BLACKEN)
@KBD
D=A
@pointer
D=D-M
@LOOP
D;JEQ
@pointer
A=M
M=-1
@pointer
M=M+1
@BLACKEN
0;JMP
