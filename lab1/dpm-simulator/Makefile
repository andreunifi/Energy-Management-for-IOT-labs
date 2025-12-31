TARGET = dpm_simulator
CC = gcc
CFLAGS = -Wall -g
INCDIR = "."

.PHONY: default clean docs idle sleep

default: $(TARGET)

SOURCES = $(wildcard src/*.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCES))
HEADERS = $(wildcard $(INCDIR)/*.h)

%.o: %.c $(TARGET).c $(HEADERS)
	$(CC) $(CFLAGS) -I$(INCDIR) -c $< -o $@

$(TARGET): $(OBJECTS) $(TARGET).o
	$(CC) $(TARGET).o $(OBJECTS) $(CFLAGS) -I$(INCDIR) -o $@ 

idle:
	$(MAKE) CFLAGS="$(CFLAGS) -DIDLE" clean $(TARGET)

sleep:
	$(MAKE) CFLAGS="$(CFLAGS) -DSLEEP" clean $(TARGET)

history1:
	$(MAKE) CFLAGS="$(CFLAGS) -DHISTORY1" clean $(TARGET)

history2:
	$(MAKE) CFLAGS="$(CFLAGS) -DHISTORY2" clean $(TARGET)

docs: Doxyfile $(HEADERS) $(wildcard src/*.c)
	doxygen $<

clean:
	-rm -f src/*.o
	-rm -f $(TARGET).o
	-rm -f $(TARGET)
