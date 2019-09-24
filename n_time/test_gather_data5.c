#include "stdio.h"
#include "time.h"
#include "stdlib.h"
#include "unistd.h"
#include "errno.h"
#include "string.h"

void read_cpu(const char* filename_in, char *buffer, int *count){
    struct timespec ts;
    FILE *fp;
    int len;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;

    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        exit(-1);
    }

 if(clock_gettime(CLOCK_REALTIME, &ts) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
    //diff = 1000000000 *(ts.tv_sec) + ts.tv_nsec;

    //len = sprintf(buffer + *count, "%lld\n", diff); //format the time and put it into the buffer.
    if((len = sprintf(buffer+ *count, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec)) < 0 ){
        perror("sprintf :");
        exit(-1);
    }
    *count+=len;

 if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        exit(-1);
    }

    if (sprintf(buffer+ *count, "%s", line) < 0){
                 perror("sprintf:");
                 exit(-1);
             }
    free(line);
    *count += numread;
    fclose(fp);
   
}

void read_memory(const char* filename_in2, char *buffer, int *count){
    struct timespec ts;
    //FILE *fp;
    FILE *fd;

    int len;
    /*
    char *line = NULL;
    size_t length = 0;
    ssize_t numread;
    */
    char *line2 = NULL;
    size_t length2 = 0;
    ssize_t numread2;

    /*
    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        exit(-1);
    }
    */
    

    fd = fopen(filename_in2,"r");
    if (fd == NULL){
        perror("open file: ");
        exit(-1);
    }
    /*
    if(timespec_get(&ts, TIME_UTC) ==0){
        perror("timespec_get");
        exit(-1);
    } //get current time.
    */
     if(clock_gettime(CLOCK_REALTIME, &ts) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
                
    if((len = sprintf(buffer+ *count, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec)) < 0 ){
        perror("sprintf :");
        exit(-1);
    } //format the time and put it into the buffer.
    /*
    if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        exit(-1);
    }
    */
    *count+= len;
     if ((numread2 = getline(&line2, &length2, fd)) < 0){
        perror("getline: ");
        exit(-1);
    }
    /*
    if (sprintf(buffer+len, "%s", line) < 0){
                 perror("sprintf:");
                 exit(-1);
             }
*/
    if (sprintf(buffer+ *count, "%s", line2) < 0){
                 perror("sprintf:");
                 exit(-1);
             }   
    //free(line);
    free(line2);
    *count+= numread2;
    //nread = fread(buffer+len, 1, sizeof(buffer), fp); //read data from file to the buffer at the position +len(length of the current time).
    //fclose(fp);
    fclose(fd);
    /*
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if (fwrite(buffer, 1, (len+numread+numread2), fp) < 0 ){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    */

}

void read_block(const char* filename_in, char *buffer, int *count){
    struct timespec ts;
    FILE *fp;
    //char buffer[500];
    int len;
  
    char *line = NULL;
    size_t length = 0;
    ssize_t numread;

    char *line2 = NULL;
    size_t length2 = 0;
    ssize_t numread2;

    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        exit(-1);
    }
    /*
     if(timespec_get(&ts, TIME_UTC) ==0){
        perror("timespec_get");
        exit(-1);
    } //get current time.
    */
     if(clock_gettime(CLOCK_REALTIME, &ts) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
                
    len = sprintf(buffer + *count, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    *count += len;

    if ((numread = getline(&line, &length, fp)) < 0){
        perror("getline: ");
        exit(-1);
    }
      if ((numread2 = getline(&line2, &length2, fp)) < 0){
        perror("getline: ");
        exit(-1);
    }
 
    if (sprintf(buffer+ *count, "%s", line) < 0){
                 perror("sprintf:");
                 exit(-1);
             }
    *count+= numread;

    if (sprintf(buffer+ *count, "%s", line2) < 0){
                 perror("sprintf:");
                 exit(-1);
             }
    *count+= numread2;


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
    /*
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if(fwrite(buffer, 1, (len+numread+numread2), fp) < 0){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    */
    
}

void read_network(const char* filename_in, char *buffer, int *count, int target_index){
    struct timespec ts;
    FILE *fp;
    //char buffer[500];
    int len;
    int count_tmp = 0;
    int line_num;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;



    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        exit(-1);
    }
    /*
       if(timespec_get(&ts, TIME_UTC) ==0){
        perror("timespec_get");
        exit(-1);
    } //get current time..
    */
     if(clock_gettime(CLOCK_REALTIME, &ts) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
    len = sprintf(buffer + *count, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    *count+=len;
    line_num = target_index; //for mac's vm, the number is 2, for windows is 5 or 4?.
     while ((numread = getline(&line, &length, fp)) != -1){
         if (count_tmp == line_num){
             if (sprintf(buffer+ *count, "%s",line) < 0){
                 perror("sprintf:");
             }
             break;
         }
         else{
             count_tmp++;
         }
     }
     *count+=numread;
    //printf("numread %ld\n", numread);
    free(line);
    fclose(fp);
    /*
    fp = fopen(filename_out,"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if (fwrite(buffer, 1, (len+numread), fp) < 0){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    */

}

long long diff_time(struct timespec start, struct timespec end)
{
	struct timespec temp;
    long long diff;
	if ((end.tv_nsec-start.tv_nsec)<0) {
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1000000000+end.tv_nsec-start.tv_nsec;
	}else{
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}
    diff =  1000000000 *(temp.tv_sec) + temp.tv_nsec;
    return (diff);
}

void read_metrics(const char* filename_in, char *buffer, int *count, int target_index, const char* resource){
    struct timespec ts;
    FILE *fp;

    int len;
    int count_tmp = 0;
    int line_num;

    char *line = NULL;
    size_t length = 0;
    ssize_t numread;

    int block = 1; 

    if (strcmp(resource, "block") == 0){
        block =0;
    }
    fp = fopen(filename_in,"r");
    if (fp == NULL){
        perror("open file: ");
        exit(-1);
    }

     if(clock_gettime(CLOCK_REALTIME, &ts) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

    len = sprintf(buffer + *count, "%lld%09ld\n", (long long)ts.tv_sec, ts.tv_nsec); //format the time and put it into the buffer.
    *count+=len;

     while ((numread = getline(&line, &length, fp)) != -1){
         if (count_tmp == target_index){
             if (sprintf(buffer+ *count, "%s",line) < 0){
                 perror("sprintf:");
             }
            *count+=numread;
             goto end;
         }
         else{
             if (block == 0){
                  if (sprintf(buffer+ *count, "%s",line) < 0){
                 perror("sprintf:");
             }
            *count+=numread;
             }
             count_tmp++;
         }
         }
    end:
     
    free(line);
    fclose(fp);

}




int main(int argc, char *argv[]){
    int i;
    struct timespec sleep_time, start_command, end_command, start_total, end_total;
    char *a;
    char *b;

    double repeat;
    long sleep;
    
    sleep_time.tv_sec = 0;
    sleep_time.tv_nsec;


    int count = 0;
    int capacity = 154;
    char *buffer_new = malloc(capacity);
    FILE *fp;

    
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
        sleep_time.tv_sec = 0;
        sleep_time.tv_nsec = sleep;

    }else{  
        a = argv[4];
        b = argv[5];
        repeat = atoi(a);
        sleep = atol(b);
        sleep_time.tv_sec = 0;
        sleep_time.tv_nsec = sleep;
    }
        if( argc == 5){

            if ((strstr(argv[2],"cpu_log.txt")) != NULL){

                if(clock_gettime(CLOCK_MONOTONIC, &start_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
                
                if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
    
                for(i = 0; i < repeat; i++){
                //while(1){

                    if (count + 31 >= capacity){
                        capacity += capacity;
                        buffer_new = realloc(buffer_new, capacity * sizeof buffer_new[0]);
                        if ( buffer_new == NULL){
                            printf("Memory allocation failed\n");
                            exit(-1);
                            }
                    }
                    read_metrics(argv[1], buffer_new, &count, 0, "cpu");
                    //read_cpu(argv[1], buffer_new, &count);
                    //printf("After read_cpu: capacity %d ,  count %d \n", capacity, count);                    
                    if(nanosleep(&sleep_time, NULL) < 0){
                        perror("CPU nanosleep:");
                        exit(-1);
                    }
                }
    
                if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                if(clock_gettime(CLOCK_MONOTONIC, &end_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                printf("Total CPU time of CPU: %lld\n",diff_time(start_command, end_command));
                printf("CPU time of per gathering CPU stats command: %f\n", diff_time(start_command, end_command) / repeat);
                printf("Total elapsed time of CPU: %lld\n",diff_time(start_total, end_total));


                fp = fopen(argv[2],"a");
                
                if (fp == NULL){
                    printf("open file error\n");
                    exit(-1); 
                    }
                    if (fwrite(buffer_new, 1, count, fp) < 0 ){
                        perror("fwrite");
                        exit(-1);
                        }

                fclose(fp);
                free(buffer_new);
            }

            else if((strstr(argv[2],"block_log.txt")) != NULL){

                 if(clock_gettime(CLOCK_MONOTONIC, &start_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                 if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }   
        for(i = 0; i < repeat; i++){
        //while(1){
            if (count + 54 >= capacity){
                        capacity += capacity;
                        buffer_new = realloc(buffer_new, capacity * sizeof buffer_new[0]);
                        //printf("?\n");
                    if ( buffer_new == NULL){
                        printf("Memory allocation failed\n");
                        exit(-1);
                    }
                    }
            read_metrics(argv[1], buffer_new, &count, 1, "block");
            //printf("block count :%d\n", count);   
            //read_block(argv[1], buffer_new, &count);
                if(nanosleep(&sleep_time, NULL) < 0){
                        perror("BLOCK nanosleep:");
                        exit(-1);
                }
                }
                 if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                 }

                 if(clock_gettime(CLOCK_MONOTONIC, &end_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

        printf("Total CPU time of BLOCK: %lld\n",diff_time(start_command, end_command));
        printf("CPU time of per gathering Block stats command: %f\n", diff_time(start_command, end_command) / repeat);
        printf("Total elapsed time of BLOCK: %lld\n",diff_time(start_total, end_total));

            fp = fopen(argv[2],"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if(fwrite(buffer_new, 1, count, fp) < 0){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    free(buffer_new);

            }
            else{
                printf("typo\n");
                return -1;
            }
        }else if (argc == 6){
            if (strstr(argv[3],"memory_log.txt" )!= NULL){

                if(clock_gettime(CLOCK_MONOTONIC, &start_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

             if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
        for(i = 0; i < repeat; i++){
        //while(1){

                    if (count + 30 >= capacity){
                        capacity += capacity;
                        buffer_new = realloc(buffer_new, capacity * sizeof buffer_new[0]);
                        //printf("?\n");
                    if ( buffer_new == NULL){
                        printf("Memory allocation failed\n");
                        exit(-1);
                    }
                    }
            read_metrics(argv[2], buffer_new, &count, 0, "memory");
            //read_memory(argv[2], buffer_new, &count);
                if(nanosleep(&sleep_time, NULL) < 0){
                        perror("MEMORY nanosleep:");
                        exit(-1);
                        }
                }

                 if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                if(clock_gettime(CLOCK_MONOTONIC, &end_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
                printf("Total CPU time of MEMORY: %lld\n",diff_time(start_command, end_command));
                printf("CPU time of per gathering memory stats command: %f\n", diff_time(start_command, end_command) / repeat);
                printf("Total elapsed time of MEMORY: %lld\n",diff_time(start_total, end_total));

                 fp = fopen(argv[3],"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if (fwrite(buffer_new, 1, count, fp) < 0 ){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    free(buffer_new);
        }
        else if (strstr(argv[2],"network_log.txt") != NULL){
            int target_index = atoi(argv[3]);
                
                if(clock_gettime(CLOCK_MONOTONIC, &start_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }
                 if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                for(i = 0; i < repeat; i++){
                //while(1){
                     if (count + 143 >= capacity){
                        capacity += capacity;
                        buffer_new = realloc(buffer_new, capacity * sizeof buffer_new[0]);
                        //printf("?\n");
                    if ( buffer_new == NULL){
                        printf("Memory allocation failed\n");
                        exit(-1);
                    }
                    }
              read_metrics(argv[1], buffer_new, &count, target_index-1, "network");
              //printf("network count :%d\n", count);      
            //read_network(argv[1], buffer_new, &count, target_index-1);  
                if(nanosleep(&sleep_time, NULL) < 0){
                        perror("NETWORK nanosleep:");
                        exit(-1);
                        }
                }
                 if(clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_command) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                if(clock_gettime(CLOCK_MONOTONIC, &end_total) < 0){
                    perror("clock_gettime");
                    exit(-1);
                }

                printf("Total CPU time of NETWORK: %lld\n",diff_time(start_command, end_command));
                printf("CPU time of per gathering network stats command: %f\n", diff_time(start_command, end_command) / repeat);
                printf("Total elapsed time of NETWORK: %lld\n",diff_time(start_total, end_total));
                fp = fopen(argv[2],"a");
    if (fp == NULL){
        printf("open file error\n");
        exit(-1);
    }
    if (fwrite(buffer_new, 1, count, fp) < 0){
        perror("fwrite");
        exit(-1);
    }
    fclose(fp);
    free(buffer_new);

    }
        }

}