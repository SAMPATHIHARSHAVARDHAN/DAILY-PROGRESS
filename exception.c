#include <stdio.h>
#include <setjmp.h>

jmp_buf env;

void divide(int a, int b) {
    if (b == 0) {
        longjmp(env, 1);
    }
    printf("Result = %d\n", a / b);
}

int main() {
    if (setjmp(env) == 0) {
        divide(10, 0);
    } else {
        printf("Exception: Division by zero\n");
    }
    return 0;
}

