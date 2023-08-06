Application Programming Interface
=================================
The generic function package provides means to define generic functions
and multi-methods. Additionally classes are provided that enable the
user to implement nearly all of Python's special methods as multi-methods.

.. module:: gf
   :synopsis: Provides generic functions, multi-methods and convenience classes
   

Basic Usage
-----------
One can define generic functions are generics and multi-methods with
Python`s special method support with juts two decorator functions and
optionally one decorator method.

Defining Generic Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~
Generic functions must be defined with the :func:`generic`-function.

.. decorator:: generic(default_function)

    Create a generic function with a default implementation provided
    by `default_function`.

    :param callable_object default_function: The generic's default implementation.

    The generic's name and docstring are taken from the `default_function`.
    
    Specialisations for different call signatures can be added with the
    :func:`method` and :meth:`<generic>.method` decorators.

    .. note:: `callable_object` can be a function or a type (a new style class).

    For example the generic :func:`foo`'s default implemenations just
    answers the arguments passed as a tuple:

        >>> from gf import generic
        >>> @generic
        ... def foo(*arguments):
        ...     """Answers its arguments."""
        ...     return arguments

    :func:`foo` can be called just like an ordinary function.

        >>> foo(1, 2, 3)
        (1, 2, 3)


.. function:: generic()

    Create an unnamed generic function with no default function and no implementation.

    Defining a generic function in this way has the same effect as defining a
    generic function with a default function that raises a `NotImplementedError`.

    This form is the simplest way to define a generic:

        >>> bar = generic()

    If this generic function is called a `NotImplementedError` is raised:

    >>> bar("Hello", "World")
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic None has no implementation for type(s): builtins.str, builtins.str

    .. note:: The name is added later when the first multi-method is added
           with :func:`method`.


.. function:: generic(name)

    Create a generic function with a name and no default implementation.

    :param str name: The generic's name accessible with the `__name__` attribute.

    If you define :func:`bar` in this way, a `NotImplementedError`
    raised will contain the generics name:
 
        >>> bar = generic("bar")
        >>> bar("Hello", "World")
        Traceback (most recent call last):
        ...
        NotImplementedError: Generic 'bar' has no implementation for type(s): builtins.str, builtins.str

    The docstring however is still `None`:

        >>> print(bar.__doc__)
        None

.. function:: generic(name, doc)

    Create a generic function with a name and a docstring, but 
    no default implementation.

    :param str name: The generic's name accessible with the `.__name__` attribute.
    :param str doc: The generic's docstring accessible with the `.__doc__` attribute.


    >>> bar = generic("bar", "A silly generic function for demonstration purposes")

    The generic now also has a docstring:

        >>> print(bar.__doc__)
        A silly generic function for demonstration purposes

Adding Multi-Methods
~~~~~~~~~~~~~~~~~~~~
Multi-methods can be added to a generic function with the :func:`method`-function

or the :meth:`<generic>.method` method.

.. decorator:: method()(implementation_function)

    Add a multi-method for the types given in the `implementation_function`\s
    type hints to the generic decorated.

    :param FunctionType implementation_function: The function implementing
        the multi-method.

    A multi-method specialising the :func:`foo` generic for
    two integers can be added as such:

        >>> from gf import method
        >>> @method()
        ... def foo(i0: int, i1: int):
        ...     return i0 + i1

    This makes :func:`foo` answer 3 for the following call:

        >>> foo(1, 2)
        3

    As you can see the types to dispatch on are defined using type hints
    as defined by `PEP 484`_. This contrasts with the `Python 2 version of GF`_,
    where types have to be `passed as arguments to the decorator`_.

    
    .. caution:: The generic function the multi-method is added to, must be defined
           in the multi-method's implementation function's global name-space.

           If this is not the case use the :meth:`<generic>.method`
           decorator.

    .. _PEP 484: https://www.python.org/dev/peps/pep-0484/
    .. _Python 2 version of GF: https://pypi.python.org/pypi/gf/
    .. _passed as arguments to the decorator: http://pythonhosted.org/gf/api.html#adding-multi-methods

.. decorator:: variadic_method()(implementation_function)

    Add a multi-method with a variable number of arguments to
    the generic decorated.

    :param FunctionType implementation_function: The function implementing
        the multi-method.

    This does essentially the same as :func:`method`, but
    accepts additional arguments to ones the specified by the parameter annotations.
    This is done by virtually adding an infinite set of of method
    defintions with the type :class:`object` used for the
    additional arguments. 

    This decorator can be used to implement functions like this:

    .. code:: python

        @variadic_method()
        def varfun1(tc: TC, *arguments):
            return (tc,) + tuple(reversed(arguments))

    This function can be called like this:

    .. code:: python

        varfun1(to, "a", "b", "c")

    and behaves in this case like being defined as:
    
    .. code:: python

        @method()
        def varfun1(tc: TC, o1: object, o2: object: o3: object, o4: object):
            return (tc,) + (o4, o3, o2, o1)

    Overlaps of variadic method definitions with non-variadic method
    definitions are always resolved towards the non-variadic method
    with the explicitly specified types.

.. decorator:: <generic>.method(implementation_function)

    Directly define a multi-method.
    
    :param FunctionType implementation_function: The function implementing
        the multi-method.

    `<generic>` needs not to be available in the implementation
    function's name-space. Additionally `implementation_function`
    can have a different name than the generic. The later leads
    to defining an alias of the generic function.

    For example a multi-method also available as bar can be defined as such:

        >>> @foo.method()
        ... def foobar(a_string: str):
        ...     return "<%s>" % a_string

    With this definition one can either call :func:`foo` with a string
    as follows:

        >>> foo("Hi")
        '<Hi>'

    Or :func:`foobar`:

        >>> foobar("Hi")
        '<Hi>'

.. decorator:: <generic>.variadic_method()(implementation_function)

    Directly define a multi-method with a variable number of arguments.
    
    :param FunctionType implementation_function: The function implementing
        the multi-method.

    This decorator is the variadic variant of :func:`<generic>.method`.


Advanced Usage
--------------
The follows section describe advanced uses cases of :mod:`gf`.

Calling Other Multi-Methods of The Same Generic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:mod:`gf` implements two ways to calls other methods of
the same generic.

New Style of :class:`super` Calls
.................................

The new way of calling other methods with the same arity of the same
generic (mis)uses the built-in :class:`super` type.

:class:`super` can be used to define :func:`foo` for integers:

     >>> @method()
     ... def foo(an_integer: int):
     ...     return foo(super(str, str(an_integer)))

Calling :func:`foo` with an integer now works as expected:

     >>> foo(42)
     '<42>'

Old Style of :class:`super` Calls
.................................

.. note:: This way of calling other methods of a generic
          function is deprecated.

As it is sometimes necessary with ordinary single dispatch methods
to call methods defined in a base class, it it is sometimes
necessary to reuse other implementations of a generic.
For this purpose the generic has :meth:`super`-method.

.. deprecated:: 0.2
.. method:: <generic>.super(*types)(*arguments)

    :param type types: An optionally empty list of built-in types or
                       new-style classes.
    :param arguments: An optionally empty list of Python objects.

    Directly retrieve and call the multi-method that implements
    the generic's functionally for `types`.

    One can add a (silly) implementation for string objects
    to :meth:`foo` like this:

        >>> @method()
        ... def foo(an_integer: int):
        ...     return foo.super(str)(an_integer)

    With this definition the generic's default implementation
    will be called for `float`-objects:

        >>> foo(42.0)
        (42.0,)

    While calling :func:`foo` with an integer yields a formatted string:

        >>> foo(42)
        '<42>'

    .. caution:: It is not checked whether the `arguments` passed
           are actually instances of `types`. This is consistent
           with Python's notion of duck typing.

Dispatch on Instances
~~~~~~~~~~~~~~~~~~~~~

Since version 0.2 :mod:`gf`'s
default dispatch algorithm dispatches on single instances, too:

    >>> silly = generic('silly')
    >>> @method()
    ... def silly(bla: str):
    ...     return '<S|' + bla + '|S>'

Thus we can call :func:`silly` with a string:

    >>> silly('Hello')
    '<S|Hello|S>'

But we can also define :func:`silly` for two integers:

    >>> @method()
    ... def silly(hitchhiker: 42, star_trek: 47):
    ...     return 'Bingo'

Now we can call :func:`silly` with exactly the right numbers:

    >>> silly(42, 47)
    'Bingo'

But calling silly with others fails like this:

    >>> silly(21, 21)
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic 'silly' has no implementation for type(s): builtins.int, builtins.int

The old behavior can be achieved by using the dispatch type 
:attr:`Dispatch.ON_CLASS`.

    >>> from gf import Dispatch
    >>> even_sillier = generic(Dispatch.ON_CLASS)
    >>> @method()
    ... def even_sillier(bla: str):
    ...     return '<SS|' + bla + '|SS>'

Thus we can call :func:`even_sillier` with a string:

    >>> even_sillier('Hello')
    '<SS|Hello|SS>'

But we can't define :func:`even_sillier` for two integers:

    >>> @method()
    ... def even_sillier(hitchhiker: 42, star_trek: 47):
    ...     return 'Bingo'
    Traceback (most recent call last):
    ...
    TypeError: Can't dispatch on instances in state: Dispatch.ON_CLASS

.. note:: The enumeration :class:`Dispatch` also has the option 
          :attr:`ON_OBJECT`, which is the new default for generic functions.

Class-Generics
~~~~~~~~~~~~~~

Since release 0.2 :mod:`gf` has some means to define the equivalent
of a class function with generic functions. This capability is defined
on a per :func:`generic` basis and not -- as one might expect -- on
a per :func:`method` basis.

The following example will explain this feature:

    >>> cm = generic(
    ...     'cm', 
    ...     """A class method (sort of)""",
    ...     Dispatch.ON_OBJECT_AND_CLASS_HIERARCHY)


One now can add methods to :func:`cm` that dispatch on the class
passed:

    >>> @method()
    ... def cm(integer: int):
    ...     return 'Integer'
    >>> @method()
    ... def cm(string: str):
    ...     return 'String'

This way we can dispatch on classes like:

    >>> cm(int)
    'Integer'
    >>> cm(str)
    'String'
    >>> cm(1)
    'Integer'
    >>> cm('Sepp')
    'String'

With the same dispatch type it is also possible to dispatch on instances:

    >>> @method()
    ... def cm(wow: 42):
    ...     return 'Jackpot'
    >>> cm(42)
    'Jackpot'
    >>> cm(4711)
    'Integer'

The normal -- and also the pre version 0.2 -- behavior is to dispatch
on the type of an instance only:

    >>> im = generic(
    ...     'im', 
    ...     """An instance method""",
    ...     Dispatch.ON_OBJECT)


One now can add methods to :func:`im` that dispatch on the class
of an instance passed as argument:

    >>> @method()
    ... def im(integer: int):
    ...     return 'Integer'
    >>> @method()
    ... def im(string: str):
    ...     return 'String'

But we can't dispatch on class arguments:

    >>> im(int)
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic 'im' has no implementation for type(s): builtins.type
    >>> im(str)
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic 'im' has no implementation for type(s): builtins.type
    >>> im(1)
    'Integer'
    >>> im('Sepp')
    'String'


Since the type of class is :class:`type` we can write one method
to dispatch on all classes:

    >>> @method()
    ... def im(cls: type):
    ...     return 'Class'

and get at least:

    >>> im(int)
    'Class'
    >>> im(str)
    'Class'

As mentioned above, it is also possible to dispatch on instances 
with the default dispatch type :attr:`Dispatch.ON_OBJECT`:

    >>> @method()
    ... def im(wow: 42):
    ...     return 'Oh Baby'
    >>> im(42)
    'Oh Baby'
    >>> im(4711)
    'Integer'


Merging Generics
~~~~~~~~~~~~~~~~

Two generic functions can merged into one generic function
with the help of the :func:`merge` function like this [#]_:

    >>> g_one = generic()
    >>> @method()
    ... def g_one(a: 1):
    ...     return 'one'
    >>> g_two = generic()
    >>> @method()
    ... def g_two(a: 2):
    ...     return 'two'

Both can be called with mixed results:

    >>> g_one(1)
    'one'
    >>> g_two(2)
    'two'
    >>> g_one(2)
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic None has no implementation for type(s): builtins.int
    >>> g_two(1)
    Traceback (most recent call last):
    ...
    NotImplementedError: Generic None has no implementation for type(s): builtins.int

Both generics can be merged into one generic by using the generic function
:func:`merge`:

    >>> from gf import merge
    >>> g_both = merge(g_one, g_two)
    >>> g_both(1)
    'one'
    >>> g_both(2)
    'two'


Testing For Being a Generic Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the need arises one can test any object for being a generic function
with the help of the :func:`isgeneric` generic function

>>> from gf import isgeneric
>>> isgeneric(0)
False
>>> isgeneric(object)
False
>>> isgeneric(g_one)
True
>>> isgeneric(g_both)
True
>>> isgeneric(isgeneric)
True
>>> isgeneric(generic)
True


The Implementation Class
~~~~~~~~~~~~~~~~~~~~~~~~

Behind the function generated by :func:`generic` there is 
ordinary Python class. This Python class can be access with
the :func:`get_implementation` generic function like this:

   >>> from gf import get_implementation
   >>> get_implementation(g_one)
   <gf.base.GenericFunction object at ...>

Of course it is also possible to provide a different implementation class
when creating a generic function [#]_:

   >>> from gf.base import GenericFunction
   >>> class TracingGenericFunction(GenericFunction):
   ...
   ...    def __call__(self, *args):
   ...        print('Calling %r with %r' % (self.name, args))
   ...        return super().__call__(*args)

A generic function with the new implementation can be generated like 
this:

   >>> from gf.base import _generic
   >>> tg = _generic(
   ...     name='tg',
   ...     implementation_constructor=TracingGenericFunction)
   >>> get_implementation(tg)
   <TracingGenericFunction object at ...>
   >>> @method()
   ... def tg(a: int, b: int):
   ...     return a ** b

It can be invoked in the usual way:

   >>> tg(2, 4)
   Calling 'tg' with (2, 4)
   16

For easier use of those traced generics, on should define a
convenience function like this:

   >>> tracing_generic = generic('tracing_generic')
   >>> @method()
   ... def tracing_generic(name:str):
   ...     return _generic(
   ...             name=name,
   ...             implementation_constructor=TracingGenericFunction)

With this generic function [#]_ one could define :func:`tg` much easier
like this:

   >>> tg = tracing_generic('tg')
   >>> @method()
   ... def tg(a: int, b: int):
   ...     return a ** b

Calling the :func:`tg` works like mentioned above:

   >>> tg(2, 6)
   Calling 'tg' with (2, 6)
   64

The Generic :class:`Object`-Library
-----------------------------------

The :mod:`gf`-package also provides an abstract base class called
:class:`gf.AbstractObject` and class called :class:`gf.Object`. 

Both classes map nearly all of Python's special methods to generic
functions.

There is also a :class:`Writer`-class and some convenience
and helper generics like :func:`as_string`, :func:`spy`,
:func:`__out__` and :func:`__spy__`.

The implementation of the aforementioned objects is contained
in the :mod:`gf.go`, but the objects are also available
for direct import from :mod:`gf`.

The following text is generated from the docstring in :mod:`gf.go`.

.. automodule:: gf.go
    :members:
    :special-members:


.. [#] This functionality was necessary for one of my own projects,
       but my be rather useless for ordinary Python projects.
.. [#] :class:`GenericFunction` and :func:`_generic` are
       not part of the API and must there fore be imported
       from :mod:`gf.base`.
.. [#] To be really useful :func:`tracing_generic` should be
       defined for more types to enable its users to pass 
       documentation-strings, instances of :class:`Dispatch` and
       the like.
