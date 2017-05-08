## Provider filename checker

This repository helps determine how different online storage providers handle different filenames. Rather than relying 
on fickle documentation, it relies on empirical metrics.

For the initial version, it uploads files through waterbutler and checks the response payload. This allows us to 
simplify code around authentication and credential management, but it means that any errors could be due to the 
waterbutler layer rather than provider-specific rules. 

Future versions will make raw API requests with a custom per-provider abstraction.

This repository provides very limited multi-storage-provider abstractions, but in general does not attempt to handle 
edge cases or a broad range of functionality. Do not use this code in production environments.

## TODO
- [x] Allow querying all providers via Waterbutler
- [~] Per provider abstractions without going through Waterbutler
- [x] Support checking folder + filename in same folder
  - [x] Requirement: annotate which providers totally disallow subfolders 
- [ ] Fix box provider (unhelpful 400 errors)
- Add "get metadata" feature to verify uploaded filenames for certain providers
  - [ ] Fix owncloud to return provider metadata
  - [ ] Evaluate Amazon s3 metadata + other notes
  - [ ] Dataverse
