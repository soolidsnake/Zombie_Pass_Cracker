#ifndef HASHES_H
#define HASHES_H

#include <inttypes.h>
#include <string.h>

/* entry point ==================================================================================================================================== */


/**
 * @brief 
 * @param message
 * @param len
 * @param hash[4]
 * @return 
 */
void md5_hash(const uint8_t *message, size_t len, uint32_t hash[4]);

/**
 * @brief 
 * @param message
 * @param len
 * @param hash[8]
 * @return 
 */
void sha512_hash(const uint8_t *message, size_t len, uint64_t hash[8]);

#endif // HASHES_H
