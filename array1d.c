#include <stdio.h>
#include <stdlib.h>

int main(void){
   /* int arr[5], size is optional */
   int arr[] = {1, 2, 3, 4, 5};

   /* arr is pointer pointing to first element */
   /* so, arr == &arr[0] */
   printf("%p == %p\n", (void*)arr, (void*)&arr[0]);

   /* accessing 2nd element of arr i.e. 2 */
   printf("%d == %d\n", arr[1], *(arr+1));

   /* const array is readonly */
   const int carr[] = {2, 4, 6, 8};
   // carr[1] = 10;     // error
   int * ptr = carr;    // allowed no compiler check
   ptr[0] = 10;

   /* dynamic allocated array, remember to free memory */
   int * darr = (int *) malloc(sizeof(int) * 5);
   free(darr);

   return 0;
}
