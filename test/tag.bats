#!/usr/bin/env bats

# Deletes the test fixture repository
delete_repo() {
  rm -rf $BATS_TMPDIR/chag-test
}

# Creates a test fixture repository
setup_repo() {
  delete_repo
  # Create new git repo
  mkdir -p $BATS_TMPDIR/chag-test
  tail -9 CHANGELOG.rst > $BATS_TMPDIR/chag-test/CHANGELOG.rst
  cd $BATS_TMPDIR/chag-test
  git init && git add -A && git commit -m 'Initial commit'
}

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
  run ./chag tag /path/to/does/not/exist
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "tag ensures parse succeeds" {
  run ./chag tag --tag 999.999.999 CHANGELOG.rst
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Failed to parse") -ne 0 ]
}

@test "Tags with annotation and specific tag" {
  setup_repo
  run $chagcmd tag --add-v CHANGELOG.rst
  [ $status -eq 0 ]
  [ "${lines[0]}" == '[SUCCESS] Tagged the v0.0.2 release' ]
  run git tag -l -n1 v0.0.2
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == 'v0.0.2          * Correcting ``--debug`` description.' ]
  delete_repo
}

@test "Tags with annotation and latest tag" {
  setup_repo
  run $chagcmd tag --debug --tag 0.0.1 CHANGELOG.rst
  [ $status -eq 0 ]
  [ "${lines[0]}" == 'Parsed the 0.0.1 changelog entry from CHANGELOG.rst:' ]
  [ $(expr "${lines[1]}" : '  tag: 0.0.1, date: 2014-08-10, tmpfile: *') -ne 0 ]
  [ $(expr "${lines[2]}" : 'Running git tag   -a -F *') -ne 0 ]
  [ "${lines[3]}" == '[SUCCESS] Tagged the 0.0.1 release' ]
  run git tag -l -n1 0.0.1
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == '0.0.1           * Initial release.' ]
  delete_repo
}

@test "Can force a tag" {
  setup_repo
  run $chagcmd tag CHANGELOG.rst
  [ $status -eq 0 ]
  run $chagcmd tag --force CHANGELOG.rst
  [ $status -eq 0 ]
  [ "${lines[0]}" == '[SUCCESS] Tagged the 0.0.2 release' ]
  cd -
  delete_repo
}

@test "Can prepend a message to a tag" {
  setup_repo
  run $chagcmd tag --message 'Testing' CHANGELOG.rst
  [ $status -eq 0 ]
  [ "${lines[0]}" == '[SUCCESS] Tagged the 0.0.2 release' ]
  run git tag -l -n1 0.0.2
  cd -
  [ $status -eq 0 ]
  [ "${lines[0]}" == '0.0.2           Testing' ]
  cd -
  delete_repo
}
