=======
History
=======

0.1.2 (2019-07-30)
==================

- Fixed a bug where hts files were opened in the wrong mode, with
  inconsistent results.

0.1.1 (2019-07-05)
==================

- Fixed an ugly timezone bug that caused the data to refer to a
  different time than what the timestamp actually said.
- When the timezone was missing from the input files, there was an
  incomprehensible AttributeError. This was fixed and now it provides an
  understandable error message.

0.1.0 (2019-06-21)
==================

- Initial release
