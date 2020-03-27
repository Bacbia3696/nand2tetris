// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @KBD
    D=M;
    @PRESSED
    D; JNE
    // CLEAR SCREEN

    // i=0
    @i
    M=0
(CLEAR)
    // i == 8192 goto LOOP
    @8192
    D=A
    @i
    D=D-M;
    @LOOP
    D; JEQ

    // clear
    @i
    D=M
    @SCREEN
    A=D+A
    M=0

    // i = i + 1
    @i
    M=M+1

    @CLEAR
    0; JMP

(PRESSED)
    // DRAW SCREEN

    // i=0
    @i
    M=0
(DRAW)
    // i == 8192 goto LOOP
    @8192
    D=A
    @i
    D=D-M
    @LOOP
    D; JEQ

    // draw
    @i
    D=M
    @SCREEN
    A=D+A
    M=-1

    // i = i + 1
    @i
    M=M+1

    @DRAW
    0; JMP
