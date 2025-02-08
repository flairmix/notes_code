# Table of Contents

- [Table of Contents](#table-of-contents)
    - [C# Hello World](#c-hello-world)
    - [f-string / string interpolation](#f-string--string-interpolation)
    - [double separator culture](#double-separator-culture)
    - [double round](#double-round)
    - [implicit conversion](#implicit-conversion)
    - [explicit conversion](#explicit-conversion)


### C# Hello World
```C#
Console.WriteLine("Hello");
```

### f-string / string interpolation
```C#
string petsName = "man";
Console.WriteLine($"my pets name is {petsName} ");
```

### double separator culture
```C#
using System.Globalization;
double myNumber = double.Parse(Console.ReadLine(), CultureInfo.InvariantCulture);
```
### double round
```C#
Console.WriteLine($"myNumber + 10 is {Math.Round(myNumber + 10, 2)}");
```

### implicit conversion 

You can't fit smaller number in biggest by memory used. 
- double can fit int, but can't in opposite way
- long can fit int 
- etc
  
```C#
int myInt = 10;
double myDouble = myInt;
```

### explicit conversion 

```C#
long myLong = 1000000000;
int myInt = (int)myLong;
// it's wrong, we will lost data. MyInt is cut that can't fit

float myFloat = 123.123f;
double myDouble = 123.123123123123;
myFloat = (float)myDouble;
// it's wrong. myFloat cuts numbers after dot; 
```
