## About
decimalcontext is a decorator to help create a local decimal context for a
specific function.

It works by injecting a new variable called `decimal_ctx` into the function's
global scope that you can use within the function. If the function accepts
any Decimal variables it will also convert those to the new decimal context.

## FAQ
### Why not use `decimal.localcontext`?
<br>You can, however, if your function passes `Decimal`s around and you need to change the `rounding` value then you will have to re-create your `Decimal` values (`d = ctx.create_decimal(d)`) to make sure they adhere to the correct context.

decimalcontext will re-create the incoming `Decimal` objects with the newly created decimal context.

This will make sure you will never use Decimal outside of the context you want to use it without changing the default thread's context.


Example:
```python
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from decimalcontext import decimal_context

@decimal_context(prec=2, rounding=ROUND_UP)
def calc_func1(a: Decimal, b: Decimal) -> Decimal:
    return a * b

@decimal_context(rounding=ROUND_DOWN)
def calc_func2(a: Decimal, b: Decimal) -> Decimal:
    return a * b

@decimal_context(prec=4, rounding=ROUND_DOWN)
def calc_func3(a: Decimal, b: Decimal) -> Decimal:
    print(a * b)
    decimal_ctx.prec = 2
    decimal_ctx.rounding = ROUND_DOWN
    a = decimal_ctx.create_decimal(a)
    b = decimal_ctx.create_decimal(b)
    print(a * b)


a = Decimal("2.4567")
b = Decimal("5.7654")

print("calc_func1: ", calc_func1(a, b=b))
print("calc_func2: ", calc_func2(a, b=b))
print("calc_func3:")
calc_func3(a, b)
```

NOTE: if you are creating new Decimal variables inside a function that is
decorated by the decimal_context decorator use `decimal_ctx.create_decimal` to
create Decimal variables that conforms to the context set in `decimal_ctx`.
