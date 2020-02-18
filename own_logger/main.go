package main

import (
	"study/mylogger"
	"time"
)

var logger mylogger.Logger

func main() {
	logger = mylogger.NewFileLogger("info", "./", "a.log", 1*1024) // 文件日志示例

	// logger = mylogger.NewConsoleLogger("INFO") // 终端日志示例
	for {
		logger.Debug("这是一条debug日志")
		logger.Info("这是一条info日志%s", "Info")
		logger.Error("这是一条info日志%s", "Error")
		logger.Fatal("这是一条info日志%s", "Fatal")
		time.Sleep(time.Second * 2)
	}

}
