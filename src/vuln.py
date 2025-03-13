# Vulnerable Python Code Example: Unsafe Use of eval()
def vulnerable_eval():
    user_input = input("Enter a mathematical expression: ")
    # WARNING: Using eval() on untrusted input is insecure. It may allow execution of arbitrary code.
    result = eval(user_input)
    print("Result:", result)

if __name__ == "__main__":
    vulnerable_eval()
