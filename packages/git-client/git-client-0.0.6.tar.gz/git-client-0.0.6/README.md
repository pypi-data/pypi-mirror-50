# gc  
  
`gc` is a simple command line helper client for git.  
  
Obviously git has a lot of functionality in the CLI already. Not seeking to re-invent any wheels, `gc` can simplify commits and pushes, add or remove files from .gitignore, and maybe one day help with merge fixes.  
  
### usage  
  
`$ gc subject for a git commit`  
  
**Commit local git repo with message "subject for a git commit", add or rm files, and push changes.** You will be prompted to add a body message (skip with 'n'), and you will see a list of untracked, modified, or deleted files. Simply unselect any files you DON'T want to add or rm.  

