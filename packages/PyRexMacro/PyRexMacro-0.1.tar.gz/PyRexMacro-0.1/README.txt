PyRex is a macro processor.

Macro Calls:
  {#} or {#WHERE}
      Replaced by name-of-source-file:line-number
  {#DATE}
      Replaced by date, e.g. 2017-12-25
  {#TIME}
      Replaced by 24 hour time, e.g. 14:27:05
  {#DEFINE, usermacro, definition of user macro}
      The definition can contain embedded macro calls or'{',
      '}', and ',' characters, escaped with a backslash.
      (See NOTES below.)
  {#usermacro}
      Replaced by usermacro's definition.
      Arg regs, #1 ... #9, meaningful only inside a usermacro,
      are replaced by value of arg of enclosing usermacro.
  {#IFEQ,macroname,val,trueval,falseval}
      Replaced by trueval if the value of macroname == val
      else replaced by falseval.
  {#INCLUDE,filepath}
      Replaced by the contents of filepath
  {#ENV,name}
      Replaced by value of name in the OS environment.
NOTES:
Inside the macro brackets, embedded balanced brackets (for example
embedded macro calls) may be nested; similarly a comma separator
is only recognized when it is not nested inside internal brackets.

After a macro's value replaces the macro call, scanning continues at
the beginning of the substituted text, supporting user macros whose
definition contain macro calls.
