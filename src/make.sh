rm -r Release
mkdir Release 2> /dev/null
qmake Zombie_Pass_Cracker.pro -o Release/
cd Release
make
./Zombie_Pass_Cracker
