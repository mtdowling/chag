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

@test "Creates changelog with appropriate header" {
  run ./chag create --file $CHNGFILE
  contents=`head -n 1 $CHNGFILE`
  delete_changelog
  [ $status -eq 0 ]
  [ "$contents" == "# CHANGELOG" ]
}
