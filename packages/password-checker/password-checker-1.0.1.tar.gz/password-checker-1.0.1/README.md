### Python Password Checker
![](Package_Banner.png)

A Python package to check vulnerability and strength pf a password.

### Usage

```python

# importing the package 
from password_checker import pc4

checker = ps4.PasswordChecker('YOUR_PASSWORD')

# The PasswordChecker will take String as a Argument

# To check vulnerability of a password.

checker.isvulnerable()  # Returns True if it is vulnerable.

```

```python

# importing the package 
from password_checker import pc4

checker = ps4.PasswordChecker('YOUR_PASSWORD')

# The PasswordChecker will take String as a Argument

# To check Strength of a password.

checker.isstrength()  # Returns True if it is following password policy.

```