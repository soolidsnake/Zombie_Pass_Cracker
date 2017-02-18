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


int next_string_rec(char string[], int current_case);
int hasher(char final_hash[]);


int main(int argc, char *argv[])
{
    int sockfd = 0, n = 0;
    char recvBuff[1024] = {0};
    char string[64] = {0};
    char initial_hash[512] = {0};
    char final_hash[512] = {0};
    int per_time = 0;
    struct sockaddr_in serv_addr = {0}; 

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000); 
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    printf("Connected\n");

    /***************************************/
    /*            Initiate data             */
    /***************************************/

    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    per_time = atoi(recvBuff);
    printf("per_time : %d \n",per_time);

    send(sockfd, "ok", sizeof("ok")-1, 0);

    n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
    recvBuff[n] = 0;
    strcpy(initial_hash, recvBuff);    
    printf("initial_hash : %s \n", initial_hash);
    
    send(sockfd, "READY", sizeof("READY"),0);
    printf("I'M READY\n");
    
    /* Main loop */

    while(1)
    {
        int found = 0;
        n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
        recvBuff[n] = 0;
        strcpy(string, recvBuff);

        printf("starting string : %s \n\n\n\n",string);

        int i;
        for(i=0; i<per_time; i++)
        {
            sleep(0.2);

            strcpy(final_hash, string);
            hasher(final_hash);
            printf("string %s final_hash %s\n", string, final_hash);
            if(strcmp(initial_hash, final_hash) == 0)
            {
                send(sockfd, "FOUND", sizeof("FOUND")-1,0);
                n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
                printf("Gg\n");
                found = 1;
                break;
            }

            next_string_rec(string, strlen(string)-1);        
        }


        if(found != 0)
            break;
        
        send(sockfd, "NOTFOUND", sizeof("NOTFOUND"),0);
        printf("not found re-trying with new beginning\n");
        //sleep(1);
    }

    return (0);
}


int next_string_rec(char string[], int current_case)
//recursive function to calculate the next string 
//example: "aaa" => "aab"

{
    if((int)string[current_case] >= 122)
    {
        string[current_case] = string[current_case] - 26;
        next_string_rec(string, current_case-1);
    }
    string[current_case] = ++string[current_case];
    
    return(0);
}


int hasher(char final_hash[])
{
    //CEASAR ENCRYPTION

    int i = 0;
    for(i=0; i<strlen(final_hash); i++)
    {
        if((int)final_hash[i] >= 122)
            final_hash[i] = final_hash[i] - 26;
        
        final_hash[i]++;
    }
}