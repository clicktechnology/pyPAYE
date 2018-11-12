# pyPAYE - A PAYE and NI Caluclator class for Python.
A Python class which calculates PAYE, National Insurance (N.I.), Employer's N.I. and Student Loan Repayment Deductions for the U.K. tax system for 2016-2017, 2017-2018 and 2018-2019.
 
# Installation
 
You can download the class by either..

(a) Clicking the 'Clone or download' button above, top right at https://github.com/clicktechnology/pyPAYE.git and downloading the package to a directory of your choice.

or

(b) In Linux, open a terminal window with Ctrl + Alt + T or click the start button and in the search dialog type 'terminal' or 'xterm'.  Click on the Terminal Emulator to start the terminal emulator.

Once opened, the terminal shows your prompt, similar to the one below.
```
bob@my-laptop ~ $
```

We use, unsurprisingly, software called 'git' to manage and control our software versioning so let's make sure it is installed.  Install it with the following command on Debian / Ubuntu Linux.

```
sudo apt-get install -y git
```

..entering your logon password to start the installation, if required.  Once installed, now type..

```
git clone https://github.com/clicktechnology/pyPAYE.git
```

and press return.  The paye module is downloaded to a subdirectory called paye-calculator.  Go straight there by typing..

```
cd paye-calculator
```

Now the class has been downloaded, you can install it by typing

```
python setup.py install
```

or, if you prefer to just see it in action, type..

```
./test.py
```


# Usage

Create a file called mytax.py using an editor of your choice.

Add in the following lines at the top of the file so the file can run from the command line.

```
#!/usr/bin/env python
# coding=utf-8
```

Next, we need to import the taxation class by adding this line next.

```
from taxation import Taxation
``` 

Now let's create a Taxation object from the Taxation class with the command

```
my_tax_object = Taxation()
```

OK, let's calculate the PAYE payable in 2016-2017 for say, £35,000

```
print "PAYE on £35,000 annually is £{:6,.2f} per month.".format(my_tax_object.calculate_paye(35000))
```

While the above is perfect, the line below demonstrates the class at its most basic.  Both lines work, but I'll use the one above for the purposes of nice formatting and demonstration.

```
print my_tax_object.calculate_paye(35000)
```

The complete file should look like this..

```
#!/usr/bin/env python
# coding=utf-8
        
from taxation import Taxation
        
my_tax_object = Taxation()
print "PAYE on £35,000 annually is £{:6,.2f} per month.".format(my_tax_object.calculate_paye(35000))
```

Now save and exit.  In the command line where the file is saved, type.. 

```
python ./mytax.py
```
    
The result shown is..

```
PAYE on £35,000 annually is £400.00 per month.
```

If you want the annual PAYE payable, simply change the default monthly parameter to 'False' as shown below..

```
print "PAYE on £35,000 annually is £{:6,.2f} per annum.".format(my_tax_object.calculate_paye(35000, False))
```

and then save and re-run to get..
```
PAYE on £35,000 annually is £4,800.00 per annum.
```

In the root of the package, the file called test.py contains additional calculations and examples of the calculation of Employer's NI, Employee's NI and Student Loan Repayments for both Plan 1 and Plan 2 repayment options.  If you have any problems, feel free to contact me at askaquestion@click-technology.com
