#include<stdio.h>
#include<cs50.h>

void draw(char type, int times)
{
    for (int i = 0; i < times; i++)
    {
        printf("%c", type);
    }
}
int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);
    int nhash = 1;
    for (int i = 0; i < height; i++)
    {
        draw(' ', height - 1 - i);
        draw('#', nhash + i);
        printf("\n");
    }
}
