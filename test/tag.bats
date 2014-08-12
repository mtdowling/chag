#!/usr/bin/env bats

load test_helper

chagcmd="$BATS_TEST_DIRNAME/../chag"

@test "--help prints tag help" {
  run ./chag tag --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag tag") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag tag --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "ERROR: Unknown option") -ne 0 ]
}

@test "tag requires a FILENAME" {
  run ./chag tag
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "tag requires a FILENAME") -ne 0 ]
}

@test "tag ensures FILENAME exists" {
  run ./chag tag /path/to/does/not/exist 0.0.1
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "tag ensures parse succeeds" {
  run ./chag tag CHANGELOG.rst 999.999.999
  [ $status -eq 1 ]
  [ "${lines[0]}" == "Tag 999.999.999 not found in CHANGELOG.rst" ]
}

@test "Tags with annotation and specific tag" {
  setup_repo
  run $chagcmd tag --add-v CHANGELOG.rst 0.0.1
  [ $status -eq 0 ]
  [ "${lines[0]}" == '[SUCCESS] Tagged v0.0.1' ]
  run git tag -l -n1 v0.0.1
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == 'v0.0.1          * Initial release.' ]
  delete_repo
}

@test "Tags with annotation and latest tag" {
  setup_repo
  run $chagcmd tag --debug CHANGELOG.rst latest
  [ $status -eq 0 ]
  [ "${lines[0]}" == 'Tagging 0.0.2 with the following annotation:' ]
  [ "${lines[1]}" == '===[ BEGIN ]===' ]
  [ "${lines[2]}" == '* Correcting ``--debug`` description.' ]
  [ "${lines[3]}" == '===[  END  ]===' ]
  [ "${lines[4]}" == 'Running git command: git tag   -a -F - 0.0.2' ]
  [ "${lines[5]}" == '[SUCCESS] Tagged 0.0.2' ]
  run git tag -l -n1 0.0.2
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == '0.0.2           * Correcting ``--debug`` description.' ]
  delete_repo
}

@test "Can force a tag" {
  setup_repo
  run $chagcmd tag CHANGELOG.rst 0.0.2
  [ $status -eq 0 ]
  run $chagcmd tag --force CHANGELOG.rst 0.0.2
  [ $status -eq 0 ]
  [ "${lines[0]}" == '[SUCCESS] Tagged 0.0.2' ]
  cd -
  delete_repo
}
