# The MIT License (MIT)
#
# Written by Eran Sandler
# Copyright (c) 2019 Peach Finance Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from decimal import Decimal, Context


def decimal_context(*args, **kwargs):
    """
    Inject a new decimal context into the function and convert all existing
    Decimal inputs to the new context.
    """

    def decorator(f):
        def inner_decorator(*a, **kwa):
            ctx = Context(*args, **kwargs)

            # Convert any Decimal object in args
            temp_args = list(a)
            for i in range(len(temp_args)):
                arg = temp_args[i]
                if isinstance(arg, Decimal):
                    temp_args[i] = ctx.create_decimal(arg)

            a = tuple(temp_args)

            # Convert any Decimal objects in kwargs
            for i in kwa:
                arg = kwa[i]
                if isinstance(arg, Decimal):
                    kwa[i] = ctx.create_decimal(arg)

            # Inject the newly created Decimal Context
            f.__globals__["decimal_ctx"] = ctx
            return f(*a, **kwa)
        return inner_decorator
    return decorator


if __name__ == "__main__":
    from decimal import *

    # Change "prec" inside the test function or the input to the
    # decimal_context decorator to see the different values of a and b based
    # on the supplied precision.
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
