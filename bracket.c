#include <stdio.h>
#include <string.h>

// 0 false, 1 true
int isValid(const char *str){
   char arr[strlen(str)/2];
   int top = -1;

   for (size_t i=0; str[i]; ++i){
      switch(str[i]){
         case '(': case '{': case '[':
            arr[++top] = str[i]; break;
         case ')': if (top < 0 || arr[top--] != '(') return 0; break;
         case '}': if (top < 0 || arr[top--] != '{') return 0; break;
         case ']': if (top < 0 || arr[top--] != '[') return 0; break;
      }
   }
   return top == -1;
}

int main(void){
   const char *str1 = "({[]})";     // valid
   const char *str2 = "({[})";      // invalid
   const char *str3 = "({[]}()";    // invalid
   const char *str4 = "((()))";     // valid
   const char *str5 = "({[)]}";     // invalid

   printf("%d\n", isValid(str1)); 
   printf("%d\n", isValid(str2)); 
   printf("%d\n", isValid(str3)); 
   printf("%d\n", isValid(str4)); 
   printf("%d\n", isValid(str5)); 

   return 0;
}
