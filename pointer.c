#include <stdio.h>

int main(void){
   /* ptr1 is pointer to an int */
   int * ptr1 = &(int){10};
   *ptr1 = 20;       // ok
   ptr1  = NULL;     // ok

   /* ptr2 is const pointer to an int */
   int * const ptr2 = &(int){10};
   *ptr2 = 20;       // ok
   // ptr2 = NULL;   // ok

   /* ptr3 is pointer to const int */
   const int * ptr3 = &(int){10};
   // *ptr3 = 20;    // ok
   ptr3 = NULL;      // ok

   /* ptr4 is const pointer to const int */
   const int * const  ptr4 = &(int){10};
   // *ptr4 = 20;    // ok
   // ptr4  = NULL;  // ok

   return 0;
}
