#include <stdio.h>
#include <string.h>

typedef const char *string;

// utility: to reverse a string in place
void revstr(char *str, size_t n) {
  for (size_t i = 0; i < n / 2; ++i) {
    char tmp = str[i];
    str[i] = str[n - 1 - i];
    str[n - 1 - i] = tmp;
  }
}

// utility: to compare binary strings without converting to integers
int BinCmp(string a, string b) {
  while (*a == '0')
    ++a;
  while (*b == '0')
    ++b;

  int l1 = strlen(a), l2 = strlen(b);
  if (l1 != l2)
    return l1 - l2;
  return strcmp(a, b);
}

void BinAdd(string b1, string b2, char *result) {
  int i = strlen(b1) - 1;
  int j = strlen(b2) - 1;
  int k = 0, carry = 0;

  while (i >= 0 || j >= 0 || carry) {
    int d1 = (i >= 0) ? (b1[i--] - '0') : 0;
    int d2 = (j >= 0) ? (b2[j--] - '0') : 0;

    int sum = d1 + d2 + carry;
    result[k++] = (sum % 2) + '0';
    carry = sum / 2;
  }
  result[k] = '\0';
  revstr(result, k);
}

void BinSub(string b1, string b2, char *result) {
  int i = strlen(b1) - 1;
  int j = strlen(b2) - 1;
  int k = 0, borrow = 0;

  while (i >= 0 || j >= 0) {
    int d1 = (i >= 0) ? (b1[i--] - '0') : 0;
    int d2 = (j >= 0) ? (b2[j--] - '0') : 0;

    d1 -= borrow;
    if (d1 < d2) {
      d1 += 2;
      borrow = 1;
    } else {
      borrow = 0;
    }
    result[k++] = (d1 - d2) + '0';
  }

  // remove leading 0s
  while (k - 1 > 0 && result[k - 1] == '0')
    --k;
  result[k] = '\0';

  revstr(result, k);
}

void BinMul(string b1, string b2, char *result) {
  char temp[100] = "0";
  int n = strlen(b1);
  int shift = 0;

  for (int i = strlen(b2) - 1; i >= 0; --i) {
    if (b2[i] == '1') {
      char shifted[100];
      strcpy(shifted, b1);
      for (int s = 0; s < shift; ++s)
        shifted[n + s] = '0';
      shifted[n + shift] = '\0';

      BinAdd(temp, shifted, result);
      strcpy(temp, result);
    }
    ++shift;
  }
}

void BinDivMod(string dividend, string divisor, char *quotient,
               char *remainder) {
  char current[100];
  current[0] = '\0';
  quotient[0] = '\0';

  for (int i = 0; i < strlen(dividend); ++i) {
    int clen = strlen(current);
    current[clen] = dividend[i];
    current[clen + 1] = '\0';

    if (BinCmp(current, divisor) >= 0) {
      BinSub(current, divisor, remainder);
      strcpy(current, remainder);
      strcat(quotient, "1");
    } else {
      strcat(quotient, "0");
    }
  }

  // update remainder
  int s = 0;
  while (current[s] == '0')
    ++s;
  strcpy(remainder, current + s);

  // remove leading 0s
  s = 0;
  while (quotient[s] == '0' && quotient[s + 1] != '\0')
    ++s;
  memmove(quotient, quotient + s, strlen(quotient + s) + 1);
}

int main(void) {
  char result[100], rem[100];

  BinAdd("110111", "101101", result); // 55 + 45
  printf("%s\n", result);             // 100

  BinSub("110111", "101101", result); // 55 - 45
  printf("%s\n", result);             // 10

  BinMul("1111", "1010", result); // 15 x 10
  printf("%s\n", result);         // 150

  BinDivMod("1110011", "111", result, rem); // 115 / 7
  printf("%s and %s\n", result, rem);       // 16 and 3

  return 0;
}
