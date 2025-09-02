// Mastery Challenge: Navigate Maze
/*
Create a label:
start:

Jump to a label using goto:
goto start;

Example using goto to create a loop:

int i = 0;
start:
if (i < 5)
{
    Console.WriteLine(i);
    i++;
    goto start;
}
*/

/*
Create a method named NavigateMaze that simulates a simple maze navigation using goto statements:

The method should:

Take an integer parameter startPosition (1, 2, or 3)
Navigate through a maze based on the starting position
Print progress messages at each step
Return to the "entrance" label if the user hits a dead end
Print "Maze completed!" when reaching the exit
Implementation details:

If starting at position 1: go to "pathA" label
If starting at position 2: go to "pathB" label
If starting at position 3: go to "pathC" label
pathA should print "Taking left path" and go to the "junction" label
pathB should print "Taking middle path" and go to the "deadEnd" label
pathC should print "Taking right path" and go to the "exit" label
The "deadEnd" label should print "Hit a wall! Going back to entrance" and go to the "entrance" label
The "junction" label should print "Reached a junction" and go to the "exit" label
The "exit" label should print "Maze completed!"
*/




using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class Flow3
{
    public static void navigateMaze(int startPosition)
    {
    // Write your code here
    entrance:
        if (startPosition == 1)
        {
            goto pathA;
        }
        else if (startPosition == 2)
        {
            goto pathB;
        }
        else if (startPosition == 3)
        {
            goto pathC;
        }
        else
        {
            Console.WriteLine("Invalid starting position");
            return;
        }

    pathA:
        Console.WriteLine("Taking left path");
        goto junction;

    pathB:
        Console.WriteLine("Taking middle path");
        goto deadEnd;

    pathC:
        Console.WriteLine("Taking right path");
        goto exit;
    deadEnd:
        Console.WriteLine("Hit a wall! Going back to entrance");
        startPosition = int.Parse(Console.ReadLine() ?? "1");
        goto entrance;
    junction:
        Console.WriteLine("Reached a junction");
        goto exit;

    exit:
        Console.WriteLine("Maze completed!");
    }
}