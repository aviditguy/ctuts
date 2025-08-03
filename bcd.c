#include <stdio.h>

void decimal_to_bcd(const char *str, size_t n, char *buffer){
  int j = 0;
  for (int i=0; i<n; ++i){
    int d = str[i] - '0';
    for (int x=3; x>=0; --x)
      buffer[j++] = (d >> x & 1) + '0';
  }
  buffer[j] = '\0';
}

int bcd_to_decimal(const char *str, size_t n){
  int result = 0;
  for (int i=0; i<n; i+=4){
    int d = 0;
    for (int j=0; j<4; ++j)
      d = d * 2 + (str[i+j] - '0');
    result = result * 10 + d;
  }
  return result;
}

int main(void){
  char result[100];

  decimal_to_bcd("100", 3, result);
  printf("%s\n", result);

  int n = bcd_to_decimal("000100000000", 12);
  printf("%d\n", n);

  return 0;
}
