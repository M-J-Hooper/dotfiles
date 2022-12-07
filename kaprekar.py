def number_to_base(x, b, n):
    digits = [0] * n
    if x == 0:
        return digits

    i = 0
    while x:
        digits[i] = int(x % b)
        x //= b
        i += 1
    
    return digits


def base_to_number(x, b):
    result = 0
    for i in range(len(x)):
        digit = x[i]
        result += digit * (b ** i)

    return result
    
def base_to_str(x, rep="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    result = ''
    for digit in x[::-1]:
        result += rep[digit]

    return result


def long_sub(top, bottom, b):
    result = [0] * len(top)

    borrow = 0
    for i in range(len(top)):
        top_digit = top[i] - borrow
        bottom_digit = bottom[i]

        if top_digit < bottom_digit:
            borrow = 1
            top_digit += b
        else:
            borrow = 0

        result[i] = top_digit - bottom_digit
    
    return result


def converge(x, b):
    i = 0
    prev = [0] * n
    curr = x
    while prev != curr:
        top = curr.copy()
        top.sort()
        bottom = top[::-1]

        prev = curr
        curr = long_sub(top, bottom, b)

        if i > 50:
            return (False, i, curr) 
        i += 1
    
    return (True, i, curr)


for b in range(15, 16):
    for n in range(3, 6):
        print(f'For base {b} and {n} digits:')
        max = 1
        for i in range(n):
            max += (b -1) * (b ** i)
        
        all = -1
        none = True
        for i in range(max):
            x = number_to_base(i, b, n)
            (converged, iters, result) = converge(x, b)
            all = all and converged
            none = none and not converged

            if converged:
                print(f'{base_to_str(x)} ({base_to_number(x, b)}) converged to {base_to_str(result)} ({base_to_number(result, b)}) after {iters} iterations!')

        if all:
            print(f'Always converged!')

        if none:
            print(f'Never converged...')

    