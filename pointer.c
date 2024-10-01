#include <stdio.h>

int main(void){
   int a = 10;
   int * iptr = &a;

   printf("value of a = %d\n", a);
   printf("addr of a = %p\n", (void*)&a);

   printf("value of ptr = %p\n", (void*)iptr);
   printf("value pointed by ptr = %d\n", *iptr);
   printf("addr of ptr = %p\n", (void*)&iptr);

   /* ptr1 is pointer to an int */
   int * ptr1 = &(int){10};
   *ptr1 = 20;          // ok
   ptr1  = NULL;        // ok

   /* ptr2 is const pointer to an int */
   int * const ptr2 = &(int){10};
   *ptr2 = 20;          // ok
   // ptr2  = NULL;     // error

   /* ptr3 is pointer to const int */
   const int * ptr3 = &(int){10};
   // *ptr3 = 20;       // error
   ptr3  = NULL;        // ok

   /* ptr4 is const pointer to const int */
   const int * const ptr4 = &(int){10};
   // *ptr4 = 20;       // error
   // ptr4  = NULL;     // error

   return 0;
}
