#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main() {
    long cc_num;
    do
    {
        cc_num = get_long("Credit Card Number: ");
    } while (cc_num <= 0);
    int num_digits = 0;
    int sum_even = 0;
    int sum_odd = 0;
    int last_digit = 0;
    int prev_last_digit = 0;
    int total;
    while (cc_num > 0)
    {
        num_digits++;
        prev_last_digit = last_digit;
        last_digit = cc_num % 10;
        if (num_digits % 2 == 0)
        {
            int product = 2 * last_digit;
            sum_even += (product % 10) + (product / 10);
        }
        else
        {
            sum_odd += last_digit;
        }
        cc_num /= 10;
    }
    total = sum_even + sum_odd;
    int digits = (last_digit * 10) + prev_last_digit;
    if ((total % 10) == 0)
    {
        if ((digits == 34 || digits == 37) && num_digits == 15)
        {
            printf("AMEX\n");
        }
        else if ((digits == 51 || digits == 52 || digits == 53 || digits == 54 || digits == 55) && num_digits == 16)
        {
            printf("MASTERCARD\n");
        }
        else if (last_digit == 4 && (num_digits == 13 || num_digits == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
