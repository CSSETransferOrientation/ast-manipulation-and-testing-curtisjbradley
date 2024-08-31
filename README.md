# Binary Operator Simplifier 

## Completed Subtasks

**1) Automated Testing** - Tests in *mult_id*, *mult_by_zero*, *combined*, and *arith_id* will run given that there is a matching output file.

**2) Arithmetic Identiy** - *BinOpAst.additive\_identity* should be able to correctly resolve any additive identities

**3) Multiplicative Identity** - *BinOpAst.multiplicative\_identity* should be able to correctly resolve the multiplicative identity

**4) Multiply by Zero** - *BinOpAst.mult\_by\_zero* is able to resolve multiplications by 0.

**5) Constant Folding** - *BinOpAst.constant_folding* will evaluate constant arithmetic. 

**6) Combined -** *BinOpAst.simplify\_binops* runs Multiply by Zero, Arithmetic Identity, Multiplicative Identity and Constant Folding, in that order.

### Issues

Probably some test cases I missed.

The constant folding parser treats negative numbers as unknowns.




## Reflection

The most valuable part of the assignment was learning more about how unit testing works. Prior to this class I had no expericence creating tests and running testing on code.

Through this assignment I've found that I don't really enjoy the quirks of Python, especially dealing with object methods.

The hardest part of this assignment was figuring out how to use the unit tester, and how to implement it.

