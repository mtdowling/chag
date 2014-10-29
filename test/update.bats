#!/usr/bin/env bats

load test_helper

@test "--help prints update help" {
  run ./chag update --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag update") -ne 0 ]
}

@test "update requires a TAG" {
  run ./chag update
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* update requires a TAG") -ne 0 ]
}

@test "update ensures FILENAME exists" {
  run ./chag update --file /path/to/does/not/exist FOO
  [ $status -eq 1 ]
  [ "${lines[0]}" ==  "[FAILURE] File not found: /path/to/does/not/exist" ]
}

@test "updates inline" {
  setup_changelog_tbd
  run ./chag update --file $CHNGFILE 9.9.9
  [ $status -eq 0 ]
  delete_changelog
  date=$(date +%Y-%m-%d)
  [ "${lines[0]}" == "[SUCCESS] Updated ${CHNGFILE} with 9.9.9" ]
}
