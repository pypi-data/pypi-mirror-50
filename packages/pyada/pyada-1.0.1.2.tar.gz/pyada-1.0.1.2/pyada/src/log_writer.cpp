//
// Created by tadeze on 8/25/17.
//

#include "log_writer.hpp"

void Log::LogMsg(const std::string &msg) {
    static Log L;
    L.logMsg(msg);
}