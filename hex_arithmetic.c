#include <stdio.h>
#include <string.h>

typedef const char *string;

// utility: reverse a string in place
void revstr(char *str, size_t n) {
  for (size_t i = 0; i < n / 2; ++i) {
    char tmp = str[i];
    str[i] = str[n - 1 - i];
    str[n - 1 - i] = tmp;
  }
}

// utility: convert hex to int
int hexToInt(char c) {
  if (c >= '0' && c <= '9')
    return c - '0';
  return 10 + (c - 'A');
}

// utility: convert int to hex
char intToHex(int c) {
  if (c >= 0 && c <= 9)
    return c + '0';
  return 'A' + (c - 10);
}

// Utility: function to compare hex strings without converting to Integer
int HexCmp(string a, string b) {
  while (*a == '0')
    ++a; // strip leading 0s
  while (*b == '0')
    ++b;

  int l1 = strlen(a), l2 = strlen(b);
  if (l1 != l2)
    return l1 - l2;
  return strcmp(a, b);
}

void HexAdd(string h1, string h2, char *result) {
  int i = strlen(h1) - 1;
  int j = strlen(h2) - 1;
  int k = 0, carry = 0;

  while (i >= 0 || j >= 0 || carry) {
    int d1 = (i >= 0) ? hexToInt(h1[i--]) : 0;
    int d2 = (j >= 0) ? hexToInt(h2[j--]) : 0;

    int sum = d1 + d2 + carry;
    result[k++] = intToHex(sum % 16);
    carry = sum / 16;
  }
  result[k] = '\0';
  revstr(result, k);
}

void HexSub(string h1, string h2, char *result) {
  int i = strlen(h1) - 1;
  int j = strlen(h2) - 1;
  int k = 0, borrow = 0;

  while (i >= 0 || j >= 0) {
    int d1 = (i >= 0) ? hexToInt(h1[i--]) : 0;
    int d2 = (j >= 0) ? hexToInt(h2[j--]) : 0;

    d1 -= borrow;
    if (d1 < d2) {
      d1 += 16;
      borrow = 1;
    } else {
      borrow = 0;
    }
    result[k++] = intToHex(d1 - d2);
  }

  // remove leading 0s
  while (k - 1 > 0 && result[k - 1] == '0')
    --k;
  result[k] = '\0';

  revstr(result, k);
}

void HexMul(string h1, string h2, char *result) {
  int i = strlen(h2) - 1;
  char temp[100] = "0";
  int shift = 0;

  while (i >= 0) {
    char shifted[100];
    int k = 99;
    shifted[k--] = '\0';
    for (int s = 0; s < shift; ++s)
      shifted[k--] = '0';

    int d1 = hexToInt(h2[i--]);
    int carry = 0;

    for (int j = strlen(h1) - 1; j >= 0; --j) {
      int d2 = hexToInt(h1[j]);
      int product = carry + (d1 * d2);
      shifted[k--] = intToHex(product % 16);
      carry = product / 16;
    }
    if (carry > 0)
      shifted[k--] = intToHex(carry);

    HexAdd(temp, shifted + k + 1, result);
    strcpy(temp, result);
    ++shift;
  }
}

void HexDivMod(string dividend, string divisor, char *quotient,
               char *remainder) {
  char current[100], mulres[100];
  current[0] = '\0';
  quotient[0] = '\0';

  for (int i = 0; i < strlen(dividend); ++i) {
    int clen = strlen(current);
    current[clen] = dividend[i];
    current[clen + 1] = '\0';

    char digit[2] = "0";
    for (int x = 15; x >= 0; --x) {
      digit[0] = intToHex(x);
      HexMul(divisor, digit, mulres);

      if (HexCmp(mulres, current) <= 0) {
        strcat(quotient, digit);
        HexSub(current, mulres, remainder);
        strcpy(current, remainder);
        break;
      }
    }
  }
  // update remainder
  strcpy(remainder, current);

  // remove leading 0s
  int s = 0;
  while (quotient[s] == '0' && quotient[s + 1] != '\0')
    ++s;
  memmove(quotient, quotient + s, strlen(quotient + s) + 1);
}

int main(void) {
  char result[100], rem[100];

  HexAdd("2D5", "64", result); // 725 + 100
  printf("%s\n", result);      // 825

  HexSub("2D5", "64", result); // 725 - 100
  printf("%s\n", result);      // 625

  HexMul("2D5", "64", result); // 725 x 100
  printf("%s\n", result);      // 72500

  HexDivMod("2D5", "64", result, rem); // 725 / 100
  printf("%s and %s\n", result, rem);  // 7 and 25

  return 0;
}
