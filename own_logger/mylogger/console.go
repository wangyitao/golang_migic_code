package mylogger

import "fmt"

// ConsoleLogger 在终端写日志相关内容
type ConsoleLogger struct {
	Level LogLevel
}

// NewConsoleLogger 新建日志对象，构造函数
func NewConsoleLogger(levelStr string) ConsoleLogger {
	level, err := parseLogLevel(levelStr)
	if err != nil {
		panic(err)
	}
	return ConsoleLogger{
		Level: level,
	}
}

// 根据日志级别筛选输出日志
func (c ConsoleLogger) enable(logLevel LogLevel) bool {
	return c.Level <= logLevel
}

// 打印日志内容
func (c ConsoleLogger) log(lv LogLevel, format string, a ...interface{}) {
	if c.enable(lv) {
		msg := fmt.Sprintf(format, a...)
		funcName, fileName, lineNo := getInfo(3)
		fmt.Printf("[%s] [%s] [%s:%s:%d] %s\n", getNow(), getLogString(lv), fileName, funcName, lineNo, msg)
	}
}

// Debug 调试日志
func (c ConsoleLogger) Debug(format string, a ...interface{}) {
	c.log(DEBUG, format, a...)
}

// Info info日志
func (c ConsoleLogger) Info(format string, a ...interface{}) {
	c.log(INFO, format, a...)
}

// Warning warning日志
func (c ConsoleLogger) Warning(format string, a ...interface{}) {
	c.log(WARNING, format, a...)
}

// Error Error日志
func (c ConsoleLogger) Error(format string, a ...interface{}) {
	c.log(ERROR, format, a...)
}

// Fatal Fatal日志
func (c ConsoleLogger) Fatal(format string, a ...interface{}) {
	c.log(FATAL, format, a...)
}
