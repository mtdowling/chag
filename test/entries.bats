#!/usr/bin/env bats

load test_helper

@test "--help prints help" {
  run ./chag entries --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag entries") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag entries --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "lists tag versions from changelog" {
  setup_changelog
  run ./chag entries --file $CHNGFILE
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "0.0.2" ]
  [ "${lines[1]}" == "0.0.1" ]
}
