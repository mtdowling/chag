#!/usr/bin/env bats

load test_helper

@test "--help prints help" {
  run ./chag create --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag create") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag create --foo
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] Unknown option '--foo'" ]
}
