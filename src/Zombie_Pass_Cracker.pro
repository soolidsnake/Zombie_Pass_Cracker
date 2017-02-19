TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

LIBS += -lmhash

SOURCES += client.c \
    hashes.c

HEADERS += \
    hashes.h
