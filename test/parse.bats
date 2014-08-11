#!/usr/bin/env bats

# Creates a test fixure changelog
setup_changelog() {
  tail -9 CHANGELOG.rst > $BATS_TMPDIR/test-changelog
}

# Deletes the test fixture changelog
delete_changelog() {
  rm $BATS_TMPDIR/test-changelog
}

@test "--help prints parse help" {
  run ./chag parse --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag parse") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag parse --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "ERROR: Unknown option") -ne 0 ]
}

@test "parse requires a FILENAME" {
  run ./chag parse
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "parse requires a FILENAME") -ne 0 ]
}

@test "parse ensures FILENAME exists" {
  run ./chag parse /path/to/does/not/exist
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "parse ensures the tag exists" {
  setup_changelog
  run ./chag parse --tag 9.9.9 $BATS_TMPDIR/test-changelog
  delete_changelog
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Tag 9.9.9 not found") -ne 0 ]
}

@test "parse can parse a specific tag" {
  run ./chag parse --tag 0.0.1 CHANGELOG.rst
  [ $status -eq 0 ]
  # The filename is randomly generated, so just check for "/"
  [ $(expr "${lines[0]}" : "0.0.1 2014-08-10 /") -ne 0 ]
  # Ensure the file exists
  file=$(echo ${lines[0]} | cut -d ' ' -f 3)
  [ -f "$file" ]
  # Ensure the file contains the correct text
  [ $(cat "$file") == "* Initial release." ]
  # Delete the file
  rm "$file"
}

@test "parse can parse latest changelog tag" {
  setup_changelog
  run ./chag parse $BATS_TMPDIR/test-changelog
  delete_changelog
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "0.0.2 2014-08-10 /") -ne 0 ]
  file=$(echo ${lines[0]} | cut -d ' ' -f 3)
  [ -f "$file" ]
  [ $(cat "$file") == '* Correcting ``--debug`` description.' ]
  rm "$file"
}
