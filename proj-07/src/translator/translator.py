import sys
import glob


def parse(file) -> tuple[list[str], dict[str, int]]:
    """
    Reads an assembly program and returns a list of parsed instructions and a dictionary of labels with their corresponding line numbers.
    :param file: File object to read from
    :return: tuple of list of instructions and dictionary of labels with their corresponding line numbers
    """
    instructions = file.read()
    instructions = instructions.split("\n")
    # Remove trailing and leading whitespace
    instructions = [line.strip() for line in instructions]
    # Remove empty lines and comments
    instructions = [
        line
        for line in instructions
        if line and not line.startswith("//")
    ]
    return instructions


def transpire_instructions(instructions: list[str]) -> list[str]:
    label_store = label_generator()
    assembly_code = []
    for instruction in instructions:
        instruction = instruction.split()
        if instruction[0] == "pop":
            assembly_code.append(pop(instruction[1], instruction[2]))
        elif instruction[0] == "push":
            assembly_code.append(push(instruction[1], instruction[2]))
        elif instruction[0] == "add":
            assembly_code.append(add())
        elif instruction[0] == "sub":
            assembly_code.append(sub())
        elif instruction[0] == "neg":
            assembly_code.append(neg())
        elif instruction[0] == "eq":
            assembly_code.append(eq(label_store))
        elif instruction[0] == "gt":
            assembly_code.append(gt(label_store))
        elif instruction[0] == "lt":
            assembly_code.append(lt(label_store))
        elif instruction[0] == "and":
            assembly_code.append(vm_and())
        elif instruction[0] == "or":
            assembly_code.append(vm_or())
        elif instruction[0] == "not":
            assembly_code.append(vm_not())
    return assembly_code


def translate(file) -> str:
    instructions = parse(file)
    assembly_code = transpire_instructions(instructions)
    return "\n".join(assembly_code) + "\n(END)\n@END\n0;JMP\n"


def read_write_file(file_path: str):
    with open(file_path, "r") as file:
        assembly_code = translate(file)
    output_path = file_path.replace(".vm", ".asm")
    with open(output_path, "w") as file:
        file.write(assembly_code)


def increment_sp() -> str:
    return "@SP\nM=M+1\n"


def decrement_sp() -> str:
    return "@SP\nM=M-1\n"


pointers = {
    "argument": "ARG",
    "local": "LCL",
    "static": "16",
    "this": "THIS",
    "that": "THAT",
    "pointer": "3",
    "temp": "5",
}


def compute_address(segment: str, index: int) -> str:
    # postcondition: R13 holds the address of segment index
    seg_pointer = pointers[segment]
    return f"@{seg_pointer}\nD=A\n@{index}\nD=D+A\n@R13\nM=D\n"


def push_from_D() -> str:
    return "".join(["@SP\nA=M\nM=D\n", increment_sp()])


def pop_to_D() -> str:
    return "".join([decrement_sp(), "@SP\nA=M\nD=M\n"])


def label_generator():
    n = 0
    while True:
        yield f"GENERATED_LABEL_{n}"
        n += 1


def add() -> str:
    instructions = "".join(
        [
            "\n// add\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            "@R14\nD=D+M\n",
            push_from_D(),
        ]
    )
    return instructions


def sub() -> str:
    instructions = "".join(
        [
            "\n// sub\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            "@R14\nD=D-M\n",
            push_from_D(),
        ]
    )
    return instructions


def neg() -> str:
    instructions = "".join(
        [
            "\n// neg\n",
            pop_to_D(),
            "D=-D\n",
            push_from_D(),
        ]
    )
    return instructions


def eq(label_store) -> str:
    label1 = next(label_store)
    label2 = next(label_store)
    instructions = "".join(
        [
            "\n// eq\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            f"@R14\nD=D-M\n@{label1}\nD;JNE\nD=-1\n@{label2}\n0;JMP\n({label1})\nD=0\n({label2})\n",
            push_from_D(),
        ]
    )
    return instructions


def gt(label_store) -> str:
    label1 = next(label_store)
    label2 = next(label_store)
    instructions = "".join(
        [
            "\n// gt\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            f"@R14\nD=D-M\n@{label1}\nD;JGT\nD=-1\n@{label2}\n0;JMP\n({label1})\nD=0\n({label2})\n",
            push_from_D(),
        ]
    )
    return instructions


def lt(label_store) -> str:
    label1 = next(label_store)
    label2 = next(label_store)
    instructions = "".join(
        [
            "\n// lt\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            f"@R14\nD=D-M\n@{label1}\nD;JLT\nD=-1\n@{label2}\n0;JMP\n({label1})\nD=0\n({label2})\n",
            push_from_D(),
        ]
    )
    return instructions


def vm_and() -> str:
    instructions = "".join(
        [
            "\n// and\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            "@R14\nD=D&M\n",
            push_from_D(),
        ]
    )
    return instructions


def vm_or() -> str:
    instructions = "".join(
        [
            "\n// or\n",
            pop_to_D(),
            "@R14\nM=D\n",
            pop_to_D(),
            "@R14\nD=D|M\n",
            push_from_D(),
        ]
    )
    return instructions


def vm_not() -> str:
    instructions = "".join(
        [
            "\n// not\n",
            pop_to_D(),
            "D=!D\n",
            push_from_D(),
        ]
    )
    return instructions


def pop(segment: str, index: int) -> str:
    instructions = "".join(
        [
            f"\n// pop {segment} {index}\n",
            pop_to_D(),
            "@R14\nM=D\n",
            compute_address(segment, index),
            "@R14\nD=M\n@R13\nA=M\nM=D\n",
        ]
    )
    return instructions


def push(segment: str, index: int) -> str:
    if segment != "constant":
        instructions = "".join(
            [
                f"\n// push {segment} {index}\n",
                compute_address(segment, index),
                "@R13\nA=M\nD=M\n",
                push_from_D(),
            ]
        )
    else:
        instructions = "".join(
            [
                f"\n// push {segment} {index}\n",
                f"@{index}\nD=A\n",
                push_from_D(),
            ]
        )
    return instructions


def main():
    if len(sys.argv) >= 2:
        input_files = sys.argv[1:]
    else:
        input_files = glob.glob("*.vm")
    for input_file in input_files:
        read_write_file(input_file)
