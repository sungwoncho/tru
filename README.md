# tru

tru is an esoteric programming language of brackets with prefix-free code.

## Examples

Below are some tru code examples.

```
# print hello world
(0)(10)(33)(100)(108)(114)(111)(119)(32)(44)(111)(108)(108)(101)(72)>><<[<><>><<>><<]>>><<
```

```
# print 25th Fibonacci number
(1)(25)(1)><>(1)(0)><>(1)>>>>>><<[(0)><>(1)>>>>>><<[>><>(1)><>>><<(0)><>>>><>(1)><><<<>><>>>><>(0)><>>><>(1)>>>>>><<](0)](1)><><><>><>>>><<
```

```
# sum first 1000 positive integers
(1000)>><<>>><>(1)><>1(111)[(1)>>>>1>><<>>><>(0)><>0<<<(1)><>1>><<(1)<>>><<](0)><><><>><>>>><<
```

## Design

Instructions are represented by only using bracket characters:

* `(`, `)`, `<`, `>`, `[`, `]`

Instructions are prefix-free and can directly follow one another. For instance,

```
(1)
>><<
<<<
<><>><<
```

is equivalent to

```
(1)>><<<<<<><>><<
```

## Specification

| Instruction  |  Description |
|---|---|
| (  |  Start describing an integer to push |
| )  | Push the integer between the corresponding opening bracket to the current stack.  |
| <><>><<  | Print character: Pop from the current stack and print the value as a UTF-8 character  |
| <><>><>  |  Print integer: Pop from the current stack and print the value as a number |
| <><>>>  | Integer input: Get an integer input and push to the current stack as a number |
| <><><  | Character input: Get an integer input and push to the current stack as a UTF-8 character |
| >>><<  | End: Specify the end of the program  |
| >>><>  | Move: Pop from the current stack and push to the other stack |
| <><<  |  Discard: Pop from the current stack and discard |
| >><<  | Duplicate the top value of the current stack  |
| >><>  |  Swap the top two values of the current stack |
| >>>>  |  Subtract |
| <<<  | Add  |
| <<>  |  Greater than |
| <>>  | Equals  |
| ><<  | Not  |
| ><>  | Select stack: Pop from the stack and set the current stack equal to the value  |
| [  | Jump: Pop the current stack and jump to the matching ] if the value is nonzero  |
| ]  | Jump: Pop the current stack and jump to the matching ] if the value is zero   |
| #  | Comment  |

