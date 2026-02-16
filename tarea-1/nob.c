#define NOB_IMPLEMENTATION
#include "nob.h"

#define BUILD_FOLDER "build/"
#define SRC_FOLDER "src/"

int main(int argc, char **argv) {
    NOB_GO_REBUILD_URSELF(argc, argv);

    if (!nob_mkdir_if_not_exists(BUILD_FOLDER))
        return 1;
    Nob_Cmd cmd = {0};

    // On POSIX
    nob_cmd_append(&cmd, "gcc", "-Wall", "-Wextra", "-g", "-O0", "-o",
                   BUILD_FOLDER "automata", SRC_FOLDER "main.c");

    if (!nob_cmd_run(&cmd))
        return 1;

    return 0;
}
