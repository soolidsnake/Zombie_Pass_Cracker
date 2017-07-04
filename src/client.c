#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h> 
#include <time.h>
#include <inttypes.h>// to get 8 bytes from strtoumax(...)

#include "hashes.h"
#include "constant.h"


/* Prototypes ===================================================================================================== */


int compare_hashes(uint64_t initial_hash[], uint64_t final_hash[], int limit);


/* Entry point ==================================================================================================== */


int main(int argc, char *argv[])
{

    char recvBuff[1024] = {0};
    char string[64] = {0};
    char combi_start[64] = {0};
    uint64_t initial_hash[128] = {0};
    uint64_t final_hash[128] = {0};
    int sockfd = 0;
    int n = 0;
    int per_time = 0;
    int choice = NULL;
    int string_length = 0;
    int found = 0;
    int i = 0, j=0;
    struct sockaddr_in serv_addr = {0}; 
    void (*hash_function) (const uint8_t*, size_t, uint64_t*) = NULL;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(12345); 
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    printf("Connected\n");

    /***************************************/
    /*            Initiate data            */
    /***************************************/

    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    choice = atoi(recvBuff);
    printf("choice : %d \n",choice);

    send(sockfd, "ok", sizeof("ok")-1, 0);
    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    per_time = atoi(recvBuff);
    printf("per_time : %d \n",per_time);

    send(sockfd, "ok", sizeof("ok")-1, 0);

    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    //printf("%s\n\n", recvBuff);

    /*
        The fellowing parse initial_hash to an array of int64, example :
        initial_hash = "12345678-abcdef12" =>
        [0x12345678, 0xabcdef12]
    */
    int limit = 0;
    char *p = NULL;
    p = recvBuff;
    p--;
    do
    {
        p++; 
        initial_hash[limit] = strtoumax(p, &p, 16);
        printf("%lx\n", initial_hash[limit]);
        limit++;

    }while(*p != '\0');

    //printf("%d\n",limit);

    /*******/

    send(sockfd, "ok", sizeof("ok")-1, 0);

    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    string_length = atoi(recvBuff);
    printf("\nstring_length : %d \n", string_length);
    send(sockfd, &READY, sizeof(char),0);
    printf("I'M READY\n");
    
    /* Main loop */


    long            ms; // Milliseconds
    time_t          s;  // Seconds
    struct timespec spec;

    /* Put the hash functions into the array 'hash_functions'. We use this to point to the right
       hash function inside the bruteforce loop.*/
    

    switch(choice) {
        case 0:
            hash_function = sha512_hash;
            break;
        case 1:
            hash_function = md5_hash;
            break;
    }


    while(1)
    {
    
        //clock_gettime(CLOCK_REALTIME, &spec);

        //ms = spec.tv_nsec; // Convert nanoseconds to milliseconds

        found = 0;
        n = read(sockfd, combi_start, string_length);
        combi_start[n] = 0;
        strcpy(string, combi_start);
        // printf("%s\n", combi_start);
        // sleep(3);

        //clock_gettime(CLOCK_REALTIME, &spec);

        //printf("%f\n",(spec.tv_nsec - ms)/1.0e6);

        //printf("starting string : %s \n\n",string);


        for(i=0; i<per_time; i++)
        {
            //printf("starting string : %s \n\n",string);
            //sleep(1);
            hash_function(string, string_length, final_hash);

            if(compare_hashes(initial_hash, final_hash, limit))
            {
                send(sockfd, &FOUND, sizeof(char),0);
                n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
                send(sockfd, string, string_length, 0);//Send password
                found = 1;
                break;
            }

            //Next string
            for(j = string_length - 1; j >= 0; j--)
            {
                if((int)string[j] >= 122)
                {
                    string[j] = string[j] - 25;
                    continue;
                }

                string[j] = ++string[j];
                break;
            }      
        }

        if(found != 0)
            break;
        
        send(sockfd, &NOT_FOUND, sizeof(char), 0);
        send(sockfd, combi_start, string_length, 0); //Send the failed combination
        // printf("sending %s\n", combi_start);
        //printf("not found re-trying with new beginning\n");
        //sleep(1);
    }

    return (0);
}

int compare_hashes(uint64_t initial_hash[], uint64_t final_hash[], int limit)
{
    int k=0;
    for(k= 0; k < limit; k++)
    {

        if(initial_hash[k] != final_hash[k])
            return 0;
    }
    return 1;  
}