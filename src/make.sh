rm -r Release
mkdir Release
gcc client.c hashes.c md5-fast-64.S sha512-64.S -o ./Release/Zombie_Pass_Cracker
./Release/Zombie_Pass_Cracker