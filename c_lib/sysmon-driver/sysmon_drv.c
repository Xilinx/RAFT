#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <dirent.h>
#include <errno.h>
#include <ctype.h>
#include "XSysmon.h"

char file[60] = {};
int main(int argc, char **argv)
{
    float value;
    if(XSysmon_ReadValue(argv[1], &value) >= 0)
    {
        printf("float value %f\n", value);
    }
    else
    {
        printf("XSysmon_ReadValue failed\n");
    }
}
