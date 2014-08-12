#!/usr/bin/env bats

load test_helper

@test "--help prints help" {
  run ./chag list --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag list") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag list --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "list requires a FILENAME" {
  run ./chag list
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* list requires a FILENAME") -ne 0 ]
}

@test "lists tag versions from changelog" {
  setup_changelog
  run ./chag list $CHNGFILE
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "0.0.2" ]
  [ "${lines[1]}" == "0.0.1" ]
}
