import abstract
import config


JSBot = abstract.JSBot
JSTop = abstract.JSTop
JSUndefNaN = abstract.JSUndefNaN
JSPrimitive = abstract.JSPrimitive
JSObject = abstract.JSObject
JSRef = abstract.JSRef

ref_id = 1 # id 0 is reserved for global scope
binary_handlers = []
update_handlers = []
unary_handlers = []
global_symbols = []
preexisting_objects = []

def to_bool(v):
    if v is JSUndefNaN:
        return False

    if isinstance(v, JSPrimitive):
        if type(v.val) is int:
            return v.val != 0
        elif type(v.val) is bool:
            return v.val
        elif type(v.val) is str:
            return len(v.val) > 0
        else:
            raise ValueError("truth_value: unhandled concrete type" + str(type(v.val)))
    elif isinstance(v, JSRef):
        return True
    else:
        raise ValueError("truth_value: unhandled abstract type" + str(type(v)) + "(value: " + str(v) + ")")

def handle_binary_operation(opname, arg1, arg2):
    r = JSTop
    for f in binary_handlers:
        r = f(opname, arg1, arg2)
        if r is not JSTop:
            break
    return r

def handle_update_operation(opname, arg):
    r = JSTop
    for f in update_handlers:
        r = f(opname, arg)
        if r is not JSTop:
            break
    return r

def handle_unary_operation(opname, arg):
    r = JSTop
    for f in unary_handlers:
        r = f(opname, arg)
        if r is not JSTop:
            break
    return r

def register_preexisting_object(obj):
    global ref_id
    preexisting_objects.append((ref_id, obj))
    ref_id = ref_id + 1
    return ref_id - 1

def register_update_handler(h):
    update_handlers.append(h)

def register_binary_handler(h):
    binary_handlers.append(h)

def register_unary_handler(h):
    unary_handlers.append(h)

def register_global_symbol(name, value):
    global_symbols.append((name, value))

def register_method_hook(hook):
    JSObject.add_hook(hook)

for p in config.enabled_plugins:
    __import__("plugins." + p)
