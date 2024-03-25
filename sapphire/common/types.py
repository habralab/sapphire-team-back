from pydantic import constr

Password = constr(pattern=r"^[\w\(\)\[\]\{\}\^\$\+\*@#%!&]{8,}$")
