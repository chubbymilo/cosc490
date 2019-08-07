#include "stdio.h"
#include "time.h"

void n_time(void){
    struct timespec ts;
    timespec_get(&ts, TIME_UTC);
    printf ("%lld%.9ld", (long long)ts.tv_sec, ts.tv_nsec);
}
int main(void){
    n_time();
}