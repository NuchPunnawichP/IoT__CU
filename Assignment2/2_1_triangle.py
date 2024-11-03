def print_triangle(n):
    for i in range(n):
        for j in range(n - i - 1):
            print(" ", end = "")
        if i == n//2 + 2:
            print("* Homework 2  *", end = "")
        else:
            for j in range(2*i + 1):
                if (i == n - 1) or (j == 0) or (j == 2*i):
                    print("*", end = "")
                else:
                    print(" ", end = "")
            
        print()
n = 10
print_triangle(n)
