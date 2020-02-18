package mylogger

// 需求分析
// 1、支持往不同的地方输出日志
// 2、日志分级别
// 3、Debug  Trace  Info  Warning  Error  Fatal
// 4、日志要支持开关控制
// 5、完整的日志记录要包含时间、行号、文件名、日志级别、日志信息
// 6、日志文件要切割

import (
	"errors"
	"fmt"
	"path"
	"runtime"
	"strings"
	"time"
)

// LogLevel 日志等级
type LogLevel uint8

// Logger 日志接口
type Logger interface {
	Debug(format string, a ...interface{})
	Info(format string, a ...interface{})
	Fatal(format string, a ...interface{})
	Warning(format string, a ...interface{})
	Error(format string, a ...interface{})
}

// 定义日志级别
const (
	UNKNOWN LogLevel = iota
	DEBUG
	TRACE
	INFO
	WARNING
	ERROR
	FATAL
)

// 获取调用打印日志的文件以及所在的行数，方便定位
func getInfo(skip int) (funcName, fileName string, lineNo int) {
	pc, file, lineNo, ok := runtime.Caller(skip)
	if !ok {
		fmt.Printf("runtime.Caller() failed\n")
		return
	}
	funcName = runtime.FuncForPC(pc).Name()
	funcName = strings.Split(funcName, ".")[1]
	fileName = path.Base(file)
	return
}

// 获取当前时间
func getNow() string {
	return time.Now().Format("2006-01-02 15:04:05")
}

func getLogString(lv LogLevel) string {
	switch lv {
	case DEBUG:
		return "DEBUG"
	case TRACE:
		return "TRACE"
	case INFO:
		return "INFO"
	case WARNING:
		return "WARNING"
	case ERROR:
		return "ERROR"
	case FATAL:
		return "FATAL"
	default:
		return "DEBUG"
	}
}

func parseLogLevel(s string) (LogLevel, error) {
	switch strings.ToLower(s) {
	case "debug":
		return DEBUG, nil
	case "trace":
		return TRACE, nil
	case "info":
		return INFO, nil
	case "warning":
		return WARNING, nil
	case "error":
		return ERROR, nil
	case "fatal":
		return FATAL, nil
	default:
		err := errors.New("无效的日志级别")
		return UNKNOWN, err
	}
}
