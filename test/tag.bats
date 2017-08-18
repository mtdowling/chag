#!/usr/bin/env bats

load test_helper

chagcmd="$BATS_TEST_DIRNAME/../chag"

@test "--help prints tag help" {
  run ./chag tag --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag tag") -ne 0 ]
}

@test "tag ensures FILENAME exists" {
  run ./chag tag --file /path/to/does/not/exist 0.0.1
  [ $status -eq 1 ]
  [ "${lines[0]}" == "[FAILURE] File not found: /path/to/does/not/exist" ]
}

@test "Tags debug output" {
  setup_repo
  run $chagcmd tag --file CHANGELOG.md
  [ $status -eq 0 ]
  [ "${lines[0]}" == 'Tagging 0.0.2 with the following annotation:' ]
  [ "${lines[1]}" == '===[ BEGIN ]===' ]
  [ "${lines[2]}" == '* Correcting ``--debug`` description.' ]
  [ "${lines[3]}" == '===[  END  ]===' ]
  [ "${lines[4]}" == 'Running git command: git tag -a --cleanup=whitespace -F - 0.0.2' ]
  [ "${lines[5]}" == '[SUCCESS] Tagged 0.0.2' ]
  run git tag -l -n1 0.0.2
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == '0.0.2           * Correcting ``--debug`` description.' ]
  delete_repo
}

@test "Can force a tag" {
  setup_repo
  run $chagcmd tag --file CHANGELOG.md 0.0.2
  [ $status -eq 0 ]
  run $chagcmd tag --force --file CHANGELOG.md --tag 0.0.2
  [ $status -eq 0 ]
  [ "${lines[5]}" == '[SUCCESS] Tagged 0.0.2' ]
  cd -
  delete_repo
}
