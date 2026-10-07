#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_ARGS 128

static int wait_child(pid_t pid)
{
    int status;
    while (waitpid(pid, &status, 0) < 0) {
        if (errno == EINTR) continue;
        perror("waitpid");
        return 1;
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}

/* Return -1 for external commands; builtins run in the shell process. */
static int builtin(char **a, int *quit)
{
    if (!strcmp(a[0], "exit")) {
        if (a[1]) { fprintf(stderr, "exit: no arguments supported\n"); return 2; }
        *quit = 1;
        return 0;
    }
    if (!strcmp(a[0], "cd")) {
        if (a[1] && a[2]) { fprintf(stderr, "cd: expected zero or one path\n"); return 2; }
        const char *path = a[1] ? a[1] : getenv("HOME");
        if (!path) { fprintf(stderr, "cd: HOME is not set\n"); return 1; }
        /* Must execute in parent, so future commands inherit the new cwd. */
        if (chdir(path) < 0) { perror("cd"); return 1; }
        return 0;
    }
    if (!strcmp(a[0], "pwd")) {
        if (a[1]) { fprintf(stderr, "pwd: no arguments supported\n"); return 2; }
        char *cwd = getcwd(NULL, 0);
        if (!cwd) { perror("pwd"); return 1; }
        int failed = puts(cwd) == EOF;
        free(cwd);
        if (failed) { perror("pwd"); return 1; }
        return 0;
    }
    if (!strcmp(a[0], "echo")) {
        /* Intentionally literal: no -n option and no backslash escapes. */
        for (size_t i = 1; a[i]; ++i) {
            if ((i > 1 && putchar(' ') == EOF) || fputs(a[i], stdout) == EOF) {
                perror("echo"); return 1;
            }
        }
        if (putchar('\n') == EOF) { perror("echo"); return 1; }
        return 0;
    }
    if (!strcmp(a[0], "cat")) {
        int result = 0;
        for (size_t i = 1; i == 1 || a[i]; ++i) {
            int fd = a[i] ? open(a[i], O_RDONLY) : STDIN_FILENO;
            if (fd < 0) { perror(a[i]); result = 1; continue; }
            char buffer[8192];
            for (;;) {
                ssize_t n = read(fd, buffer, sizeof(buffer));
                if (n < 0 && errno == EINTR) continue;
                if (n < 0) { perror("cat: read"); result = 1; break; }
                if (!n) break;
                ssize_t offset = 0;
                while (offset < n) {
                    ssize_t w = write(STDOUT_FILENO, buffer + offset, (size_t)(n - offset));
                    if (w < 0 && errno == EINTR) continue;
                    if (w <= 0) { perror("cat: write"); result = 1; break; }
                    offset += w;
                }
                if (offset < n) break;
            }
            if (a[i] && close(fd) < 0) { perror("cat: close"); result = 1; }
            if (!a[i]) break;
        }
        return result;
    }
    if (!strcmp(a[0], "touch")) {
        if (!a[1]) { fprintf(stderr, "touch: expected file(s)\n"); return 2; }
        int result = 0;
        for (size_t i = 1; a[i]; ++i) {
            /* Create if absent; preserve existing bytes (no O_TRUNC). */
            int fd = open(a[i], O_WRONLY | O_CREAT, 0666);
            if (fd < 0) { perror(a[i]); result = 1; continue; }
            if (close(fd) < 0) { perror("touch: close"); result = 1; }
        }
        return result;
    }
    if (!strcmp(a[0], "rm")) {
        if (!a[1]) { fprintf(stderr, "rm: expected file(s)\n"); return 2; }
        int result = 0;
        for (size_t i = 1; a[i]; ++i) {
            if (unlink(a[i]) < 0) { perror(a[i]); result = 1; }
        }
        return result;
    }
    return -1;
}

static int execute(char **a, int *quit)
{
    int result = builtin(a, quit);
    if (result >= 0) return result;
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }
    if (pid == 0) {
        execvp(a[0], a);
        int code = errno == ENOENT ? 127 : 126;
        perror(a[0]);
        _exit(code); /* No duplicate flushing of inherited stdio buffers. */
    }
    return wait_child(pid);
}


#define MAX_TOKENS 256
#define MAX_LINE 65536

typedef struct {
    char *text;
    int kind; /* 0=word, '<', '>', 'A'=append, '|' */
} Token;

typedef struct {
    char *args[MAX_ARGS];
    const char *input, *output;
    int append;
} Command;

static void free_tokens(Token *tokens, size_t n)
{
    for (size_t i = 0; i < n; ++i) free(tokens[i].text);
}

static int lex(const char *line, Token *tokens, size_t *n)
{
    *n = 0;
    const char *p = line;
    while (*p) {
        if (strchr(" \t\r\n", *p)) { ++p; continue; }
        if (*n == MAX_TOKENS) { fprintf(stderr, "parse: too many tokens\n"); return 2; }
        if (strchr("\"'\\;&", *p)) {
            fprintf(stderr, "parse: quotes, escapes, ; and & are unsupported\n"); return 2;
        }
        int kind = 0;
        const char *start = p;
        if (strchr("<>|", *p)) {
            kind = *p++;
            if (kind == '>' && *p == '>') { kind = 'A'; ++p; }
        } else {
            while (*p && !strchr(" \t\r\n<>|\"'\\;&", *p)) ++p;
        }
        char *word = strndup(start, (size_t)(p - start));
        if (!word) { perror("strndup"); return 1; }
        if (!kind && (!strcmp(word, "$HOME") || !strcmp(word, "$PATH"))) {
            const char *value = getenv(word + 1);
            free(word);
            word = strdup(value ? value : "");
            if (!word) { perror("strdup"); return 1; }
        }
        tokens[*n] = (Token){word, kind};
        ++*n;
    }
    return 0;
}

static int parse(Token *tokens, size_t n, Command *cmd)
{
    size_t argc = 0;
    memset(cmd, 0, sizeof(*cmd));
    for (size_t i = 0; i < n; ++i) {
        int kind = tokens[i].kind;
        if (!kind) {
            if (argc == MAX_ARGS - 1) goto syntax;
            cmd->args[argc++] = tokens[i].text;
        } else {
            if (kind == '|' || i + 1 == n || tokens[i + 1].kind) goto syntax;
            const char *path = tokens[++i].text;
            if (kind == '<') {
                if (cmd->input) goto syntax;
                cmd->input = path;
            } else {
                if (cmd->output) goto syntax;
                cmd->output = path;
                cmd->append = kind == 'A';
            }
        }
    }
    if (!argc) goto syntax;
    return 0;
syntax:
    fprintf(stderr, "parse: invalid syntax, duplicate redirection or too many arguments\n");
    return 2;
}

static int redirect(const Command *cmd)
{
    for (int target = 0; target <= 1; ++target) {
        const char *path = target ? cmd->output : cmd->input;
        if (!path) continue;
        int flags = target ? O_WRONLY | O_CREAT | (cmd->append ? O_APPEND : O_TRUNC) : O_RDONLY;
        int fd = open(path, flags, 0666);
        if (fd < 0) { perror(path); return 1; }
        if (fd != target) {
            if (dup2(fd, target) < 0) { perror("dup2"); close(fd); return 1; }
            if (close(fd) < 0) { perror("close"); return 1; }
        }
    }
    return 0;
}

static int run_command(const Command *cmd, int *quit)
{
    int saved[2] = {-1, -1}, result = 1;
    /* Save only changed fds. CLOEXEC prevents leaking backup fds to external programs. */
    for (int i = 0; i < 2; ++i) {
        if (!(i ? cmd->output : cmd->input)) continue;
        saved[i] = fcntl(i, F_DUPFD_CLOEXEC, 3);
        if (saved[i] < 0) { perror("fcntl: save fd"); goto restore; }
    }
    if (redirect(cmd)) goto restore;
    result = execute((char **)cmd->args, quit);
    if (fflush(stdout) == EOF) { perror("stdout"); clearerr(stdout); result = 1; }
restore:
    for (int i = 0; i < 2; ++i) {
        if (saved[i] < 0) continue;
        if (dup2(saved[i], i) < 0) { perror("dup2: restore"); result = 1; *quit = 1; }
        if (close(saved[i]) < 0) { perror("close: saved fd"); result = 1; }
    }
    clearerr(stdin);
    return result;
}

/* Pipeline builtins run in children: cd/exit affect only their pipeline side. */
static void pipeline_child(const Command *cmd, int read_end, int write_end, int side)
{
    int fd = side == 0 ? write_end : read_end;
    int target = side == 0 ? STDOUT_FILENO : STDIN_FILENO;
    if (dup2(fd, target) < 0) { perror("dup2: pipe"); _exit(1); }
    if (close(read_end) < 0 || close(write_end) < 0) { perror("close: pipe"); _exit(1); }
    /* Explicit redirection overrides this side's pipe connection. */
    if (redirect(cmd)) _exit(1);
    int quit = 0;
    int result = builtin((char **)cmd->args, &quit);
    if (result >= 0) {
        if (fflush(stdout) == EOF) { perror("stdout"); result = 1; }
        _exit(result);
    }
    execvp(cmd->args[0], cmd->args);
    int code = errno == ENOENT ? 127 : 126;
    perror(cmd->args[0]);
    _exit(code);
}

static int run_line(Token *tokens, size_t n, int *quit)
{
    size_t split = n;
    for (size_t i = 0; i < n; ++i) {
        if (tokens[i].kind != '|') continue;
        if (split != n) { fprintf(stderr, "parse: only one pipe supported\n"); return 2; }
        split = i;
    }
    Command left, right;
    int result = parse(tokens, split, &left);
    if (result) return result;
    if (split == n) return run_command(&left, quit);
    result = parse(tokens + split + 1, n - split - 1, &right);
    if (result) return result;
    int fds[2];
    if (pipe(fds) < 0) { perror("pipe"); return 1; }
    pid_t first = fork();
    if (first == 0) pipeline_child(&left, fds[0], fds[1], 0);
    if (first < 0) { perror("fork"); close(fds[0]); close(fds[1]); return 1; }
    pid_t second = fork();
    if (second == 0) pipeline_child(&right, fds[0], fds[1], 1);
    /* Parent owns neither endpoint. Keeping a writer open prevents EOF. */
    int close_error = 0;
    if (close(fds[0]) < 0) { perror("close: pipe read"); close_error = 1; }
    if (close(fds[1]) < 0) { perror("close: pipe write"); close_error = 1; }
    if (second < 0) {
        perror("fork"); wait_child(first); return 1;
    }
    /* Both children must exist before waiting, otherwise large output can deadlock. */
    wait_child(first);
    result = wait_child(second);
    return close_error ? 1 : result;
}

int main(void)
{
    /* Inherit caller environment; use documented defaults only if absent. */
    if ((!getenv("HOME") && setenv("HOME", "/", 1) < 0) ||
        (!getenv("PATH") && setenv("PATH", "/usr/bin:/bin", 1) < 0)) {
        perror("setenv"); return 1;
    }
    /* No stdio read-ahead: cat/external commands may consume the same fd 0. */
    if (setvbuf(stdin, NULL, _IONBF, 0) != 0) {
        fprintf(stderr, "setvbuf failed\n"); return 1;
    }
    char *line = NULL;
    size_t capacity = 0;
    int quit = 0, result = 0;
    while (!quit) {
        if (isatty(STDIN_FILENO)) {
            fputs("[OS-LAB1] myshell$ ", stderr);
            fflush(stderr);
        }
        if (getline(&line, &capacity, stdin) < 0) {
            if (ferror(stdin)) { perror("getline"); result = 1; }
            break;
        }
        if (strlen(line) > MAX_LINE) {
            fprintf(stderr, "parse: line too long\n"); result = 2; continue;
        }
        Token tokens[MAX_TOKENS];
        size_t n = 0;
        result = lex(line, tokens, &n);
        if (!result && n) {
            result = run_line(tokens, n, &quit);
        }
        free_tokens(tokens, n);
        /* Commit builtin output before a later fork or descriptor change. */
        if (fflush(stdout) == EOF) { perror("stdout"); result = 1; clearerr(stdout); }
    }
    free(line);
    return result;
}
