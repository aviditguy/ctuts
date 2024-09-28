#include <stdio.h>
#include <stdlib.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

int calc(int (*fptr)(int, int), int a, int b) { return fptr(a, b); }

int comp()

int main(void){
   printf("%d + %d = %d\n", 5, 7, calc(add, 5, 7));
   printf("%d - %d = %d\n", 5, 7, calc(sub, 5, 7));
   printf("%d * %d = %d\n", 5, 7, calc(mul, 5, 7));

   return 0;
}
