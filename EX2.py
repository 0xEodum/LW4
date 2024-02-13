def check_parentheses_balance(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    balance = 0
    for char in text:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            if balance < 0:
                return False

    return balance == 0

print(check_parentheses_balance('brackets.txt'))