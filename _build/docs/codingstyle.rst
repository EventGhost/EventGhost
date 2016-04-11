:tocdepth: 1

Coding Style Guidelines
=======================

To follow this style guide is no duty for any plugin developer. It's mainly a 
description of how I (Bitmonster) write code for the project. 

General
-------

If not otherwise state here, :pep:`8` and :pep:`257` should be followed. 


Indentation
-----------

Four spaces and definitely **no tabs**. 


Maximum Line Length
-------------------

Maximum line length of 79 characters. Longer lines should be wrapped by 
surrounding expressions in parentheses rather than using \\. If you break up 
parentheses, let every parameter be on a line of its own indented by one 
level. The closing bracket should also be on a line of its own but with the 
same indentation as the line with the opening bracket. If additional 
parentheses are inside this construct, break them in the same way, if they 
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
            parameter1 is None
            and parameter2 is not None
            and (
                parameter3 == parameter4
                or parameter3 == parameter5
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
understand as this example with the same content::

    def MyMethodWithManyParameters(self, parameter1, parameter2,  parameter3,
                                                        parameter4, parameter5):
        if parameter1 is None and parameter2 is not None and \
                        (parameter3 == parameter4 or parameter3 == parameter5)):
            DoMyFunctionWithManyParameters(parameter1, DoAnotherFunction(
                    parameter2, parameter3, parameter4), ShortFunc(parameter2, 
                                                        parameter5), parameter5)
                                                        
                                                        
Blank Lines
-----------

Put two blank lines between function and method definitions. Three lines 
between class definitions. Inside functions or methods never use more than one 
consecutive blank line. 


Naming Conventions
------------------

Since EventGhost relies heavily on wxPython, it uses naming conventions, that 
are not so common in the Python world. But actually they are also quite 
similar to the ones used by the Microsoft Windows-API. 


**Classes, Methods, Functions**
    For all of these *MixedCase* is used (upper-case letter to start with, 
    words run together, each starting with an upper-case letter). 

**Class Attributes, Function Parameters, Local Variables**
    For all of these *mixedCaseExceptFirstWord* is used (lower-case letter 
    to start with, words run together, each starting with an upper-case 
    letter).
    
**Constants**
    *ALL_CAPS_WITH_UNDERSCORES* is used. 
    

    