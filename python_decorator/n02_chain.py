def make_bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def make_italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@make_bold
@make_italic
def hello():
    return "Hello, world!"

print(hello())
'''
<b><i>Hello, world!</i></b>
'''



# ============================================
def my_decorator(n: int = 0):
    count = max(0, n)
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            pre, post = "", ""
            
            for i in range(count):
                if i % 2 == 0:
                    pre += "<div>"
                    post = "</div>" + post
                else:
                    pre += "<p>"
                    post = "</p>" + post
            
            wrapped_content = func(*args, **kwargs)
            
            return pre + "<b>" + str(wrapped_content) + "</b>" + post
        return wrapper
    return decorator
        
        

# Don't change below this line
n = int(input())

@my_decorator(n)
def my_function(s):
    return s.upper()

result = my_function(input())
print(result)