A humble project by me (Abdallah Elbeheiry) and Youssef atef made to solve various types of equations with different methods, for Cairo university faculty of science

Important notes:
- Equations written cannot be in form U = V, as the program assumes the equation is equal to zero, so the correct form is U - V and the program will interpret it as U - V = 0
- writing formats like 2x will not work, it must be 2*x instead of 2x to be interpreted correctly
- when using euler's approximation method, be aware with giving x0 and y0 values that make the equation divide by zero
- for writing π you need to write 'pi' ('' not included) and e is the normal euler constant
- normal mathematical operators like log(function) and ln(function), as well as trigonometric and hyperbolic functions work, they just need to be written correctly
- writing sh(function) and ch(function) won't work, replace with sinh(function) and cosh(function)
- for inverse trigonometric or hyperbolic values, write 'arc' before the function ('' not included) i.e -> arcsin(function), arctan(function), arcsinh(function)
- some Ordinary differential equations crash due to the algorithm not being able to solve it... although most Ordinary differential equations work fine
- There may be inaccuracy with the results, it's normal considering that this is a computer algorithm
- All constants resulting from integrating (whenever solving ODEs using integrating factors or exact methods) are automatically replaced with 1, which may result in some inaccuracy but we weren't able to design an algorithm that correctly handles the constants
- This program uses standard computer algorithm operators (+ - * ^ % and so on)
