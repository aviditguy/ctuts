#include <stdio.h>
#include <stdlib.h>

int main(void){
   /* void pointer is a pointer that has no associated data type with it */
   /* void pointer can hold address of any type and can be typecasted to any */
   int a = 10;
   char c = 'a';

   void *ptr = &a;
   ptr = &c;

   /*  */

   int iarr[] = {1, 2, 3};
   char carr[] = {'d', 'e', 'f'};

   void * iter = iarr;
   for (size_t i=0; i<3; ++i)
      printf("%d ", ((int*)iter)[i]);
   printf("\n");

   iter = carr;
   for (size_t i=0; i<3; ++i)
      printf("%c ", *((char*)iter + i * sizeof(char)));
   printf("\n");

   return 0;
}
