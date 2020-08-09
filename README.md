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

```
# quine (outputs its own source code)
(9999)(60)(60)(62)(62)(62)(60)(60)(62)(60)(93)(60)(60)(62)(62)(62)(60)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(60)(60)(62)(62)(93)(41)(0)(40)(62)(60)(62)(41)(0)(40)(41)(7777)(40)(62)(60)(62)(41)(1)(40)(60)(60)(62)(62)(60)(62)(60)(62)(60)(62)(62)(62)(60)(60)(62)(62)(62)(60)(62)(41)(0)(40)(91)(60)(60)(62)(62)(60)(62)(41)(1)(40)(93)(41)(0)(40)(62)(60)(62)(41)(0)(40)(41)(8888)(40)(62)(60)(62)(41)(1)(40)(62)(60)(62)(62)(60)(62)(60)(62)(60)(62)(62)(62)(60)(60)(62)(62)(62)(60)(62)(41)(0)(40)(91)(60)(60)(62)(62)(62)(62)(60)(41)(2)(40)(62)(60)(62)(41)(1)(40)(62)(60)(62)(62)(62)(60)(60)(60)(62)(60)(62)(41)(0)(40)(62)(60)(62)(62)(62)(62)(62)(60)(41)(40)(40)(60)(60)(62)(62)(62)(60)(62)(62)(62)(62)(62)(60)(41)(7777)(40)(62)(60)(62)(41)(1)(40)(91)(41)(1)(40)(41)(1)(40)(41)(8888)(40)(62)(60)(62)(41)(1)(40)(60)(60)(62)(60)(93)(93)(41)(0)(40)(60)(60)(62)(62)(60)(62)(60)(41)(41)(40)(62)(60)(62)(62)(60)(62)(60)(62)(60)(62)(62)(62)(60)(60)(62)(62)(60)(60)(62)(62)(60)(62)(60)(41)(40)(40)(62)(60)(62)(62)(91)(60)(60)(62)(62)(60)(60)(62)(62)(62)(60)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(60)(60)(62)(62)(62)(60)(62)(41)(1)(40)(91)(41)(1)(40)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(62)(60)(62)(41)(0)(40)(60)(60)(62)(62)(60)(62)(60)(41)(41)(40)(62)(60)(62)(62)(60)(62)(60)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(60)(60)(62)(62)(60)(62)(60)(41)(40)(40)(60)(60)(62)(60)(93)(93)(41)(0)(40)(62)(60)(62)(62)(62)(62)(60)(62)(62)(91)(60)(60)(62)(62)(60)(60)(62)(62)(62)(60)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(60)(60)(62)(62)(62)(60)(62)(41)(0)(40)(91)(41)(1)(40)(60)(60)(60)(41)(1)(40)(41)(9998)(40)(62)(60)(62)(41)(1)(40)(1)><>(9998)(1)<<<(1)[(0)><>>><<(9998)(1)<<<<>>><<>><<[>><>>>><>(0)]]<><<(40)<><>><<(9998)(1)<<<<><>><>(41)<><>><<(0)><>(9998)(1)<<<(1)[(1)><>>><<(9998)(1)<<<<>>><<>><<[>><>(40)<><>><<>><<>>><><><>><>(41)<><>><<(0)]]<><<(1)><>(8888)(1)(1)[(1)><>(7777)<>>>>><>>><<(40)<>>>>><>(0)><><<<>>><>(1)><>(2)<>>>><<[(0)><>>><<>>><><><>><>(1)><>(8888)(0)><>(0)](1)><>><<[(0)><>>><<>>><><><>><<(1)><>(7777)(0)><>(0)]>><<(9998)(1)<<<<>>><<]<><<>>><<
```

## Specification

Tru is a stack-based virtual machine.

There are two built-in stacks which tru programs can manipulate using the following set of instructions.

### Instructions

| Instruction  |  Description |
|---|---|
| `(`  |  Start describing an integer to push |
| `)`  | Push the integer between the corresponding opening bracket to the current stack.  |
| `<><>><<`  | Print character: Pop from the current stack and print the value as a UTF-8 character  |
| `<><>><>`  |  Print integer: Pop from the current stack and print the value as a number |
| `<><>>>`  | Integer input: Get an integer input and push to the current stack as a number |
| `<><><`  | Character input: Get an integer input and push to the current stack as a UTF-8 character |
| `>>><<`  | End: Specify the end of the program  |
| `>>><>`  | Move: Pop from the current stack and push to the other stack |
| `<><<`  |  Discard: Pop from the current stack and discard |
| `>><<`  | Duplicate the top value of the current stack  |
| `>><>`  |  Swap the top two values of the current stack |
| `>>>>`  |  Subtract |
| `<<<`  | Add  |
| `<<>`  |  Greater than |
| `<>>`  | Equals  |
| `><<`  | Not  |
| `><>`  | Select stack: Pop from the stack and set the current stack equal to the value. The stacks are indexed 0 and 1.  |
| `[`  | Jump: Pop the current stack and jump to the matching ] if the value is zero  |
| `]`  | Jump: Pop the current stack and jump to the matching [ if the value is non-zero   |
| `#`  | Comment: ignore all characters that follow for the rest of the line |

In summary, instructions are represented by only using bracket characters:

```
(, ), [, ], <, >
```

Instructions are prefix-free and can directly follow one another. For instance,

```
(1)
>><<
(2)
<<<
<><>><<
```

is equivalent to

```
(1)>><<(2)<<<<><>><<
```

### Linebreaks and spaces

Linebreaks and spaces are permitted and generally ignored. However, numbers and instructions cannot be broken with linebreaks or spaces.

```
# Okay
(
  10
)

# Not okay
(
1
0
)

# Okay
>><<

# Not okay
>>
<<
```

One can write a relatively readable tru program using linebreaks, spaces and comments. It can always be compressed due to the prefix-free nature of the instructions.

## Tru VM implementation

Pytru is an official tru virtual machine implemented in Python. You can use it to execute tru code.

```
# pytru requires Python 3
python3 ./tru.py input_file_path
```

## License

Apache 2.0
