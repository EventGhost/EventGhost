:tocdepth: 1

Coding Style Guidelines
=======================

When contributing code to the EventGhost project, please follow this style 
guide to the letter.


General
-------

If not otherwise stated here, :pep:`8` and :pep:`257` should be followed. 


Indentation
-----------

Use four spaces and definitely **no tabs**. 


Maximum Line Length
-------------------

Maximum line length is 79 characters. Longer lines should be wrapped by 
surrounding expressions in parentheses rather than using \\. If you break up 
parentheses, let every parameter be on a line of its own, indented by one 
level. The closing bracket should also be on a line of its own, but with the 
same indentation as the line with the opening bracket. If additional 
parentheses are inside this construct, break them in the same way if they 
would otherwise be longer than the maximum line length. An example::

    def MyMethodWithManyParameters(
        self,
        parameter1,
        parameter2,
        parameter3,
        parameter4,
        parameter5
    ):
        if (
            parameter1 is None and
            parameter2 is not None and
            (
                parameter3 == parameter4 or
                parameter3 == parameter5
            )
        ):
            DoMyFunctionWithManyParameters(
                parameter1,
                DoAnotherFunction(
                    parameter2,
                    parameter3,
                    parameter4
                ),
                ShortFunc(parameter2, parameter5),
                parameter5
            )

Even though this looks wasteful and odd in the beginning, it is easier to 
understand than this example with the same content::

    def MyMethodWithManyParameters(self, parameter1, parameter2,  parameter3,
                                                        parameter4, parameter5):
        if parameter1 is None and parameter2 is not None and \
                        (parameter3 == parameter4 or parameter3 == parameter5)):
            DoMyFunctionWithManyParameters(parameter1, DoAnotherFunction(
                    parameter2, parameter3, parameter4), ShortFunc(parameter2, 
                                                        parameter5), parameter5)
                                                        
                                                        
Blank Lines
-----------

Use two lines of separating whitespace **after** class definitions, and no 
more than one line anywhere else.


Naming Conventions
------------------

Since EventGhost relies heavily on wxPython, it uses naming conventions that 
may be uncommon in the Python world, but are actually quite similar to the 
ones used in Microsoft's Win32 API. 


**Classes, Methods, Functions**
    For all of these, *MixedCase* is used (uppercase letter to start with, 
    words run together, each starting with an uppercase letter). 

**Class Attributes, Function Parameters, Local Variables**
    For all of these, *mixedCaseExceptFirstWord* is used (lowercase letter 
    to start with, words run together, each starting with an uppercase 
    letter).
    
**Constants**
    *ALL_CAPS_WITH_UNDERSCORES* is used. 
