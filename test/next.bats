#!/usr/bin/env bats

load test_helper

@test "--help prints help" {
  run ./chag next --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag next") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag next --foo
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] Unknown option '--foo'" ]
}

@test "creates a next change log" {
  setup_changelog
  run ./chag next
  delete_changelog
  [ $status -eq 0 ]
}
