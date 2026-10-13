# Todos

## Variables

Add mutability tracking for variables (class attr)

Add call tracking and prefix unused variables with and `_` for rust conventions purposes (class attr)

## Misc Issues

### Issue
the ending curly brace isnt being placed properly becuase of the if_true rather than if_false.
### Solution
seems to work? added class attribute to track how many open expressions require closure, and that is checked andrectified when the loop is closed

### Issue
the range -> 0..k isnt working now because a VAR that has an int needs to be treated like a CONST, but a VAR that has a !vec needs to be treated like a !vec, aka with `.iter()` not `0..<CONST>`
### Solution
made sure that whenever `LOAD_FAST` is called and the variable is loaded into the stack, its datatype is retrieved from the `self.variables` attribute array and assigned accordingly, and then, it's checked in the `transform_loop` function to assign proper rust syntax
### Issue
the vec! needs to be mut if append end up being called
### Solution
added a loop in the _append function to loop through buildStack to find the array, and toggle the reqMut to True
