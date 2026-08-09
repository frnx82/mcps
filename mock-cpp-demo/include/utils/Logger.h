#pragma once
/**
 * @file Logger.h
 * @brief Thread-safe logging for the CAE solver.
 */

#include <string>
#include <iostream>
#include <sstream>
#include <mutex>
#include <chrono>
#include <ctime>

namespace cae {

enum class LogLevel { DEBUG, INFO, WARN, ERROR };

class Logger {
public:
    static Logger& instance() {
        static Logger logger;
        return logger;
    }

    void setLevel(LogLevel level) { m_level = level; }

    template<typename... Args>
    void log(LogLevel level, const std::string& fmt, Args&&... args) {
        if (level < m_level) return;
        std::lock_guard<std::mutex> lock(m_mutex);

        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        char time_buf[32];
        std::strftime(time_buf, sizeof(time_buf), "%H:%M:%S", std::localtime(&time));

        const char* level_str[] = {"DEBUG", "INFO ", "WARN ", "ERROR"};
        std::cout << "[" << time_buf << "] "
                  << level_str[static_cast<int>(level)] << " "
                  << format(fmt, std::forward<Args>(args)...) << "\n";
    }

private:
    Logger() = default;
    LogLevel m_level = LogLevel::INFO;
    std::mutex m_mutex;

    // Simple {} format replacement
    std::string format(const std::string& fmt) { return fmt; }

    template<typename T, typename... Args>
    std::string format(const std::string& fmt, T&& val, Args&&... args) {
        auto pos = fmt.find("{}");
        if (pos == std::string::npos) return fmt;
        std::ostringstream oss;
        oss << val;
        return fmt.substr(0, pos) + oss.str()
             + format(fmt.substr(pos + 2), std::forward<Args>(args)...);
    }
};

#define LOG_DEBUG(...) cae::Logger::instance().log(cae::LogLevel::DEBUG, __VA_ARGS__)
#define LOG_INFO(...)  cae::Logger::instance().log(cae::LogLevel::INFO,  __VA_ARGS__)
#define LOG_WARN(...)  cae::Logger::instance().log(cae::LogLevel::WARN,  __VA_ARGS__)
#define LOG_ERROR(...) cae::Logger::instance().log(cae::LogLevel::ERROR, __VA_ARGS__)

} // namespace cae
