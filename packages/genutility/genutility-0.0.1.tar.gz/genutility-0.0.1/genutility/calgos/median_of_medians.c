#include <stdio.h>

// source: https://github.com/heineman/algorithms-nutshell-2ed/blob/17bd6e9cf9917727501f9eeadbfb2100f94eede0/Code/Sorting/PointerBased/selectKthWorstLinear.c#L46

/** The size of the grouping is determined elsewhere. */
int groupingSize = 5;

/** specialized insertion sort elements with spaced gap. */
void _insertion (int ar[], int(*cmp)(int, int),
                 int low, int right, int gap) {
  int loc;
  //printf("_insertion %d %d %d\n", low, right, gap);

  for (loc = low+gap; loc <= right; loc += gap) {
    int i = loc-gap;
    int value = ar[loc];
    while (i >= low && cmp(ar[i], value)> 0) {
      ar[i+gap] = ar[i];
      i -= gap;
    }
    ar[i+gap] = value;
  }
}


/**
 * Find suitable pivotIndex to use for ar[left,right] with closed bound
 * on both sides.
 *
 * 1. Divide the elements into floor(n/size) groups of size elements and
 *    use _insertion on each group
 * 2. Pick median from each sorted groups (size/2 element).
 * 3. Use select recursively to find median x of floor(n/size) medians
 *    found in step 2. This is known as the median-of-medians.
 */
int medianOfMedians (int ar[], int(*cmp)(int, int),
		     int left, int right, int gap) {
  int s, num;
  int span = groupingSize*gap;


  /* less than five? Insertion sort and return median.  */
  num = (right - left + 1) / span;
  //printf("median_of_medians %d %d %d %d %d\n", left, right, gap, span, num);
  if (num == 0) {
    _insertion (ar, cmp, left, right, gap);
    num = (right - left + 1)/gap;
    return left + gap*(num-1)/2;
  }

  /* set up all median values of groups of groupingSize elements */
  for (s = left; s+span < right; s += span) {
    _insertion (ar, cmp, s, s + span-1, gap);
  }

  /* Recursively apply to subarray [left, s-1] with increased gap
   * if more than 'groupingSize' groupings remain. */
  if (num < groupingSize) {
    /* find median of this reduced set. BASE CASE */
    _insertion (ar, cmp, left+span/2, right, span);
    return left + num*span/2;
  } else {
    return medianOfMedians (ar, cmp, left+span/2, s-1, span);
  }
}

int cmp(int a, int b)
{
    return a > b;
}

void eval(int list[], int len)
{
    int result = medianOfMedians(list, &cmp, 0, len-1, 1);
    printf("%d (%d), %d\n", result, len, list[result]);
}

int main(void)
{
    int list1[] = {0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4};
    eval(list1, 15);
    int list2[] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    eval(list2, 15);
    int list3[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
    eval(list3, 15);
    int list4[] = {4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0};
    eval(list4, 15);
    int list5[] = {1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 2};
    eval(list5, 15);
    int list6[] = {14, 94, 41, 69, 47, 96, 90, 46, 33, 21, 89, 60, 63, 0, 49};
    eval(list6, 15);
    int list7[] = {646, 624, 329, 47, 845, 221, 15, 92, 940, 831, 169, 190, 83, 599, 636, 496, 785, 701, 105, 807, 384, 605, 285, 219, 931, 185, 863, 68, 837, 165, 717, 608, 347, 713, 593, 191, 180, 405, 649, 744, 170, 490, 407, 659, 541, 342, 72, 6, 510, 101, 757, 203, 724, 792, 477, 361, 993, 836, 640, 74, 882, 31, 622, 18, 764, 698, 444, 62, 965, 692, 32, 956, 980, 621, 103, 45, 828, 70, 768, 161, 296, 200, 676, 44, 90, 753, 535, 274, 230, 871, 404, 741, 922, 78, 28, 908, 313, 184, 543, 536};
    eval(list7, 100);
}
