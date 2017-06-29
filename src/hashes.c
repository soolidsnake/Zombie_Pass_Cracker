#include <mhash.h>
#include <string.h>


#include "hashes.h"

/* Function prototypes */

void md5_hash(const uint8_t *message, size_t len, uint32_t hash[4]);
void sha512_hash(const uint8_t *message, size_t len, uint64_t hash[8]);

// Link this program with an external C or x86 compression function
extern void md5_compress(uint32_t state[4], const uint8_t block[64]);
extern void sha512_compress(uint64_t state[8], const uint8_t block[128]);

/* entry point ==================================================================================================================================== */


void md5_hash(const uint8_t *message, size_t len, uint32_t hash[4]) {
    hash[0] = UINT32_C(0x67452301);
    hash[1] = UINT32_C(0xEFCDAB89);
    hash[2] = UINT32_C(0x98BADCFE);
    hash[3] = UINT32_C(0x10325476);
    
    size_t i;
    for (i = 0; len - i >= 64; i += 64)
        {
            md5_compress(hash, &message[i]);
        }
    uint8_t block[64];
    size_t rem = len - i;
    memcpy(block, &message[i], rem);
    
    block[rem] = 0x80;
    rem++;
    if (64 - rem >= 8)
        memset(&block[rem], 0, 56 - rem);
    else {
        memset(&block[rem], 0, 64 - rem);
        md5_compress(hash, block);
        memset(block, 0, 56);
    }
    
    block[64 - 8] = (uint8_t)((len & 0x1FU) << 3);
    len >>= 5;
    for (i = 1; i < 8; i++, len >>= 8)
        block[64 - 8 + i] = (uint8_t)len;
    md5_compress(hash, block);
}


void sha512_hash(const uint8_t *message, size_t len, uint64_t hash[8]) {
    hash[0] = UINT64_C(0x6A09E667F3BCC908);
    hash[1] = UINT64_C(0xBB67AE8584CAA73B);
    hash[2] = UINT64_C(0x3C6EF372FE94F82B);
    hash[3] = UINT64_C(0xA54FF53A5F1D36F1);
    hash[4] = UINT64_C(0x510E527FADE682D1);
    hash[5] = UINT64_C(0x9B05688C2B3E6C1F);
    hash[6] = UINT64_C(0x1F83D9ABFB41BD6B);
    hash[7] = UINT64_C(0x5BE0CD19137E2179);
    
    #define BLOCK_SIZE 128  // In bytes
    #define LENGTH_SIZE 16  // In bytes
    
    size_t off;
    for (off = 0; len - off >= BLOCK_SIZE; off += BLOCK_SIZE)
        sha512_compress(hash, &message[off]);
    
    uint8_t block[BLOCK_SIZE] = {0};
    size_t rem = len - off;
    memcpy(block, &message[off], rem);
    
    block[rem] = 0x80;
    rem++;
    if (BLOCK_SIZE - rem < LENGTH_SIZE) {
        sha512_compress(hash, block);
        memset(block, 0, sizeof(block));
    }
    
    block[BLOCK_SIZE - 1] = (uint8_t)((len & 0x1FU) << 3);
    len >>= 5;
    int i = 1; 
    for (i = 1; i < LENGTH_SIZE; i++, len >>= 8)
        block[BLOCK_SIZE - 1 - i] = (uint8_t)(len & 0xFFU);
    sha512_compress(hash, block);
}
