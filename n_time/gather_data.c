#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include "unistd.h"
#include "errno.h"
#include "string.h"
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
void read_cpu(const char* filename_in, const char* filename_out){
    struct timespec ts;
    FILE *fp;
    FILE *fd;
    char buffer[5000];
    int nread;
    int nwrite;
    int len;
    int i;
    int count = 0;
    int line_num;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;

    char *line2 = NULL;
    size_t length2 = 0;
    ssize_t numread2;

    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        return;
    }

    fd = fopen("/proc/stat","r");
    if (fd == NULL){
        perror("open file:");
        return;
    }

    timespec_get(&ts, TIME_UTC); //get current time.
    len = sprintf(buffer, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    line_num = 0;

    if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        return;
    }
     if ((numread2 = getline(&line2, &length2, fd)) < 0){
        perror("getline: ");
        return;
    }

    if (sprintf(buffer+len, "%s", line) < 0){
                 perror("sprintf:");
                 return;
             }

    if (sprintf(buffer+len+numread, "%s", line2) < 0){
                 perror("sprintf:");
                 return;
             }
    



    /*
     while ((numread = getline(&line, &length, fp)) != -1){
         printf("%ld\n", numread);
         if (count == line_num){
             if (sprintf(buffer+len, "%s",line) < 0){
                 perror("sprintf:");
             }
             break;
         }
         else{
             count++;
         }
     }
     */
     
    free(line);
    free(line2);
    //nread = fread(buffer+len, 1, sizeof(buffer), fp); //read data from file to the buffer at the position +len(length of the current time).
    fclose(fp);
    fclose(fd);
    
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    nwrite = fwrite(buffer, 1, (len+numread+numread2), fp);
    fclose(fp);
}

void read_memory(const char* filename_in, const char* filename_in2, const char* filename_out){
    struct timespec ts;
    FILE *fp;
    FILE *fd;
    char buffer[5000];
    int nread;
    int nwrite;
    int len;
    int i;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;
    
    char *line2 = NULL;
    size_t length2 = 0;
    ssize_t numread2;

 
    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        return;
    }

    fd = fopen(filename_in2,"r");
    if (fd == NULL){
        perror("open file: ");
        return;
    }

    timespec_get(&ts, TIME_UTC); //get current time.
    len = sprintf(buffer, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.

    if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        return;
    }

     if ((numread2 = getline(&line2, &length2, fd)) < 0){
        perror("getline: ");
        return;
    }
    
    if (sprintf(buffer+len, "%s", line) < 0){
                 perror("sprintf:");
                 return;
             }

    if (sprintf(buffer+len+numread, "%s", line2) < 0){
                 perror("sprintf:");
                 return;
             }   
    free(line);
    free(line2);
    //nread = fread(buffer+len, 1, sizeof(buffer), fp); //read data from file to the buffer at the position +len(length of the current time).
    fclose(fp);
    fclose(fd);
    
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    nwrite = fwrite(buffer, 1, (len+numread+numread2), fp);
    fclose(fp);

}

void read_block(const char* filename_in, const char* filename_out){
    struct timespec ts;
    FILE *fp;
    char buffer[5000];
    int nread;
    int nwrite;
    int len;
    int i;
    int count = 0;
    int line_num;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;

    char *line2 = NULL;
    size_t length2 = 0;
    ssize_t numread2;

    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        return;
    }

    timespec_get(&ts, TIME_UTC); //get current time.
    len = sprintf(buffer, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    line_num = 0;

    if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        return;
    }
      if ((numread2 = getline(&line2, &length2, fp)) < 0){
        perror("getline: ");
        return;
    }
 
    if (sprintf(buffer+len, "%s", line) < 0){
                 perror("sprintf:");
                 return;
             }
    if (sprintf(buffer+len + numread, "%s", line2) < 0){
                 perror("sprintf:");
                 return;
             }





    /*
     while ((numread = getline(&line, &length, fp)) != -1){
         printf("%ld\n", numread);
         if (count == line_num){
             if (sprintf(buffer+len, "%s",line) < 0){
                 perror("sprintf:");
             }
             break;
         }
         else{
             count++;
         }
     }
     */
     
    free(line);
    free(line2);
    //nread = fread(buffer+len, 1, sizeof(buffer), fp); //read data from file to the buffer at the position +len(length of the current time).
    fclose(fp);
    
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    nwrite = fwrite(buffer, 1, (len+numread+numread2), fp);
    fclose(fp);
}

void read_network(const char* filename_in, const char* filename_out){
    struct timespec ts;
    FILE *fp;
    char buffer[5000];
    int nwrite;
    int len;
    int count = 0;
    int line_num;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;



    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        return;
    }

    timespec_get(&ts, TIME_UTC); //get current time.
    len = sprintf(buffer, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    line_num = 2; //for mac's vm, the number is 2, for windows is 5.
     while ((numread = getline(&line, &length, fp)) != -1){
         if (count == line_num){
             if (sprintf(buffer+len, "%s",line) < 0){
                 perror("sprintf:");
             }
             break;
         }
         else{
             count++;
         }
     }
     
    free(line);
    fclose(fp);
    
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        return;
    }
    nwrite = fwrite(buffer, 1, (len+numread), fp);
    fclose(fp);

}







int main(int argc, char *argv[]){
    int i;
    struct timespec sleep_time, start, end;
    char *a;
    char *b;
    int repeat;
    long sleep;
    sleep_time.tv_sec = 0;
    sleep_time.tv_nsec;
    long long start_time, end_time;
    char buffer[20];
    char buffer2[20];
    int len;

    
   
    if(argc != 5 && argc !=6){
        printf("Usage: [target file path][output file path][repeated times][sleep time interval]\n");
        printf("Usage: [target file path][target file path2][output file path][repeated times][sleep time interval]\n");
        printf("You entered: %d\n", argc);
        return -1;
    }
    if (argc == 5){
        a = argv[3];
        b = argv[4];
        repeat = atoi(a);
        sleep = atol(b);
        sleep_time.tv_nsec = sleep;
    }else{  
        a = argv[4];
        b = argv[5];
        repeat = atoi(a);
        sleep = atol(b);
        sleep_time.tv_nsec = sleep;
    }
     /*
    time_t start = time(NULL);
    time_t now = time(NULL);
    while ((now - start) <= 20) {
        myfunc();
        time_t now = time(NULL);
    }*/
        if( argc == 5){
            if ((strcmp(argv[2],"/tmp/cpu_log.txt")) == 0){
                timespec_get(&start, TIME_UTC);
                for(i = 0; i < repeat; i++){
            read_cpu(argv[1], argv[2]);
            nanosleep(&sleep_time,NULL);
        }
        timespec_get(&end, TIME_UTC);
            }else if((strcmp(argv[2],"/tmp/block_log.txt")) == 0){
                timespec_get(&start, TIME_UTC);    
        for(i = 0; i < repeat; i++){
            read_block(argv[1], argv[2]);
            nanosleep(&sleep_time,NULL);
        }
        timespec_get(&end, TIME_UTC);
            }else if ((strcmp(argv[2],"/tmp/network_log.txt")) == 0){
                timespec_get(&start, TIME_UTC);
                for(i = 0; i < repeat; i++){
            read_network(argv[1], argv[2]);
            nanosleep(&sleep_time,NULL);
        }
        timespec_get(&end, TIME_UTC);
            }else{
                printf("typo\n");
                return -1;
            }
        }else{
            timespec_get(&start,TIME_UTC);
        for(i = 0; i < repeat; i++){
            read_memory(argv[1], argv[2], argv[3]);
            nanosleep(&sleep_time,NULL);
        }
        timespec_get(&end, TIME_UTC);
        }

        printf ("Start time : %lld%09ld\n", (long long)start.tv_sec, start.tv_nsec);
        printf ("End time : %lld%09ld\n", (long long)end.tv_sec, end.tv_nsec);
        len = sprintf(buffer,"%lld%09ld", (long long)start.tv_sec, start.tv_nsec);
        len = sprintf(buffer2,"%lld%09ld", (long long)end.tv_sec, end.tv_nsec);
        start_time = atol(buffer);
        end_time = atol(buffer2);
        printf("Duration: %lld\n", end_time-start_time);
    //n_time();
    //read_file("/sys/fs/cgroup/memory/docker/972e3860906ba4392f9b28bfbe085eda6e58a68e8c995721bbd77c7ccc263978/memory.stat","/tmp/memory_test.txt");
}