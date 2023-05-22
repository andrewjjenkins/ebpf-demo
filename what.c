#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#define MAX_PRIME 175000
#define NUM_WORKERS 16
#define NUM_RUNS 10000

static pid_t pids[NUM_WORKERS];
char **argvZero = NULL;
int verbose = 0;
int runsCompleted = 0;

void doWork() {
    uint64_t i, num, primes = 0;
    for (num = 1; num <= MAX_PRIME; num ++) {
        uint64_t largestTrialFactor = (uint64_t)(sqrt((double) num)) + 2;
        for (i = 2; (i <= largestTrialFactor) && (num % i != 0); i++) {
            if (i == largestTrialFactor) {
                ++primes;
            }
        }
    }
    if (verbose) {
        printf("[%d] found %ld primes between 1 and %d\n", getpid(), primes, MAX_PRIME);
    }
}

char newName[16];
void chooseNewName() {
    for (int j = 0; j < 15; j++) {
        newName[j] = 'a' + (random() % 26);
    }
    newName[0] = '/';
    newName[1] = 'b';
    newName[2] = 'i';
    newName[3] = 'n';
    newName[4] = '/';
    newName[15] = '\0';
}

void spawnChild(int i) {
    chooseNewName();

    pids[i] = fork();
    if (pids[i] == 0) {
        strcpy(*argvZero, newName);
        if (verbose) {
            printf("[%d] new child\n", getpid());
        }
        doWork();
        exit(0);
    } else if (pids[i] < 0) {
        perror("fork");
        exit(1);
    } else {
        if (verbose) {
            printf("[%d] forked new child: %d\n", getpid(), pids[i]);
        }
    }
}

void sigchld_handler(int childPid, siginfo_t *childInfo, void *) {
    fflush(stdout);

    if (waitpid(childInfo->si_pid, NULL, 0) < 0) {
        perror("waitpid");
        exit(1);
    }

    ++runsCompleted;
    if (runsCompleted >= NUM_RUNS) {
        exit(0);
    }

    for (int i = 0; i < NUM_WORKERS; ++i) {
        if (pids[i] != childInfo->si_pid) {
            continue;
        }
        spawnChild(i);
    }
}

int main(int argc, char *argv[]) {
    int c;
    argvZero = &argv[0];

    opterr = 0;
    while ((c = getopt(argc, argv, "v")) != -1) {
        switch (c) {
            case 'v':
                verbose = 1;
                break;
            case '?':
                if (isprint (optopt)) {
                    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
                } else {
                    fprintf (stderr,
                            "Unknown option character `\\x%x'.\n",
                            optopt);
                }
                return 1;
            default:
                abort ();
        }
    }

    struct sigaction sa_chld;
    bzero(&sa_chld, sizeof(sa_chld));
    sa_chld.sa_flags = SA_SIGINFO;
    sa_chld.sa_sigaction = sigchld_handler;
    sigemptyset(&sa_chld.sa_mask);
    if (sigaction(SIGCHLD, &sa_chld, NULL) < 0) {
        perror("sigaction");
        exit(1);
    }

    for (int i = 0; i < NUM_WORKERS; ++i) {
        spawnChild(i);
    }

    while(1) {
        usleep(100000);
        if (runsCompleted >= NUM_RUNS) {
            return 0;
        }
    }

    return 1;
}

