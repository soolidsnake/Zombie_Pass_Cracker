#ifndef HASHES_H
#define HASHES_H


/* entry point ==================================================================================================================================== */

/**
 * @brief Calculate md5 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 32 bytes.
 * @return 0 if success, else -1.
 */
int hash_md5(const char original_str[], char hash[]);


/**
 * @brief Calculate md5 hash from the original_str[] and store the result in vector_hash[] in the form of
 *      an array (Ex : {255, 16...}.
 * @param vector_hash[] the minimum size of this array is 16 bytes.
 * @return return the size of the array vector_hash[] or -1 if an error has occured.
 */
int hash_md5_vector(const char original_str[], unsigned char vector_hash[]);


/**
 * @brief Calculate sha1 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 40 bytes.
 * @return 0 if success, else -1.
 */
int hash_sha1(const char original_str[], char hash[]);


/**
 * @brief Calculate sha224 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 56 bytes.
 * @return 0 if success, else -1.
 */
int hash_sha224(const char original_str[], char hash[]);


/**
 * @brief Calculate sha256 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 64 bytes.
 * @return 0 if success, else -1.
 */
int hash_sha256(const char original_str[], char hash[]);


/**
 * @brief Calculate sha384 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 48 bytes.
 * @return 0 if success, else -1.
 */
int hash_sha384(const char original_str[], char hash[]);


/**
 * @brief Calculate 512 hash from the original_str[] and store the result in the form of a string (Ex : "ff10..") in hash[] .
 * @param hash[] the minimum size of this array is 64 bytes.
 * @return 0 if success, else -1.
 */
int hash_sha512(const char original_str[], char hash[]);

#endif // HASHES_H
