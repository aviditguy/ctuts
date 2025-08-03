#include <stdio.h>
#include <math.h>

void power_of_two_binary(int n, char *buffer) {
  buffer[0] = '1';
  for (int i = 1; i <= n; ++i)
    buffer[i] = '0';
  buffer[n + 1] = '\0';
}

void power_of_two_hex(int n, char *buffer) {
  int k = 0;
  buffer[k] = pow(2, (n % 4)) + '0';
  for (k = 1; k <= n / 4; ++k)
    buffer[k] = '0';
  buffer[k] = '\0';
}

int main(void) {
  char bin[100], hex[100];

  int n = 13; // x = 2^13 = 8192

  power_of_two_binary(n, bin);
  power_of_two_hex(n, hex);

  printf("2^%d in bin: %s\n", n, bin);
  printf("2^%d in hex: %s\n", n, hex);

  return 0;
}
