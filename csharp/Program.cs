using System;
using System.Diagnostics;
public class Program
{
    public static bool Is_valid(string username, string password)
    {
        // Write your code below
        if (username == "user")
        {
            return (password == "qweasd");
        }
        else
        {
            return (username == "admin");
        }

    }

    public static void PrintNTimes(string message, int n)
    {
        // Write you code here
        for (int i = 0; i < n; i++)
        {
            Console.WriteLine(message);
        }
    }

    public static string[] ChangeElement(string[] arr, int index, string newElement)
    {
        // Write code here
        if (index >= 0 && index < arr.Length)
        {
            arr[index] = newElement;
        }
        return arr;
    }

    public static void Arr1()
    {
        // Create the shoppingList array here
        string[] shoppingList = { "bread", "eggs", "milk", "butter" };

        // Don't change the code below
        System.Console.WriteLine("Shopping List:");
        for (int i = 0; i < shoppingList.Length; i++)
        {
            System.Console.WriteLine(shoppingList[i]);
        }
    }

    public static void Values(int[] arr)
    {
        // Write code here
        for (int i = 0; i < arr.Length; i++)
        {
            Console.WriteLine(arr[i]);
        }
    }

    public static string[] Merge(string[] arr1, string[] arr2)
    {
        // Write code here
        string[] mergedArray = new string[arr1.Length + arr2.Length];
        Array.Copy(arr1, mergedArray, arr1.Length);
        Array.Copy(arr2, 0, mergedArray, arr1.Length, arr2.Length);
        Array.Sort(mergedArray);
        return mergedArray;
    }

    public static int Prod(int[] arr)
    {
        // Write your code below
        int product = 1;
        for (int i = 0; i < arr.Length; i++)
        {
            product *= arr[i];
        }
        return product;
    }

    public static int[] Reverse(int[] arr)
    {
        // Write your code below
        int[] reversedArray = new int[arr.Length];
        // for (int i = 0; i < arr.Length; i++)
        // {
        //     reversedArray[i] = arr[arr.Length - 1 - i];
        // }
        Array.Reverse(arr);
        return arr;
    }

    public static void AnalyzeString(string str)
    {
        // Write your code here
        // Length: [The length]
        // Substring: [The First substring]
        // Substring 2: [The Second substring]
        // Starts with 'Hello': [true or false]
        // Lowercase: [The string in lowercase]
        Console.WriteLine($"Length: {str.Length}");
        Console.WriteLine($"Substring: {str.Substring(7)}");
        Console.WriteLine($"Substring 2: {str.Substring(0, 5)}");
        Console.WriteLine($"Starts with 'Hello': {str.StartsWith("Hello")}");
        Console.WriteLine($"Lowercase: {str.ToLower()}");
    }

    public static string CreateFormattedString(string productName, int quantity, double unitPrice)
    {
        // Write your code here
        // Product: [productName], Quantity: [quantity], Unit Price: [unitPrice]
        return $"Product: {char.ToUpper(productName[0]) + productName[1..]}, Quantity: {quantity:F1}, Unit Price: {unitPrice:F2}";
    }

    public static double[] CalculateStats(int[] arr)
    {
        // Write your code here
        double[] calculate = new double[4];
        // sum, average, max, min
        for (int i = 0; i < arr.Length; i++)
        {
            calculate[0] += arr[i]; // Sum
        }
        calculate[1] = arr.Length > 0 ? calculate[0] / arr.Length : 0; // Average
        Array.Sort(arr);
        calculate[2] = arr.Length > 0 ? arr[arr.Length - 1] : 0; // Max
        calculate[3] = arr.Length > 0 ? arr[0] : 0; // Min
        return calculate;
    }

    public static int getElement(int[][] array, int row, int col)
    {
        // Write your code here
        if (row >= 0 && row < array.Length && col >= 0 && col < array[row].Length)
        {
            return array[row][col];
        }
        return -1;
    }

    public static int[][]? MultiplyMatrices(int[][] matrix1, int[][] matrix2)
    {
        // Write your code here
        if (matrix1[0].Length != matrix2.Length
            || matrix1.Length == 0
            || matrix2.Length == 0
            || matrix2[0].Length == 0
            || matrix1[0].Length == 0
            )
        {
            return null;
        }

        int row = matrix1.Length;
        int col = matrix2[0].Length;
        int[][] result = new int[row][];
        for (int i = 0; i < row; i++)
        {
            result[i] = new int[col];
            for (int j = 0; j < col; j++)
            {
                for (int s = 0; s < matrix1[0].Length; s++)
                {
                    result[i][j] += matrix1[i][s] * matrix2[s][j];
                }
            }
        }
        return result;
    }
    public static int findDiagonalDifference(int[][] matrix)
    {
        // Write your code here
        if (matrix.Length != matrix[0].Length)
        {
            return -1;
        }

        int primaryDiagonal = 0;
        int secondaryDiagonal = 0;

        for (int i = 0; i < matrix.Length; i++)
        {
            primaryDiagonal += matrix[i][i];
            secondaryDiagonal += matrix[i][matrix.Length - 1 - i];
        }

        return Math.Abs(primaryDiagonal - secondaryDiagonal);
    }
    public static bool ValidateUserAccess(bool isAuthenticated, bool hasAdminRole,
                                         bool hasValidToken, bool isInOfficeNetwork,
                                         bool isWorkingHours)
    {
        // Write your code here
        if (isAuthenticated && hasAdminRole ||
            isAuthenticated && !hasAdminRole && hasValidToken
            && (isInOfficeNetwork || isWorkingHours))
        {
            Console.WriteLine("Access granted");
            return true;
        }
        else
        {
            Console.WriteLine("Access denied");
            return false;
        }

    }

    public static void Main(string[] args)
    {
        // bool[] flags = new bool[5];
        // for (int i = 0; i < flags.Length; i++)
        // {
        //     Console.WriteLine($"{i}: {flags[i]}");
        // }

        // string[] arr = { "apple", "banana", "cherry" };
        // Array.Clear(arr, 1, 1);
        // for (int i = 0; i < arr.Length; i++)
        // {
        //     Console.WriteLine(arr[i]);
        // }
        // Array.Sort(arr);
        // for (int i = 0; i < arr.Length; i++)
        // {
        //     Console.WriteLine(arr[i]);
        // }

        // string text = Console.ReadLine();
        // string delimiter = Console.ReadLine();
        // string[] words = text.Split(' ');
        // Console.WriteLine(string.Join(delimiter, words));

        // string product = Console.ReadLine();
        // int qty = int.Parse(Console.ReadLine());
        // double price = double.Parse(Console.ReadLine());
        // string formattedString = CreateFormattedString(product, qty, price);
        // Console.WriteLine(formattedString);

        // prints a new array containing only the words longer than 5 characters
        // string[] arr1 = { "apple", "banana", "cherry" };
        // int length = 0;
        // for (int i = 0; i < arr1.Length; i++)
        // {
        //     if (arr1[i].Length > 5)
        //     {
        //         arr1[i] = arr1[length];
        //         length++;
        //     }
        // }
        // string[] arr2 = new string[length];
        // Array.Copy(arr1, 0, arr2, 0, length);
        // Console.WriteLine(string.Join(", ", arr2));

        // string text = Console.ReadLine();
        // string[] arrString = text.Split(",");
        // int[] numbers = new int[arrString.Length];
        // for (int i = 0; i < arrString.Length; i++)
        // {
        //     numbers[i] = int.Parse(arrString[i]);
        // }
        // double[] stats = CalculateStats(numbers);
        // Console.WriteLine("Sum: " + stats[0]);
        // Console.WriteLine("Average: " + stats[1]);
        // Console.WriteLine("Maximum: " + stats[2]);
        // Console.WriteLine("Minimum: " + stats[3]);

        // pyramid
        // int n = int.Parse(Console.ReadLine());
        // for (int i = 1; i <= n; i += 2)
        // {
        //     Console.WriteLine(new string('*', i));
        // }

        // Pattern Finder
        // Create a program that receives two arrays of strings as input and determines if the second array appears as a pattern within the first array (in consecutive order).
        // string arrString1 = Console.ReadLine();
        // string arrString2 = Console.ReadLine();
        // string[] str1 = arrString1.Split(",");
        // string[] str2 = arrString2.Split(",");
        // // Write your code below
        // bool found = false;
        // for (int i = 0; i < str1.Length; i++)
        // {
        //     if (str1[i] == str2[0])
        //     {
        //         int ii = i;
        //         for (int j = 1; j < str2.Length; j++)
        //         {
        //             ii++;
        //             if (ii >= str1.Length)
        //             {
        //                 break;
        //             }
        //             if (str1[ii] != str2[j])
        //             {
        //                 break;
        //             }
        //             if (j == str2.Length - 1)
        //             {
        //                 found = true;
        //                 Console.WriteLine(found);
        //                 return;
        //             }
        //         }

        //     }
        // }
        // Console.WriteLine(found);

        // jagged array
        // 5, 7, 10, 24, 41
        // 86, 13, 683, 64, 13
        // 42, 46, 791, 111, 9
        // 86, 88, 1845, 5, 15897
        // 9, 1, 5, 5, 6
        int[][] matrix = {
            new int[] { 5, 7, 10, 24, 41 },
            new int[] { 86, 13, 683, 64, 13 },
            new int[] { 42, 46, 791, 111, 9 },
            new int[] { 86, 88, 1845, 5, 15897 },
            new int[] { 9, 1, 5, 5, 6 }
        };

        // creates a jagged array representing a chess board (8x8) with all elements initialized to 0
        int[][] chessBoard = new int[8][];
        for (int i = 0; i < chessBoard.Length; i++)
        {
            chessBoard[i] = new int[8];
        }

        int[][] matrix2 = new int[3][] {
            new int[2],
            new int[3] { 500, 600, 700 },
            new int[1] { 800 }
        };

        int[][] matrix3 = new int[][] {
            new int[4] { 200, 500, 300, 500 },
            new int[3] { 500, 600, 700 },
            new int[2] { 800, 100 }
        };

        int[][] matrix4 = new int[3][];
        matrix4[0] = new int[2];
        matrix4[1] = new int[3];
        matrix4[2] = new int[1];

        // int[][] matrix5 = ProcessMatrix.processMatrix(matrix3);
        // for (int i = 0; i < matrix5.Length; i++)
        // {
        //     for (int j = 0; j < matrix5[i].Length; j++)
        //     {
        //         Console.Write(matrix5[i][j] + "\t");
        //     }
        //     Console.WriteLine();
        // }

        // 執行 dotnet run -- 30
        // 未更動： dotnet run --no-restore -- 30 
        if (args.Length == 0)
        {
            Console.WriteLine("請輸入題目編號。例如：dotnet run -- 30");
            return;
        }

        string questionNumber = args[0];

        switch (questionNumber)
        {
            case "30":
                new GuardClauses().Main0();
                break;
            case "31":
                new ExceptionHanding().Main0();
                break;
            case "32":
                new ExceptionHanding2().Main0();
                break;
            case "33":
                new ExceptionHanding3().Main0();
                break;
            case "37":
                new NullHandling1().Main0();
                break;
            case "61":
                new HashSet1().Main0();
                break;
            default:
                Console.WriteLine("無效的題目編號");
                break;
        }



    }
}


class PrintMatrix
{
    public static void printMatrix(int[][] matrix)
    {
        // Write your code here
        for (int i = 0; i < matrix.Length; i++)
        {
            for (int j = 0; j < matrix[i].Length; j++)
            {
                Console.Write(matrix[i][j] + "\t");
            }
            Console.WriteLine();
        }
    }
}

// Each element is replaced with the sum of its adjacent elements
public class ProcessMatrix
{
    public static int[][] processMatrix(int[][] matrix3)
    {
        // int[][] matrix3 = new int[][] {
        //     new int[4] { 200, 500, 300, 500 },
        //     new int[3] { 500, 600, 700 },
        //     new int[2] { 800, 100 }
        // };
        // Write your code here
        int[][] result = new int[matrix3.Length][];
        for (int i = 0; i < matrix3.Length; i++)
        {
            result[i] = new int[matrix3[i].Length];
            for (int j = 0; j < matrix3[i].Length; j++)
            {
                int sum = 0;
                // Sum adjacent elements
                for (int di = -1; di <= 1; di++)
                {
                    for (int dj = -1; dj <= 1; dj++)
                    {
                        if (Math.Abs(di) + Math.Abs(dj) == 1) // Check for adjacent cells
                        {
                            int ni = i + di;
                            int nj = j + dj;
                            if (ni >= 0 && ni < matrix3.Length && nj >= 0 && nj < matrix3[ni].Length)
                            {
                                sum += matrix3[ni][nj];
                            }
                        }
                    }
                }
                result[i][j] = sum;
            }
        }
        return result;
    }
}