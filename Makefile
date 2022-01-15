NAME		= TNM.exe

SRC			= TNM.cpp
SRCS		= ${addprefix ./src/, ${SRC}}

INCLUDE		= -I ./include
SDL_INCLUDE	= -I ./sdl/include
SDL_LIB		= -L ./sdl/lib

CC=g++

all:
	${CC} ${SDL_INCLUDE} ${SDL_LIB} ${INCLUDE} ${SRCS} -o ${NAME} -lmingw32 -lSDL2main -lSDL2
