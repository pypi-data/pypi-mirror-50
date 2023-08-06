//
// Created by tadeze on 8/25/17.
//

#ifndef PYIFOREST_LOGWRITER_HPP
#define PYIFOREST_LOGWRITER_HPP
#include<string>
#include <fstream>
#include <memory>

namespace util {
    class LogWriter {
    private:
        std::ofstream logfile;

        LogWriter() {};
    public:
        virtual ~LogWriter() {};

        std::unique_ptr<LogWriter> create_instance();

        void open_log(std::string &filename);

        void close_log();

        void write(std::string &log);
    };

}
class Log
{
public:
    ~Log() {
        // closing file-descriptors, etc...
    }
    static void LogMsg( const std::string& msg );

private:
    Log() { }
    void logMsg( const std::string& msg ) {
        // do work
    }
};

#endif //PYIFOREST_LOGWRITER_HPP
