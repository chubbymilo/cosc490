#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include "unistd.h"

int main(int argc, char *argv[]){
struct timespec start;
struct timespec end;
struct timespec sleep_time;
int repeat, i;
long time_interval;


if(argc != 3){
    printf("Usage : [repeated times] [time interval in ns]\n");
    return -1;
}
char *a = argv[1];
repeat = atoi(a);
char *b = argv[2];
time_interval = atol(b);
sleep_time.tv_sec = 0;
sleep_time.tv_nsec = time_interval;
char buffer[20];
char buffer2[20];
int len;
long long start_time;
long long end_time;

timespec_get(&start, TIME_UTC);
for (i = 0; i < repeat; i++){
    nanosleep(&sleep_time, NULL);
}
timespec_get(&end, TIME_UTC);
printf ("Start time : %lld%09ld\n", (long long)start.tv_sec, start.tv_nsec);
printf ("End time : %lld%09ld\n", (long long)end.tv_sec, end.tv_nsec);
len = sprintf(buffer,"%lld%09ld", (long long)start.tv_sec, start.tv_nsec);
//printf("%d\n", len);
len = sprintf(buffer2,"%lld%09ld", (long long)end.tv_sec, end.tv_nsec);
start_time = atol(buffer);
end_time = atol(buffer2);
//printf("%lld\n", start_time);
printf("Duration: %lld\n", end_time-start_time);
}