#include <stdio.h>
#include <stdlib.h>

int main(void){
/******************************************************************************/
/******************************************************************************/
   /* int arr[3][3], row size is optional */
   int arr[][3] = { {1,2,3}, {4,5,6}, {7,8,9} };

   /* arr is pointer to pointer to an int */
   /* each row of arr - arr[0], arr[1], arr[2] is pointer to 1st elem of list */
   /* arr points to arr[0] which points to arr[0][0] */
   printf("%p == %p == %p\n",
         (void*)arr, (void*)&arr[0], (void*)&arr[0][0]);

   /* accessing 6th element i.e. 6 */
   printf("%d == %d == %d\n",
         arr[1][2], *(arr[1]+2), *(*(arr+1)+2));

   /* arr[0], arr[1], arr[2] are pointer to first elem of respective rows */
   printf("%d == %d == %d\n", *arr[0], *arr[1], *arr[2]);
   printf("%d == %d == %d\n", **arr, *(*(arr+1)), *(*(arr+2)));

/******************************************************************************/
/******************************************************************************/
   /* ptr1 is pointer to an array of 3 int */
   /* so ptr1 points to an arr which points to arr[0] */
   int (*ptr1)[3] = arr;

   /* here ptr1 points to row 1 i.e. arr[1] of arr */
   ptr1 = &arr[1];

   /* accessing elements of array pointed by ptr1 */
   printf("%d - %d - %d\n", (*ptr1)[0], (*ptr1)[1], (*ptr1)[2]);  // 4 - 5 - 6
   printf("%d - %d - %d\n", **ptr1, *(*ptr1+1), *(*ptr1+2));      // 4 - 5 - 6

   /* now what differs, int * ptr = arr[0]; to int (*ptr)[3] = arr; */
   /* they both points to first element of arr[0] i.e. arr[0][0] */
   /* difference lies in how C view them as types - */
   /* - one is ptr is pointer to an int */
   /* - other ptr is pointer to an array of int of size 3 */
   /* the other difference is pointer arithmetic */
   /* - int * ptr : *ptr == arr[0][0], *(ptr+1) == arr[0][1] and so on */
   /* - int (*ptr)[3] : **ptr == arr[0][0], *(*(ptr+1)) == arr[1][0] ... */
   printf("%d - %d\n", *ptr1[0], *ptr1[1]);     // 4 - 7
   printf("%d - %d\n", **ptr1, *(*(ptr1+1)));   // 4 - 7

/******************************************************************************/
/******************************************************************************/
   /* arr2 is an array of pointer to int */
   /* always initialize with initializer list */
   /* int * arr[] = { &(int){10}, &(int){20}, &(int){30} }; */
   int * arr2[] = {arr[0], arr[1], arr[2]};
   
   /* accesing 2 elements 2 element i.e. 5 */
   printf("%d == %d == %d\n", 
         arr2[1][1], *(arr2[1]+1), *(*(arr2+1)+1));

/******************************************************************************/
/******************************************************************************/
   /* dynamically allocated array */
   int ** darr = (int **) malloc(sizeof(int *) * 5);
   for (size_t i=0; i<5; ++i)
      darr[i] = (int *) malloc(sizeof(int) * 5);

   /* free allocated memory */
   for (size_t i=0; i<5; ++i) free(darr[i]);
   free(darr);

   return 0;
}
