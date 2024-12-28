@echo off
REM 检查是否提供了两个参数
if "%~1"=="" (
    echo 错误: 未提供输入文件和输出文件!
    echo 用法: convert.bat [输入文件] [输出文件]
    exit /b 1
)

set input_file=%~1
set output_file=%~n1.html

REM 调用 Ruby 脚本并传递参数
ruby C:\D\bat_script\md_to_html.rb "%input_file%" "%output_file%"

python C:\D\bat_script\md_to_page.py "%output_file%"

exit /b 0
