#!/usr/bin/env bats

load test_helper

@test "--help prints help" {
  run ./chag latest --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag latest") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag latest --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "latest shows latest tag" {
  setup_changelog
  run ./chag latest --file $CHNGFILE
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "0.0.2" ]
}
