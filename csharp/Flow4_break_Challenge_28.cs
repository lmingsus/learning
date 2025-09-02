// Mastery Challenge: Filter And Sum
/*

*/

/*

*/




using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class Flow4
{
    public static int filterAndSum(int[] numbers, int threshold)
    {
        // Write your code here
        int count = 0;
        foreach (int num in numbers)
        {
            if (num < 0)
            {
                continue;
            }
            if (num == threshold)
            {
                break;
            }
            else if (num < threshold)
            {
                Console.WriteLine(num);
                count++;
            }
        }
        return count;
    }

}