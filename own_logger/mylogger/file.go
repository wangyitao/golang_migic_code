package mylogger

import (
	"fmt"
	"os"
	"path"
	"time"
)

// 往文件里面写日志相关代码

// FileLogger 文件日志结构体
type FileLogger struct {
	Level       LogLevel
	filePath    string   // 日志文件保存路径
	fileName    string   // 日志文件保存的文件名
	fileObj     *os.File // 日志文件对象
	errFileObj  *os.File // 错误日志文件对象
	maxFileSize int64    // 日志文件分割大小
}

// NewFileLogger 新建文件日志对象
func NewFileLogger(levelStr, fp, fn string, maxSize int64) *FileLogger {
	logLevel, err := parseLogLevel(levelStr)
	if err != nil {
		panic(err)
	}
	fl := &FileLogger{
		Level:       logLevel,
		filePath:    fp,
		fileName:    fn,
		maxFileSize: maxSize,
	}
	err = fl.initFile() // 按照文件路径和文件名将文件打开
	if err != nil {
		panic(err)
	}
	return fl
}

// 初始化文件，根据指定的日志文件路径和文件名打开日志文件
func (f *FileLogger) initFile() error {
	fullFileName := path.Join(f.filePath, f.fileName)
	fileObj, err := os.OpenFile(fullFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("open log file failed,err:%v\n", err)
		return err
	}

	errFileObj, err := os.OpenFile(fullFileName+".err", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("open error log file failed,err:%v\n", err)
		return err
	}
	// 日志文件都已经打开
	f.fileObj = fileObj
	f.errFileObj = errFileObj
	return nil
}

// 切割文件
func (f *FileLogger) splitFile(file *os.File) (*os.File, error) {
	// 需要切割日志文件
	nowStr := time.Now().Format("20060102150405000")
	// 获取文件名
	fileInfo, err := file.Stat()
	if err != nil {
		fmt.Printf("get file info failed,err:%v\n", err)
		return nil, err
	}
	logName := path.Join(f.filePath, fileInfo.Name())      // 取到当前日志文件完整路径
	newLogName := fmt.Sprintf("%s.bak%s", logName, nowStr) // 备份的文件名
	// 1、关闭当前的日志文件
	file.Close()
	// 2、备份一下 rename
	os.Rename(logName, newLogName)
	// 3、打开一个新的日志文件
	fileObj, err := os.OpenFile(logName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("open log file failed,err:%v\n", err)
		return nil, err
	}
	return fileObj, nil
}

// 打印日志内容
func (f *FileLogger) log(lv LogLevel, format string, a ...interface{}) {
	if f.enable(lv) {
		msg := fmt.Sprintf(format, a...)
		funcName, fileName, lineNo := getInfo(3)
		if f.checkSize(f.fileObj) {
			newFile, err := f.splitFile(f.fileObj)
			if err != nil {
				return
			}
			f.fileObj = newFile
		}
		fmt.Fprintf(f.fileObj, "[%s] [%s] [%s:%s:%d] %s\n", getNow(), getLogString(lv), fileName, funcName, lineNo, msg)
		if lv >= ERROR {
			if f.checkSize(f.errFileObj) {
				newFile, err := f.splitFile(f.errFileObj)
				if err != nil {
					return
				}
				f.errFileObj = newFile
			}
			// 如果要记录的日志大于等于ERROR级别，还需要在err日志文件中再记录一遍
			fmt.Fprintf(f.errFileObj, "[%s] [%s] [%s:%s:%d] %s\n", getNow(), getLogString(lv), fileName, funcName, lineNo, msg)
		}
	}
}

// 检查日志是否需要进行切割
func (f *FileLogger) checkSize(file *os.File) bool {
	fileInfo, err := file.Stat()
	if err != nil {
		fmt.Printf("get file info failed,err:%v", err)
		return false
	}
	// 如果当前文件大小大于等于日志文件的最大值就应该返回true
	return fileInfo.Size() >= f.maxFileSize
}

// 根据日志级别筛选输出日志
func (f *FileLogger) enable(logLevel LogLevel) bool {
	return f.Level <= logLevel
}

// Debug 调试日志
func (f *FileLogger) Debug(format string, a ...interface{}) {
	f.log(DEBUG, format, a...)
}

// Info info日志
func (f *FileLogger) Info(format string, a ...interface{}) {
	f.log(INFO, format, a...)
}

// Warning warning日志
func (f *FileLogger) Warning(format string, a ...interface{}) {
	f.log(WARNING, format, a...)
}

// Error Error日志
func (f *FileLogger) Error(format string, a ...interface{}) {
	f.log(ERROR, format, a...)
}

// Fatal Fatal日志
func (f *FileLogger) Fatal(format string, a ...interface{}) {
	f.log(FATAL, format, a...)
}

// Close 关闭文件
func (f *FileLogger) Close() {
	f.fileObj.Close()
	f.errFileObj.Close()
}
