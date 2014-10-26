#!/usr/bin/env bats

load test_helper

@test "--help prints parse help" {
  run ./chag parse --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag parse") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag parse --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "parse requires a FILENAME" {
  run ./chag parse
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* parse requires a FILENAME") -ne 0 ]
}

@test "parse ensures FILENAME exists" {
  run ./chag parse /path/to/does/not/exist
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "parse requires a TAG" {
  setup_changelog
  run ./chag parse $CHNGFILE
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* parse requires a TAG") -ne 0 ]
  delete_changelog
}

@test "parse ensures the tag exists" {
  setup_changelog
  run ./chag parse $CHNGFILE 9.9.9
  delete_changelog
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Tag 9.9.9 not found") -ne 0 ]
}

@test "parse can parse a tag" {
  setup_changelog
  run ./chag parse $CHNGFILE 0.0.1
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "* Initial release." ]
}

@test "parse can parse the latest tag" {
  setup_changelog
  run ./chag parse $CHNGFILE latest
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == '* Correcting ``--debug`` description.' ]
}
