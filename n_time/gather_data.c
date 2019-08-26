#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include "unistd.h"
/*
void n_time(void){
    struct timespec ts;
    char buffer[100];
    int len;
    int i;
    timespec_get(&ts, TIME_UTC);
    printf ("%lld%09ld", (long long)ts.tv_sec, ts.tv_nsec);
    len = sprintf(buffer, "%lld%09ld", (long long)ts.tv_sec, ts.tv_nsec);
    printf("\n");
    for (i = 0; i < len; i++){
        printf("%c", buffer[i]);
    }
    printf("%d\n", len);

}
*/
void read_memory(const char* filename_in, const char* filename_out){
    struct timespec ts;
    FILE *fp;
    char buffer[5000];
    int nread;
    int nwrite;
    int len;
    int i;

    fp = fopen(filename_in,"r");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    timespec_get(&ts, TIME_UTC); //get current time.
    len = sprintf(buffer, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
  
    nread = fread(buffer+len, 1, sizeof(buffer), fp); //read data from file to the buffer at the position +len(length of the current time).
    fclose(fp);
    
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    nwrite = fwrite(buffer, 1, (len+nread), fp);
    fclose(fp);
}
int main(int argc, char *argv[]){
    int i;
    struct timespec sleep_time;
    char *a = argv[3];
    char *b = argv[4];
    int repeat =atoi(a);
    long sleep = atol(b);
    sleep_time.tv_sec = 0;
    sleep_time.tv_nsec = sleep;
    if(argc != 5){
        printf("Usage: [target file path][output file path][repeated times][sleep time interval]\n");
        return -1;
    }
     /*
    time_t start = time(NULL);
    time_t now = time(NULL);
    while ((now - start) <= 20) {
        myfunc();
        time_t now = time(NULL);
    }*/
    for(i = 0; i < repeat; i++){
        read_memory(argv[1], argv[2]);
        nanosleep(&sleep_time,NULL);
    }
    //n_time();
    //read_file("/sys/fs/cgroup/memory/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/memory.stat","/tmp/memory_test.txt");
}