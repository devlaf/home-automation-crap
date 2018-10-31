/*
 *  serial_logger.h
 *
 *  A simple logging library that logs to a serial connection.
 *
 */

#ifndef logger_h
#define logger_h

#include <stdarg.h>

void log_info (const char* msg, ...);

#endif
