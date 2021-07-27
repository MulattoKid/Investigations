#include <stdalign.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    char a;
} example_1;

typedef struct
{
    uint16_t a;
} example_2;

typedef struct
{
    uint32_t a;
} example_3;

typedef struct
{
    uint64_t a;
} example_4;

typedef struct
{
    char a;
    uint64_t b;
} example_5;

typedef struct
{
    uint64_t a;
    char b;
} example_6;

typedef struct
{
    char a;
    uint64_t b;
    char c;
} example_7;

typedef struct
{
    uint64_t a;
    char b;
    char c;
} example_8;

typedef struct
{
    example_8 a;
    example_1 b;
    example_8 c;
} example_9;

typedef struct __attribute__((packed))
{
    char a;
    uint32_t b;
} example_12;

typedef struct
{
    char a;
    uint32_t b __attribute__((packed));
    char c;
} example_13;

typedef struct
{
    char a;
    uint32_t b __attribute__((packed, aligned(2)));
    char c;
} example_14;

int main(int argc, char** argv)
{
    // Platform
    {
        printf("Platform:\n");

        // Operating System - https://sourceforge.net/p/predef/wiki/OperatingSystems/
#if __APPLE__
        printf("\tApple ");
#elif _WIN32
        printf("\tWindows ");
#elif __linux__
        printf("\tLinux ");
#else
        printf("Operating System not supported\n");
        exit(EXIT_FAILURE);
#endif

        // CPU Architecture - https://sourceforge.net/p/predef/wiki/Architectures/
#if __arm__
        printf("arm32\n");
#elif __aarch64__
        printf("arm64\n");
#elif __i386__
        printf("x86\n");
#elif __x86_64__
        printf("x64\n");
#else
        printf("CPU Architecture not supported\n");
        exit(EXIT_FAILURE);
#endif

        printf("\t_Alignof(void*): %zu\n", _Alignof(void*));
        printf("\t_Alignof(char): %zu\n", _Alignof(char));
        printf("\t_Alignof(uint16_t): %zu\n", _Alignof(uint16_t));
        printf("\t_Alignof(uint32_t): %zu\n", _Alignof(uint32_t));
        printf("\t_Alignof(uint64_t): %zu\n", _Alignof(uint64_t));
        printf("\t_Alignof(float): %zu\n", _Alignof(float));
        printf("\t_Alignof(double): %zu\n", _Alignof(double));
    }

    ////////// Example 1 //////////
    /**
     * This is the most basic example: a single-byte struct.
     *  - The struct's alignment matches that of member 'a'
     *  - The struct's size matches that of member 'a'
     *  - Member 'a' starts at an offset of 0 bytes
    */
   {
        printf("example_1:\n");
        printf("\t_Alignof(example_1):    %zu\n", _Alignof(example_1));
        printf("\tsizeof(example_1):      %zu\n", sizeof(example_1));
        printf("\toffsetof(example_1, a): %zu\n", offsetof(example_1, a));
   }

    ////////// Example 2 //////////
    /**
     * This is similar to 'Example 1', only that member 'a' has increased in 
     * size from 1 byte to 2 bytes.
     *  - The struct's alignment matches that of member 'a'
     *  - The struct's size matches that of member 'a'
     *  - Member 'a' starts at an offset of 0 bytes
    */
    {
        printf("example_2:\n");
        printf("\t_Alignof(example_2):    %zu\n", _Alignof(example_2));
        printf("\tsizeof(example_2):      %zu\n", sizeof(example_2));
        printf("\toffsetof(example_2, a): %zu\n", offsetof(example_2, a));
    }

    ////////// Example 3 //////////
    /**
     * This is similar to 'Example 2', only that member 'a' has increased in 
     * size from 2 bytes to 4 bytes.
     *  - The struct's alignment matches that of member 'a'
     *  - The struct's size matches that of member 'a'
     *  - Member 'a' starts at an offset of 0 bytes
    */
   {
        printf("example_3:\n");
        printf("\t_Alignof(example_3):    %zu\n", _Alignof(example_3));
        printf("\tsizeof(example_3):      %zu\n", sizeof(example_3));
        printf("\toffsetof(example_3, a): %zu\n", offsetof(example_3, a));
   }

    ////////// Example 4 //////////
    /**
     * This is similar to 'Example 3', only that member 'a' has increased in 
     * size from 8 byte to 8 bytes.
     *  - The struct's alignment matches that of member 'a'
     *  - The struct's size matches that of member 'a'
     *  - Member 'a' starts at an offset of 0 bytes
    */
    {
        printf("example_4:\n");
        printf("\t_Alignof(example_4):    %zu\n", _Alignof(example_4));
        printf("\tsizeof(example_4):      %zu\n", sizeof(example_4));
        printf("\toffsetof(example_4, a): %zu\n", offsetof(example_4, a));
    }

    ////////// Example 5 //////////
    /**
     * This example is slightly more complicated in that the struct now has
     * two members instead of just one.
     *  - The struct's alignment equals the largest basic type in the struct
     *  - The struct's size is a multiple of the struct's alignment
     *  - Member 'a' starts at an offset of 0 bytes
     *  - Member 'b' starts at an offset of 8 bytes, even though member 'a' only
     *    requires 1 byte of storage. This is because member 'b' has a larger
     *    alginment requirement which must be satisfied.
     *    - Note how this essentially wastes 7 bytes between member 'a' and 'b'
    */
    {
        printf("example_5:\n");
        printf("\t_Alignof(example_5):    %zu\n", _Alignof(example_5));
        printf("\tsizeof(example_5):      %zu\n", sizeof(example_5));
        printf("\toffsetof(example_5, a): %zu\n", offsetof(example_5, a));
        printf("\toffsetof(example_5, b): %zu\n", offsetof(example_5, b));
    }

    ////////// Example 6 //////////
    /**
     * This is similar to example 5, only that the sizes of members 'a' and 'b'
     * are swapped. However, this doesn't affect the size of the struct.
     *  - The struct's alignment equals the largest basic type in the struct
     *  - The struct's size is a multiple of the struct's alignment
     *  - Member 'a' starts at an offset of 0 bytes
     *  - Member 'b' starts at an offset of 8 bytes
     *    - Note how this essentially wastes 7 bytes and the end of the struct
    */
    {
        printf("example_6:\n");
        printf("\t_Alignof(example_6):    %zu\n", _Alignof(example_6));
        printf("\tsizeof(example_6):      %zu\n", sizeof(example_6));
        printf("\toffsetof(example_6, a): %zu\n", offsetof(example_6, a));
        printf("\toffsetof(example_6, b): %zu\n", offsetof(example_6, b));
    }

    ////////// Example 7 //////////
    /**
     * This is a variation of example 5 where another 1-byte basic type is
     * added to the end of the struct.
     *  - The struct's alignment equals the largest basic type in the struct
     *  - The struct's size is a multiple of the struct's alignment
     *  - Member 'a' starts at an offset of 0 bytes
     *    - Note how this essentially wastes 7 bytes between 'a' and 'b'
     *  - Member 'b' starts at an offset of 8 bytes
     *  - Member 'c' starts at an offset of 16 bytes
     *    - Note how this essentially wastes 7 bytes between 'b' and 'c'
     * 
     * Note how the struct's members aren't reorganized to be packed better.
     * By organinzing the members this way in our code 14 of 24 bytes are wasted.
    */
    {
        printf("example_7:\n");
        printf("\t_Alignof(example_7):    %zu\n", _Alignof(example_7));
        printf("\tsizeof(example_7):      %zu\n", sizeof(example_7));
        printf("\toffsetof(example_7, a): %zu\n", offsetof(example_7, a));
        printf("\toffsetof(example_7, b): %zu\n", offsetof(example_7, b));
        printf("\toffsetof(example_7, c): %zu\n", offsetof(example_7, c));
    }

    ////////// Example 8 //////////
    /**
     * This is a manually reorganized version of example 7, where the two
     * 1-byte basic types follow each other. This results in them occupying
     * 2 of the 8 bytes needed due to the alignment of the struct.
     *  - The struct's alignment equals the largest basic type in the struct
     *  - The struct's size is a multiple of the struct's alignment
     *  - Member 'a' starts at an offset of 0 bytes
     *  - Member 'b' starts at an offset of 8 bytes
     *  - Member 'c' starts at an offset of 9 bytes
     *    - Note how members 'b' and 'c' reside in the same 8-byte memory area
    */
    {
        printf("example_8:\n");
        printf("\t_Alignof(example_8):    %zu\n", _Alignof(example_8));
        printf("\tsizeof(example_8):      %zu\n", sizeof(example_8));
        printf("\toffsetof(example_8, a): %zu\n", offsetof(example_8, a));
        printf("\toffsetof(example_8, b): %zu\n", offsetof(example_8, b));
        printf("\toffsetof(example_8, c): %zu\n", offsetof(example_8, c));
    }

    ////////// Example 9 //////////
    /**
     * This example shows that the concept just showcased only applies to basic
     * types. Any type, whether basic or struct, cannot occupy memory that isn't
     * assigned to it. Therefore, member 'b', although its alignment requirement
     * is 1, and it could theoretically occupy the byte following member 'a''s
     * last used byte (byte 9), it cannot since member 'a' reserves this memory.
     * It's therefore important to organize what I call 'root structures' in a
     * good way. If not done properly, this can lead to large wastage of memory.
     *  - The struct's alignment equals the largest basic type in the struct
     *  - The struct's size is a multiple of the struct's alignment
     *  - Member 'a' starts at an offset of 0 bytes
     *  - Member 'b' starts at an offset of 16 bytes
     *  - Member 'c' starts at an offset of 24 bytes
     *    - Note how this cannot start at an offset of 17 bytes, as it must follow
     *      the alignment requirements of its type
    */
    {
        printf("example_9:\n");
        printf("\t_Alignof(example_9):    %zu\n", _Alignof(example_9));
        printf("\tsizeof(example_9):      %zu\n", sizeof(example_9));
        printf("\toffsetof(example_9, a): %zu\n", offsetof(example_9, a));
        printf("\toffsetof(example_9, b): %zu\n", offsetof(example_9, b));
        printf("\toffsetof(example_9, c): %zu\n", offsetof(example_9, c));
    }

    ////////// Example 10 //////////
    /**
     * This example deliberately violates the C standard, specifically
     *  "A pointer to an object or incomplete type may be converted to
     *   a pointer to a different object or incomplete type. If the
     *   resulting pointer is not correctly aligned for the referenced
     *   type, the behavior is undefined." - The C99 Standard, 6.3.2.3 Paragraph 7
     * 
     * In addition, the example violates the C standard's strict aliasing
     * rule - The C99 Standard, 6.5
    */
    {
        // Allocate 1024 bytes - each byte is 1-byte aligned since _Alignof(char) = 1
        char* p0 = malloc(1024 * sizeof(char)); // (VALID)
        uint16_t* pa = (uint16_t*)p0;
        *pa = 1;
        printf("%u\n", *pa);
        // Go to the address of the next char in the allocated array
        char* p1 = p0 + 1; // (VALID)
        // Cast this pointer to an uint64_t pointer
        // (also breaks the strict aliasing rule - the C99 Standard, 6.5)
        uint64_t* p2 = (uint64_t*)p1; // (INVALID)
        printf("example_10:\n");
        printf("\t_Alignof(uint64_t):       %zu\n", _Alignof(uint64_t));
        printf("\tAddress of example_10_p2: %p\n", p2);
        printf("\t\t1-byte aligned:   %i\n", (uint64_t)p2 % 1 == 0);
        printf("\t\t2-byte aligned:   %i\n", (uint64_t)p2 % 2 == 0);
        printf("\t\t4-byte aligned:   %i\n", (uint64_t)p2 % 4 == 0);
        printf("\t\t8-byte aligned:   %i\n", (uint64_t)p2 % 8 == 0);
    }

    ////////// Example 11 //////////
    /**
     * This example goes the other way compared to example 10, which is allowed.
     * Casting from a pointer to an object of lower alignment requirements is fine,
     * as it's guaranteed to be aligned (we don't have non-power of two types).
     * 
     * Also, casting to a char* and accessing the value through it doesn't violate
     * the strict aliasing rule.
    */
    {
        // Allocate 1024 bytes - each 8 bytes is 8-byte aligned since _Alignof(char) = 8
        uint64_t* p0 = malloc(16 * sizeof(uint64_t)); // (VALID)
        // Go to the address of the next uint64_t in the allocated array
        uint64_t* p1 = p0 + 1; // (VALID)
        // Cast this pointer to an char pointer
        // (doesn't break the strict aliasing rule, as p1 is cast to a char*)
        char* p2 = (char*)p1; // (VALID)
        printf("example_11:\n");
        printf("\t_Alignof(uint64_t):       %zu\n", _Alignof(char));
        printf("\tAddress of example_11_p2: %p\n", p2);
        printf("\t\t1-byte aligned:   %i\n", (uint64_t)p2 % 1 == 0);
        printf("\t\t2-byte aligned:   %i\n", (uint64_t)p2 % 2 == 0);
        printf("\t\t4-byte aligned:   %i\n", (uint64_t)p2 % 4 == 0);
        printf("\t\t8-byte aligned:   %i\n", (uint64_t)p2 % 8 == 0);
    }

    ////////// Example 12 //////////
    /**
     * It is possible to force structs to be 'packed', meaning that padding isn't
     * inserted to uphold the different basic types' alignment requirements. This
     * is accomplished using the __attribute__((packed)) attribute for GCC.
     * 
     * It can also be useful when working with binary data with a given layout
     * (remember to take differences in endianess into account).
     * 
     * Note that packed structures do not generate unaligned accesses, when members
     * are accessed through the struct itself, as the compiler will insert
     * instructions that generate valid code. However, accessing a member directly
     * through its address does not guarantee this, and can cause an unaligned access.
     * 
     *  - The struct's alignment equals 1, as it's packed
     *  - The struct's size is the sum of the size of each member
     *  - Member 'a' starts at an offset of 0 bytes
     *  - Member 'b' starts at an offset of 1 bytes
    */
   {
        printf("example_12:\n");
        printf("\t_Alignof(example_12):    %zu\n", _Alignof(example_12));
        printf("\tsizeof(example_12):      %zu\n", sizeof(example_12));
        printf("\toffsetof(example_12, a): %zu\n", offsetof(example_12, a));
        printf("\toffsetof(example_12, b): %zu\n", offsetof(example_12, b));
   }

   ////////// Example 13 //////////
   /**
    * It's also possible to specify that only specific members should be packed.
    *  - The struct's alignment equals 1, as all its members have 1-byte alignment
    *  - The struct's size is the sum of the size of each member
    *  - Member 'a' starts at an offset of 0 bytes
    *  - Member 'b' starts at an offset of 1 bytes
    *  - Member 'c' starts at an offset of 5 bytes
   */
   {
        printf("example_13:\n");
        printf("\t_Alignof(example_13):    %zu\n", _Alignof(example_13));
        printf("\tsizeof(example_13):      %zu\n", sizeof(example_13));
        printf("\toffsetof(example_13, a): %zu\n", offsetof(example_13, a));
        printf("\toffsetof(example_13, b): %zu\n", offsetof(example_13, b));
        printf("\toffsetof(example_13, c): %zu\n", offsetof(example_13, c));
   }

   ////////// Example 14 //////////
   /**
    * It's also possible to specify a specific alignment for an entire struct,
    * or just for single members using the __attribute__((packed, aligned(X))),
    * where X is a value that's a power of two.
    *  - The struct's alignment equals 2, as that's the largest alignment requirement
    *    for any member in the struct
    *  - The struct's size is the sum of the size of each member with an additional byte
    *    added due to padding, and another byte added as the size must be a multiple of
    *    the alignment
    *  - Member 'a' starts at an offset of 0 bytes
    *  - Member 'b' starts at an offset of 2 bytes
    *  - Member 'c' starts at an offset of 6 bytes
   */
  {
        printf("example_14:\n");
        printf("\t_Alignof(example_14):    %zu\n", _Alignof(example_14));
        printf("\tsizeof(example_14):      %zu\n", sizeof(example_14));
        printf("\toffsetof(example_14, a): %zu\n", offsetof(example_14, a));
        printf("\toffsetof(example_14, b): %zu\n", offsetof(example_14, b));
        printf("\toffsetof(example_14, c): %zu\n", offsetof(example_14, c));
  }

    return EXIT_SUCCESS;
}