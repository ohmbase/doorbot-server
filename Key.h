#ifndef RRDCLIENT_KEY_H
#define RRDCLIENT_KEY_H

#include <sha256.h>

#define RRDCLIENT_KEY_SIZE 32

typedef struct Key { byte x[RRDCLIENT_KEY_SIZE]; } Key;

void stringToKey(String const& s, Key &k); //!< helper to convert a string to a key
String bytesToHex(const byte* bytes, uint16_t length); //!< helper to convert blob of data to hex

#endif