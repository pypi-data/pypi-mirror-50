"""This module implements help command.
"""
def ___help():
    """Function lists the commands supported by our application.
    """
    print("""These shell commands are defined internally.\
Type `name --help` or `name -h` to find out more about the function `name'
ls [OPTION]
mkdir DIRECTORY...
pwd
rmdir DIRECTORY
cd [DIRECTORY]
cat [OPTION] [FILE]...
cp SOURCE DIRECTORY
rm [FILE] ...
mv [SOURCE] ... [TARGET]
grep [-n] [WORD] [FILE] 
head -n [FILE]
tail -N [FILE]
sizeof [fILE]
find [PATH] [FILE]
date
whoami
hostname
timeit
exit
history""")
