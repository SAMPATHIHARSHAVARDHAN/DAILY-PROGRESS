#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

// Thread function
void* printNumbers(void* arg) {
    char* threadName = (char*)arg;

    for (int i = 1; i <= 5; i++) {
        printf("%s : %d\n", threadName, i);
        sleep(1);   // pause for 1 second
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;

    // Create threads
    pthread_create(&t1, NULL, printNumbers, "Thread 1");
    pthread_create(&t2, NULL, printNumbers, "Thread 2");

    // Wait for threads to finish
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}

