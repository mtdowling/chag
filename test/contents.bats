#!/usr/bin/env bats

load test_helper

@test "--help prints contents help" {
  run ./chag contents --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag contents") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag contents --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "contents ensures FILENAME exists" {
  run ./chag contents --file /path/to/does/not/exist
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "contents ensures the tag exists" {
  setup_changelog
  run ./chag contents --file $CHNGFILE --tag 9.9.9
  delete_changelog
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] Tag not found" ]
}

@test "contents can contents a tag" {
  setup_changelog
  run ./chag contents --file $CHNGFILE --tag 0.0.1
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "* Initial release." ]
}

@test "contents can contents the latest tag" {
  setup_changelog
  run ./chag contents --file $CHNGFILE
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == '* Correcting ``--debug`` description.' ]
}
