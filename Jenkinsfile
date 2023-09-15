#!groovy
library "JenkinsLib"

e2eRepo = 'vv-e2e-automation'
e2eBranch = common.getGitBranch()
libRepo = 'automation-lib'
libBranch = 'master'
totalRetries = 3
e2eGuests = 2

parameters = [
    string(defaultValue: 'https://application-integration.ship.virginvoyages.com/svc/', description: "Ship Link", name: 'shipLink', trim: true),
    string(defaultValue: 'https://int.gcpshore.virginvoyages.com/', description: "Shore Link", name: 'shoreLink', trim: true),
    booleanParam(name: 'isPromotion', defaultValue: false, description: 'is this Promotion Job'),
]

if (JOB_BASE_NAME.toLowerCase().contains('-branch')) {
    parameters += [
        string(defaultValue: 'master', description: "E2E Branch", name: 'E2EBranch', trim: true),
        string(defaultValue: 'master', description: "Lib Branch", name: 'LibBranch', trim: true),
    ]
}

properties([
    buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '500')),
    azureAdAuthorizationMatrix(common.azurePermissions([users: [], build: true, read: true])),
    parameters(parameters)
])

testBed = e2e.getTestBed(params.shoreLink)
env.TEAMS_CHANNEL = e2e.getChannelName(params.shipLink)

currentBuild.displayName = "$BUILD_NUMBER - ${testBed.toUpperCase()}"

userTriggered = common.getBuildUser()['email']

mentions = [userTriggered, 'ht.krishnakumara@decurtis.com']
description = [userTriggered.toUpperCase()]

if (params.containsKey('E2EBranch')) {
    if (params.E2EBranch != 'master') {
        description.add("E2E: $params.E2EBranch")
    }
    e2eBranch = params.E2EBranch
}

if (params.containsKey('LibBranch')) {
    if (params.LibBranch != 'master') {
        description.add("LIB: $params.LibBranch")
    }
    libBranch = params.LibBranch
}

currentBuild.description = description.unique().sort().join(" ")

pod.kubeNode(pod.ReturnContainers()) {
    if (params.containsKey('LibBranch') && libBranch != 'master') {
        stage('Setup Library') {
            libCommit = scmWrapper.gitClone([repoName: libRepo, branch: libBranch, clean: true, folder: true])
            dir (libRepo) {
                sh(returnStdout: true, script: "git rev-parse --short --verify HEAD").trim()
                sh '''
                    set +x
                    rm -rf /root/e2e-venv/lib/python3.8/site-packages/decurtis*
                    cp -pr $WORKSPACE/automation-lib/decurtis /root/e2e-venv/lib/python3.8/site-packages/
                '''
            }
        }
    }

    if (params.shoreLink.contains('developer.dxp-decurtis.com')) {
        cluster = 'developer'
    } else if (params.shoreLink.contains('qa1-shore.dxp-decurtis.com')) {
        cluster = 'qa1'
    } else if (params.shoreLink.contains('dc-shore.dxp-decurtis.com')) {
        cluster = 'prod'
    } else {
        cluster = 'dev'
    }

    e2eCommit = scmWrapper.gitClone([repoName: e2eRepo, branch: e2eBranch, clean: true, folder: true])
    dir(e2eRepo) {
        for (iter = 1; iter <= totalRetries; iter++) {
            pyTestParams = [
                "--ship=$params.shipLink",
                "--shore=$params.shoreLink",
                "--guests=$e2eGuests",
                "--test-rail"
            ]
            if (JOB_BASE_NAME.toLowerCase().contains('-branch')) {
                pyTestParams -=["--test-rail"]
            }
            stage("Running E2E $iter") {
                try {
                    python.RunPyTest([
                        pyTestParams: pyTestParams, pyTestsPath: 'test_scripts', allureReport: true,
                        reportName: "e2e-report-$iter", timeOut: 55, mentions: mentions, exitFirst: false,
                    ])
                    scmWrapper.StatusUpdate([
                        commit: e2eCommit, repoName: e2eRepo, message: "E2E Passed", status: 'SUCCESSFUL'
                    ])
                    if (params.containsKey('LibBranch') && libBranch != 'master') {
                        scmWrapper.StatusUpdate([
                            commit: libCommit, repoName: libRepo, message: "E2E Passed", status: 'SUCCESSFUL'
                        ])
                    }
                    log.Success("E2E has passed after $iter iterations :)")
                    iter = totalRetries + 1
                } catch (e) {
                    if (iter >= totalRetries) {
                        scmWrapper.StatusUpdate([
                            commit: e2eCommit, repoName: e2eRepo, message: "E2E Failed", status: 'FAILED'
                        ])
                        if (params.containsKey('LibBranch') && libBranch != 'master') {
                            scmWrapper.StatusUpdate([
                                commit: libCommit, repoName: libRepo, message: "E2E Failed", status: 'FAILED'
                            ])
                        }
                        log.Fail("E2E has failed after $totalRetries iterations :( $e.message")
                    } else {
                        log.Error("Stage: $STAGE_NAME failed, triggering next one :( $e.message")
                        
                    }
                }
            }
        }
    }
}
