#include <stdio.h>
#include <string.h>

typedef const char *string;

// Utility: function to reverse a string in place
void revstr(char *str, size_t n) {
  for (size_t i = 0; i < n / 2; ++i) {
    char tmp = str[i];
    str[i] = str[n - 1 - i];
    str[n - 1 - i] = tmp;
  }
}

// Utility: function to compare binary strings without converting to Integer
int BinCmp(string a, string b) {
  while (*a == '0')
    ++a; // strip leading 0s
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
    int bit1 = (i >= 0) ? (b1[i--] - '0') : 0;
    int bit2 = (j >= 0) ? (b2[j--] - '0') : 0;

    int sum = bit1 + bit2 + carry;
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
    int bit1 = (i >= 0) ? (b1[i--] - '0') : 0;
    int bit2 = (j >= 0) ? (b2[j--] - '0') : 0;

    bit1 -= borrow;
    if (bit1 < bit2) {
      bit1 += 2;
      borrow = 1;
    } else {
      borrow = 0;
    }
    result[k++] = (bit1 - bit2) + '0';
  }

  // remove leading 0s
  while (k - 1 > 0 && result[k - 1] == '0')
    --k;

  result[k] = '\0';
  revstr(result, k);
}

void BinMul(string b1, string b2, char *result) {
  int n = strlen(b1);
  int i = strlen(b2) - 1;
  char temp[100] = "0";
  int shift = 0;

  while (i >= 0) {
    if (b2[i--] == '1') {
      char shifted[100];
      strcpy(shifted, b1);
      for (int s = 0; s < shift; ++s)
        shifted[n + s] = '0';
      shifted[n + shift] = '\0';

      BinAdd(temp, shifted, result);
      printf("%s\n", result);
      strcpy(temp, result);
    }
    ++shift;
  }
  strcpy(result, temp);
}

void BinDiv(string dividend, string divisor, char *quotient, char *remainder) {
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
  strcpy(remainder, current);

  // remove leading 0s from quotient
  int s = 0;
  while (quotient[s] == '0' && quotient[s + 1] != '\0')
    ++s;
  memmove(quotient, quotient + s, strlen(quotient + s) + 1);
}

int main(void) {
  char result[100], remainder[100];

  BinAdd("10110", "1111", result); // 22 + 15
  printf("%s\n", result);          // 37

  BinSub("10110", "1111", result); // 22 - 15
  printf("%s\n", result);          // 7

  BinMul("10110", "1111", result); // 22 * 15
  printf("%s\n", result);          // 330

  BinDiv("10110", "11", result, remainder); // 22 / 3
  printf("%s and %s\n", result, remainder); // 7  1

  BinDiv("10110", "1010", result, remainder); // 22 / 10
  printf("%s and %s\n", result, remainder);   // 2  2

  BinDiv("10110", "10110", result, remainder); // 22 / 22
  printf("%s and %s\n", result, remainder);    // 1  0

  return 0;
}
