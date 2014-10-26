#!/usr/bin/env bats

load test_helper

@test "--help prints update help" {
  run ./chag update --help
  [ $status -eq 0 ]
  [ $(expr "${lines[0]}" : "Usage: chag update") -ne 0 ]
}

@test "Invalid options fail" {
  run ./chag update --foo
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "Unknown option") -ne 0 ]
}

@test "update requires a FILENAME" {
  run ./chag update
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* update requires a FILENAME") -ne 0 ]
}

@test "update ensures FILENAME exists" {
  run ./chag update /path/to/does/not/exist
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "File not found: /path/to/does/not/exist") -ne 0 ]
}

@test "update requires a TAG" {
  setup_changelog
  run ./chag update $CHNGFILE
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : ".* update requires a TAG") -ne 0 ]
  delete_changelog
}

@test "update ensures TBD exists" {
  setup_changelog
  run ./chag update $CHNGFILE 9.9.9
  delete_changelog
  [ $status -eq 1 ]
  [ $(expr "${lines[0]}" : "'Next Release (TBD)' not found in .*") -ne 0 ]
}

@test "updates inline" {
  setup_changelog_tbd
  run ./chag update $CHNGFILE 9.9.9
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "[SUCCESS] Updated ${CHNGFILE}:3 to '9.9.9'" ]
}

@test "updates inline with date" {
  setup_changelog_tbd
  run ./chag update --date 2014-08-09 $CHNGFILE 9.9.9
  [ "$(sed "3q;d" $CHNGFILE)" == "9.9.9 (2014-08-09)" ]
  [ "$(sed "4q;d" $CHNGFILE)" == "------------------" ]
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "[SUCCESS] Updated ${CHNGFILE}:3 to '9.9.9 (2014-08-09)'" ]
}

@test "updates inline with automatic date" {
  setup_changelog_tbd
  run ./chag update --date 1 $CHNGFILE 9.9.9
  d=$(date +%Y-%m-%d)
  [ "$(sed "3q;d" $CHNGFILE)" == "9.9.9 (${d})" ]
  [ "$(sed "4q;d" $CHNGFILE)" == "------------------" ]
  delete_changelog
  [ $status -eq 0 ]
  [ "${lines[0]}" == "[SUCCESS] Updated ${CHNGFILE}:3 to '9.9.9 (${d})'" ]
}
