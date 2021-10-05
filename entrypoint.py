#!/usr/bin/env python3

import sys
import git
import os
from github import Github

DEFAULT_MESSAGE = "Hey, I Tried to Merge with Master, but encountered a merge conflict. Can you please resolve it? I am taking off the label in the meanwhile. Please put the label back on when I should try again! And Have a Great Day!"
POSSIBLE_TRUE = ['true', '1', 't', 'y', 'yes', 'si', 'yeah',
                 'yup', 'certainly', 'uh-huh', 'hell-yeah', 'why-not', 'sure']


def strToBoolean(s):
    global POSSIBLE_TRUE
    return s.lower() in POSSIBLE_TRUE


def getParameters():
    global DEFAULT_MESSAGE
    labelToCheck = sys.argv[1]
    githubToken = sys.argv[2]
    messageForPr = sys.argv[3] if sys.argv[3] else DEFAULT_MESSAGE
    removeLabel = strToBoolean(
        sys.argv[4]) if sys.argv[4] else True
    gpgKey = sys.argv[5] if sys.argv[5] else None
    return (labelToCheck, githubToken, messageForPr, removeLabel, gpgKey)


def safelyApplyUpdate(repo, destBranch, srcBranch="master"):
    repo.git.checkout(destBranch)
    repo.git.merge(srcBranch)
    # Todo: Check for Merge Conflicts
    repo.git.push()
    repo.git.reset("--hard")
    repo.git.checkout(srcBranch)  # Always End on original Branch
    return 0


def checkoutAndPullBranchName(repo, branchName="master"):
    # Checkouts the Branch Name to Make sure We have it locally
    repo.git.checkout(branchName)
    # Pulls it to make sure we got the latest change in our branch
    repo.git.pull()


def attemptToSyncBranch(repo, gh, pull):
    prBranchName = pull.head.ref
    print("Attempting to merge into " + prBranchName)
    result = safelyApplyUpdate(repo, prBranchName)
    if (result == 0):
        # Success
        print("Successful Sync")
    else:
        print("Failed to Sync")


def getAllPRsBranchNamesThatHaveLabel(repo, gh, labelToCheck):
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]
    ourRepo = None
    for ghrepo in gh.get_user().get_repos():
        if (repo_name in ghrepo.name):
            # Todo: FIX this logic. This is sad
            ourRepo = ghrepo

    if (ourRepo == None):
        return "Failed to find Repo"

    pulls = ourRepo.get_pulls(state='open', sort='created', base='master')
    for pull in pulls:
        labels = pull.labels
        for label in labels:
            if (label.name == labelToCheck):
                attemptToSyncBranch(repo, gh, pull)


def getCurrentRepoInformation(repo):

    print(repo.git.status())


if __name__ == "__main__":
    # Rename these variables to something meaningful
    (labelToCheck, githubToken, messageForPr,
     removeLabel, gpgKey) = getParameters()

    runningVerification = (gpgKey != None)  # For Signing Commits Later

    repo = git.Repo(".")
    gh = Github(githubToken)

    getCurrentRepoInformation(repo)
    # Make sure we have the latest changes locally
    checkoutAndPullBranchName(repo)

    getAllPRsBranchNamesThatHaveLabel(repo, gh, labelToCheck)
