#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
//#include <mutex>

#define serial_baud 115200

static bool logger_initialized = false;
//static std::mutex lock;

static void init_logger()
{
//    std::lock (lock);
    if(!logger_initialized) {
        Serial.begin(serial_baud);
        logger_initialized = true;
    }
//    lock.unlock();
}

static void verify_init()
{
    if(!logger_initialized)
        init_logger();
}

static int get_total_length_with_args(const char* msg, va_list args)
{
    va_list argclone;
    va_copy(argclone, args);
    int len = vsnprintf(0, 0, msg, argclone);
    va_end(argclone);
    return (len + 1);
}

static char* generate_str_from_args(const char* msg, va_list args)
{
    int len = get_total_length_with_args(msg, args);
    char* full_message = (char*)malloc(sizeof(char)*(len + 1));
    vsnprintf(full_message, len, msg, args);
    full_message[len] = '\0';

    return full_message;
}

void log_info (const char* msg, ...)
{
    if (NULL == msg)
        return;

    verify_init();

    va_list args;
    va_start(args, msg);

    char* full_msg = generate_str_from_args(msg, args);
    Serial.println(full_msg);
    free(full_msg);

    va_end(args);
}
