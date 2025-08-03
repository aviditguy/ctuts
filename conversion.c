#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { BINARY = 2, OCTAL = 8, DECIMAL = 10, HEX = 16 } Base;

const char *hex = "0123456789ABCDEF";

const char *hex_to_bin[] = {"0000", "0001", "0010", "0011", "0100", "0101",
                            "0110", "0111", "1000", "1001", "1010", "1011",
                            "1100", "1101", "1110", "1111"};

const char *oct_to_bin[] = {"000", "001", "010", "011",
                            "100", "101", "110", "111"};

int hexToInt(char c) {
  if (c >= '0' && c <= '9')
    return c - '0';
  return 10 + (c - 'A');
}

void trim_leading_zeros(char *str) {
  int k = strlen(str) - 1;
  while (k > 0 && str[k] == '0')
    --k;
  str[k + 1] = '\0';

  k = 0;
  while (str[k] == '0' && str[k + 1] != '\0')
    ++k;
  memmove(str, str + k, strlen(str + k) + 1);
}

void todecimal(const char *str, size_t len, char *buffer, size_t pidx,
               Base base) {
  double num = 0.0;
  for (int i = 0, p = pidx - 1; i < len; ++i) {
    if (str[i] == '.')
      continue;

    num += (hexToInt(str[i]) * pow(base, p));
    --p;
  }
  sprintf(buffer, "%.2lf", num);
}

void oct_hex_to_bin(const char *str, size_t len, char *buffer, Base base) {
  int k = 0;
  int pad = (base == OCTAL) ? 3 : 4;
  for (int i = 0; i < len; ++i) {
    if (str[i] == '.') {
      buffer[k++] = '.';
      continue;
    }
    if (base == OCTAL)
      strcpy(buffer + k, oct_to_bin[hexToInt(str[i])]);
    else
      strcpy(buffer + k, hex_to_bin[hexToInt(str[i])]);
    k += pad;
  }
  buffer[k] = '\0';
  trim_leading_zeros(buffer);
}

void Int(const char *str, char *buffer, size_t n, Base base) {
  double num = atof(str);
  int whole = (int)num;
  double frac = num - whole;

  int k = n - 1;
  buffer[k--] = '\0';
  do {
    buffer[k--] = hex[whole % base];
    whole /= base;
  } while (whole > 0);
  memmove(buffer, buffer + k + 1, strlen(buffer + k + 1) + 1);

  if (frac > 0.0) {
    k = strlen(buffer);
    buffer[k++] = '.';

    int places = 8;
    while (frac > 0.0 && places > 0) {
      frac *= base;
      buffer[k++] = hex[(int)frac];
      frac -= (int)frac;
      --places;
    }
    buffer[k] = '\0';
  }
  trim_leading_zeros(buffer);
}

void Binary(const char *str, char *buffer, size_t n, Base base) {
  int len = strlen(str);
  const char *point = strchr(str, '.');
  int idx = point ? (point - str) : len;

  if (base == DECIMAL) {
    todecimal(str, len, buffer, idx, BINARY);
    return;
  }

  // convert binary to octal and hexadecimal
  int group = (base == OCTAL) ? 3 : 4;
  int start, end, num, index;
  start = (group - 1) - (group - (idx % group)) % group;
  end = 0, num = 0, index = -1;

  while (end < len) {
    num = 0;
    if (str[end] == '.') {
      buffer[++index] = '.';
      ++end;
    } else {
      while (start >= 0 && end < len)
        num += (str[end++] - '0') * pow(2, start--);
      buffer[++index] = hex[num];
    }
    start = group - 1;
  }
  buffer[++index] = '\0';
  trim_leading_zeros(buffer);
}

void Octal(const char *str, char *buffer, size_t n, Base base) {
  int len = strlen(str);
  const char *point = strchr(str, '.');
  int idx = point ? (point - str) : len;

  if (base == DECIMAL) {
    todecimal(str, len, buffer, idx, OCTAL);
    return;
  }

  oct_hex_to_bin(str, len, buffer, OCTAL);
  if (base == HEX)
    Binary(buffer, buffer, n, HEX);
}

void Hex(const char *str, char *buffer, size_t n, Base base) {
  int len = strlen(str);
  const char *point = strchr(str, '.');
  int idx = point ? (point - str) : len;

  if (base == DECIMAL) {
    todecimal(str, len, buffer, idx, HEX);
    return;
  }

  oct_hex_to_bin(str, len, buffer, HEX);
  if (base == OCTAL)
    Binary(buffer, buffer, n, OCTAL);
}

int main(void) {
  char result[100];

  Int("100.36", result, 100, BINARY);
  printf("%s\n", result);

  Int("100.36", result, 100, OCTAL);
  printf("%s\n", result);

  Int("100.36", result, 100, HEX);
  printf("%s\n", result);

  Binary("1100100.01011100", result, 100, DECIMAL);
  printf("%s\n", result);

  Binary("1100100.01011100", result, 100, OCTAL);
  printf("%s\n", result);

  Binary("1100100.01011100", result, 100, HEX);
  printf("%s\n", result);

  Octal("144.27", result, 100, DECIMAL);
  printf("%s\n", result);

  Octal("144.27", result, 100, BINARY);
  printf("%s\n", result);

  Octal("144.27", result, 100, HEX);
  printf("%s\n", result);

  Hex("64.5C", result, 100, DECIMAL);
  printf("%s\n", result);

  Hex("64.5C", result, 100, BINARY);
  printf("%s\n", result);

  Hex("64.5C", result, 100, OCTAL);
  printf("%s\n", result);

  return 0;
}
