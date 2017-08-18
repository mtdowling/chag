#!/usr/bin/env bats

@test "no arguments prints usage instructions" {
  run ./chag
  [ $status -eq 0 ]
  [ $(expr "${lines[1]}" : "Usage:") -ne 0 ]
}

@test "--version prints version number" {
  run ./chag --version
  [ $status -eq 0 ]
  [ $(expr "$output" : "chag [0-9][0-9.]*") -ne 0 ]
}

@test "--help prints help" {
  run ./chag --help
  [ $status -eq 0 ]
  [ "${#lines[@]}" -gt 3 ]
}

@test "Invalid options fail" {
  run ./chag contents --foo
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] Unknown option '--foo'" ]
}

@test "Invalid commands fail" {
  run ./chag foo
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] Available commands: contents|tag|latest|entries|update|entry|next|create" ]
}
